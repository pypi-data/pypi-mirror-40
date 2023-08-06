import tensorflow as tf
import numpy as np
import traceback
import warnings
import types
import math
import tqdm
import time
import os

from tfextras.io import GraphIO

class GraphTrainer:

    def __new__(cls, *args, **kwargs):
        np.set_printoptions(suppress=True)
        return super(GraphTrainer, cls).__new__(cls)

    def __init__(self,
        max_epochs=1,
        batch_size=1,
        test_interval=1,
        stats_interval=1,
        verbosity=1,
        progress=0,
        log_path=None,
        summary_path=None,
        model_path=None,
        model_save_accuracy=math.inf):

        self.max_epochs = max_epochs
        self.batch_size = batch_size
        self.test_interval = test_interval
        self.stats_interval = stats_interval
        self.verbosity = verbosity
        self.progress = progress
        self.log_path = log_path
        self.model_path = model_path
        self.model_save_accuracy = model_save_accuracy
        self.summary_path = summary_path
        self.summary_batch = None
        self.summary_epoch = None
        self.global_index = 0
        self.global_step = 0
        self.train_step = 0
        self.test_step = 0
        self.train_writer = None
        self.test_writer = None
        self.input_shape = None
        self.output_shape = None
        self.graph_ready = False
        self.session = None
        self.stats = None
        self.saver = None

    def __repr__(self):
        return (
            '[ Stats ] {}'
            '\n\t* epoch:\t\t{}'
            '\n\t* best epoch:\t\t{}'
            '\n\t* min. train loss:\t{:0.9f}'
            '\n\t* min. test loss:\t{:0.9f}'
            '\n\t* max. train accuracy:\t{:.5f}%'
            '\n\t* max. test accuracy:\t{:.5f}%\n'
        ).format(
            '-' * 40,
            self.stats.current_epoch,
            self.stats.best_epoch,
            self.stats.min_train_loss,
            self.stats.min_test_loss,
            self.stats.max_train_acc * 100,
            self.stats.max_test_acc * 100,
        )

    @property
    def epoch(self):
        return self.global_step + 1

    @property
    def default_name(self):
        return 'model-{:03d}-a{:.3f}'.format(
            self.epoch,
            self.stats.current_test_acc * 100.
        )

    @property
    def default_wait(self):
        return 0.1 if self.progress else 0

    @property
    def has_summaries_enabled(self):
        return self.summary_path is not None

    @property
    def has_saving_enabled(self):
        return self.model_path is not None

    @property
    def has_logging_enabled(self):
        return self.log_path is not None and self.graph_ready

    @property
    def is_test_epoch(self):
        return (self.global_step == 0 or self.epoch == self.max_epochs or self.global_step % self.test_interval == 0)

    @property
    def is_stats_epoch(self):
        return (self.global_step == 0 or self.global_step % self.stats_interval == 0) and self.stats_interval > 0

    def init_path(self, path):
        if path and not os.path.exists(path):
            os.makedirs(path)
        return path

    def init_paths(self):
        for path_attr in filter(lambda attr: attr.endswith('_path'), self.__dict__.keys()):
            self.init_path(getattr(self, path_attr))

    def init_index(self):
        for path_attr in [ 'log_path', 'summary_path', 'model_path' ]:
            path = getattr(self, path_attr)
            if path and os.path.exists(path):
                self.global_index = len(os.listdir(path))
                return self.global_index
        return 0

    def init_stats(self):
        self.stats = types.SimpleNamespace(
            current_epoch=-1,
            best_epoch=-1,
            current_train_loss=math.inf,
            current_train_acc=0,
            current_test_loss=math.inf,
            current_test_acc=0,
            min_train_loss=math.inf,
            min_test_loss=math.inf,
            max_train_acc=0.,
            max_test_acc=0.
        )
        return self.stats

    def init_data(self, train_data, test_data):
        if not self.input_shape:
            raise AttributeError('graph input shape is not defined. run create_graph() first')
        if not self.output_shape:
            raise AttributeError('graph output shape is not defined. run create_graph() first')

        x_train, y_train = train_data
        x_test, y_test = test_data

        assert x_train.shape[1:] == x_test.shape[1:], 'training and test features dimensions mismatch'
        assert y_train.shape[1:] == y_test.shape[1:], 'training and test labels dimensions mismatch'
        assert x_train.shape[1:] == self.input_shape, 'data and graph input dimensions mismatch'
        assert y_train.shape[1:] == self.output_shape, 'data and graph output dimensions mismatch'

        self.train_batch_count = x_train.shape[0]//self.batch_size
        self.test_batch_count = x_test.shape[0]//self.batch_size

        return (x_train, y_train, x_test, y_test)

    def index_path(self, path_name):
        path = getattr(self, path_name + '_path', None)
        if path:
            return self.init_path(os.path.join(path, str(self.global_index)))
        return None

    def create_io(self, create_training_outputs, *args, **kwargs):
        with GraphIO(*args, log_placement=self.verbosity > 1, **kwargs) as self.io:
            try:
                (self.output,
                self.train_op,
                self.loss_op,
                self.predict_op,
                self.accuracy_op) = create_training_outputs(self.io.features, self.io.labels)
                return self.io
            except (ValueError, TypeError) as e:
                warnings.warn('''create_training_outputs() should return the following operations: \
                    output, train_op, loss_op, predict_op, accuracy_op. Return tf.no_op for \
                    operations that are not relevant in your case''', UserWarning)
                raise e

    def create_session(self):
        self.session = tf.Session(
            graph=self.io.graph,
            config=self.io.config
        )
        return self.session

    def create_saver(self):
        self.saver = tf.train.Saver(
            # TODO: additional arguments?
        )
        return self.saver

    def create_summaries(self):
        self.loss_history = tf.placeholder(
            tf.float32,
            [ None ],
            name='loss_history'
        )
        self.accuracy_history = tf.placeholder(
            tf.float32,
            [ None ],
            name='accuracy_history'
        )
        self.mean_loss = tf.reduce_mean(
            self.loss_history,
            name='mean_loss'
        )
        self.mean_accuracy = tf.reduce_mean(
            self.accuracy_history,
            name='mean_accuracy'
        )

        if not self.summary_path:
            self.summary_batch = tf.no_op(name='summary_batch')
            self.summary_epoch = tf.no_op(name='summary_epoch')
            return None, None

        with tf.name_scope('summary_batch'):
            self.summary_batch = tf.summary.merge([
                tf.summary.scalar('loss', self.loss_op),
                tf.summary.scalar('accuracy', self.accuracy_op),
                tf.summary.histogram('predictions', self.predict_op),
            ])
        with tf.name_scope('summary_epoch'):
            self.summary_epoch = tf.summary.merge([
                tf.summary.scalar('mean_loss', self.mean_loss),
                tf.summary.histogram('loss_history', self.loss_history),
                tf.summary.scalar('mean_accuracy', self.mean_accuracy),
                tf.summary.histogram('accuracy_history', self.accuracy_history)
            ])

    def create_summary_writers(self):
        if self.has_summaries_enabled:
            self.train_writer = tf.summary.FileWriter(
                os.path.join(self.index_path('summary'), 'train'),
                self.session.graph
            )
            self.test_writer = tf.summary.FileWriter(
                os.path.join(self.index_path('summary'), 'test')
            )
            return self.train_writer, self.test_writer
        return None, None

    def create_graph(self, create_training_outputs, input_shape, output_shape, device=None):
        self.input_shape = input_shape
        self.output_shape = output_shape

        self.session and self.session.close()
        self.graph_ready = False

        with self.create_io(
            create_training_outputs,
            self.input_shape,
            self.output_shape,
            device):
            self.create_session()
            self.create_saver()
            self.create_summaries()
            self.init_op = tf.global_variables_initializer()

            self.log('Initialized graph topology with IO dimensions {}:{}'.format(
                tuple(self.input_shape),
                tuple(self.output_shape)
            ))

        self.session.run(self.init_op)
        self.graph_ready = True

    def save_graph(self, path=None, name=None):
        self.io.enable_predict(self.session)
        model_path = path or os.path.join(
            self.index_path('model'),
            name or self.default_name
        )
        return self.saver.save(self.session, model_path)

    def restore_graph(self, path=None):
        # TODO: Restore from checkpoint file
        raise NotImplementedError('restore_graph() is not implemented')

    def export_graph(self, path=None):
        # TODO: Portable graph with SavedModel
        raise NotImplementedError('export_graph() is not implemented')

    def update_stats(self,
        epoch=0,
        train_mean_loss=math.inf,
        train_mean_acc=0,
        test_mean_loss=math.inf,
        test_mean_acc=0):

        self.stats.current_epoch = max(epoch, self.stats.current_epoch)
        self.stats.current_train_loss = train_mean_loss or self.stats.current_train_loss
        self.stats.current_train_acc = train_mean_acc or self.stats.current_train_acc
        self.stats.current_test_loss = test_mean_loss or self.stats.current_test_loss
        self.stats.current_test_acc = test_mean_acc or self.stats.current_test_acc

        if train_mean_loss < self.stats.min_train_loss:
            self.stats.min_train_loss = train_mean_loss
        if test_mean_loss < self.stats.min_test_loss:
            self.stats.min_test_loss = test_mean_loss
        if train_mean_acc > self.stats.max_train_acc:
            self.stats.max_train_acc = train_mean_acc
        if test_mean_acc > self.stats.max_test_acc:
            self.stats.max_test_acc = test_mean_acc
            self.stats.best_epoch = max(epoch, self.stats.best_epoch)
            return True
        return False

    def update_progress(self, label, step, total, *metrics):
        if self.progress is not None and not self.progress:
            return False

        if self.progress is None or not isinstance(self.progress, tqdm.tqdm):
            self.progress = tqdm.tqdm(
                total=total,
                ascii=True
            )
        self.progress.update(1)
        label = label.capitalize() + (8 - len(label)) * ' '
        if step == total:
            self.progress.set_description('{} [{:03d}/{:03d}], avg_loss={:.6f}, avg_acc={:.2f}%'.format(
                label,
                total,
                total,
                *metrics
            ))
            self.progress.close()
            self.progress = None
        else:
            self.progress.set_description('{} [{:03d}/{:03d}], loss={:.6f}, acc={:.2f}%'.format(
                label,
                step,
                total,
                *metrics
            ))
        return True

    def training_callback(self, *args):
        (loss,
        predict,
        acc,
        summary,
        train_losses, _, train_accuracy) = args

        self.train_writer and self.train_writer.add_summary(
            summary,
            self.global_step * self.train_batch_count + \
            self.train_step
        )

        if self.train_step >= self.train_batch_count:
            loss, acc, epoch_summary = self.session.run([
                    self.mean_loss,
                    self.mean_accuracy,
                    self.summary_epoch
                ], feed_dict={
                    self.loss_history: train_losses,
                    self.accuracy_history: train_accuracy,
                })
            self.train_writer and self.train_writer.add_summary(
                epoch_summary,
                self.epoch
            )
            self.update_stats(self.epoch, train_mean_loss=loss, train_mean_acc=acc)

        self.update_progress(
            'training',
            self.train_step,
            self.train_batch_count,
            loss,
            acc * 100.
        )

    def testing_callback(self, *args):
        (loss,
        predict,
        acc,
        summary,
        test_losses, _, test_accuracy) = args
        acc_peak = False

        self.test_writer and self.test_writer.add_summary(
            summary,
            self.global_step * self.train_batch_count + \
            (self.train_batch_count // self.test_batch_count) * \
            self.test_step
        )

        if self.test_step >= self.test_batch_count:
            loss, acc, epoch_summary = self.session.run([
                    self.mean_loss,
                    self.mean_accuracy,
                    self.summary_epoch
                ], feed_dict={
                    self.loss_history: test_losses,
                    self.accuracy_history: test_accuracy,
                })
            self.test_writer and self.test_writer.add_summary(
                epoch_summary,
                self.epoch
            )
            acc_peak = self.update_stats(self.epoch, test_mean_loss=loss, test_mean_acc=acc)

        self.update_progress(
            'testing',
            self.test_step,
            self.test_batch_count,
            loss,
            acc * 100.
        )

        if acc_peak and self.has_saving_enabled and acc > self.model_save_accuracy:
            saved_path = self.save_graph(name='model-e{:03d}-a{:.3f}'.format(
                self.epoch,
                acc * 100.
            ))
            self.log('Reached accuracy peak. Model saved to "{}"'.format(saved_path))

    def run_training_epoch(self, x_train, y_train):
        self.io.enable_training(
            self.session,
            x_train,
            y_train,
            self.batch_size
        )
        train_losses = []
        train_predicts = []
        train_accuracy = []
        for self.train_step in range(1, self.train_batch_count + 1):
            _, l, p, a, s = self.session.run([
                self.train_op,
                self.loss_op,
                self.predict_op,
                self.accuracy_op,
                self.summary_batch
            ])
            train_losses = np.append(train_losses, l)
            train_predicts = np.append(train_predicts, p)
            train_accuracy = np.append(train_accuracy, a)
            self.training_callback(
                l,
                p,
                a,
                s,
                train_losses,
                train_predicts,
                train_accuracy
            )
        return train_losses, train_predicts, train_accuracy

    def run_test_epoch(self, x_test, y_test):
        self.io.enable_testing(
            self.session,
            x_test,
            y_test,
            self.batch_size
        )
        test_losses = []
        test_predicts = []
        test_accuracy = []
        for self.test_step in range(1, self.test_batch_count + 1):
            l, p, a, s = self.session.run([
                self.loss_op,
                self.predict_op,
                self.accuracy_op,
                self.summary_batch
            ])
            test_losses = np.append(test_losses, l)
            test_predicts = np.append(test_predicts, p)
            test_accuracy = np.append(test_accuracy, a)
            self.testing_callback(
                l,
                p,
                a,
                s,
                test_losses,
                test_predicts,
                test_accuracy
            )
        return test_losses, test_predicts, test_accuracy

    def run(self, train_data, test_data):
        self.init_paths()
        self.init_index()
        self.init_stats()

        x_train, y_train, x_test, y_test = self.init_data(
            train_data,
            test_data
        )

        self.create_summary_writers()
        self.log('Trainer start -- run {}, max. {} epochs'.format(self.global_index, self.max_epochs))
        try:
            for self.global_step in range(self.max_epochs):
                time.sleep(self.default_wait)

                self.run_training_epoch(x_train, y_train)
                time.sleep(self.default_wait)

                if self.is_test_epoch:
                    self.run_test_epoch(x_test, y_test)
                    time.sleep(self.default_wait)

                if self.is_stats_epoch:
                    self.log(repr(self))
                    time.sleep(self.default_wait)

        except KeyboardInterrupt:
            self.log('\nUser stopped training.')
        except Exception as e:
            self.log('\nTraining stopped due to exception')
            self.log(traceback.format_exc())

        if self.has_saving_enabled:
            saved_path = self.save_graph()
            saved_path and self.log('Model saved to "{}"'.format(saved_path))

    def log(self, *args):
        if int(self.verbosity) > 0:
            print(*args)
        if self.has_logging_enabled:
            with open(os.path.join(self.index_path('log'), 'output.log'), 'a') as log_file:
                print(*args, file=log_file)
