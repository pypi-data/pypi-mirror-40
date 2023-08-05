# NOTES:
# (1) Save raw graphs
# (2) Automatically save model on peak test acc
# (3) Make sure io graph is not saved along with the model or the data is empty
import tensorflow as tf
import numpy as np
import warnings
import tqdm
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
        verbosity=1,
        progress=0,
        summary_path=None,
        model_path=None):
        self.max_epochs = max_epochs
        self.batch_size = batch_size
        self.test_interval = test_interval
        self.verbosity = verbosity
        self.progress = progress
        self.summary_path = summary_path
        self.summary_batch = None
        self.summary_epoch = None
        self.model_path = model_path
        self.train_step = 0
        self.test_step = 0
        self.train_progress = None
        self.test_progress = None
        self.train_writer = None
        self.test_writer = None
        self.saver = None

    @property
    def index(self):
        if self.summary_path and os.path.exists(self.summary_path):
            return len(os.listdir(self.summary_path))
        return 0

    def log(self, *args):
        int(self.verbosity) > 0 and print(*args)

    # TODO: Restore from checkpoint file
    def restore_graph(self, path=None):
        # NOTE: Returns create_training_outputs function
        pass

    # TODO: Portable graph with SavedModel
    def export_graph(self, path=None):
        pass

    # TODO: Write to checkpoint file
    def save_graph(self, path=None):
        if self.saver:
            pass

    def create_graphio(self, create_training_outputs, *ioargs):
        with GraphIO(*ioargs, log_placement=self.verbosity > 1) as self.io:
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
        if self.model_path:
            self.saver = tf.train.Saver()
            return self.saver
        return None

    def create_summaries(self):
        self.loss_history = tf.placeholder(tf.float32, [ None ], name='loss_history')
        self.accuracy_history = tf.placeholder(tf.float32, [ None ], name='accuracy_history')

        if not self.summary_path:
            self.mean_loss = tf.no_op(name='mean_loss')
            self.mean_accuracy = tf.no_op(name='mean_accuracy')
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
            self.mean_loss = tf.reduce_mean(
                self.loss_history,
                name='mean_loss'
            )
            self.mean_accuracy = tf.reduce_mean(
                self.accuracy_history,
                name='mean_accuracy'
            )
            self.summary_epoch = tf.summary.merge([
                tf.summary.scalar('mean_loss', self.mean_loss),
                tf.summary.histogram('loss_history', self.loss_history),
                tf.summary.scalar('mean_accuracy', self.mean_accuracy),
                tf.summary.histogram('accuracy_history', self.accuracy_history)
            ])
        self.train_writer = tf.summary.FileWriter(
            self.summary_path + '/' + str(self.index) + '/train',
            self.session.graph
        )
        self.test_writer = tf.summary.FileWriter(
            self.summary_path + '/' + str(self.index - 1) + '/test'
        )
        return self.train_writer, self.test_writer

    def training_callback(self, *args):
        (epoch,
        total,
        count,
        loss,
        predict,
        acc,
        summary,
        train_losses, _, train_accuracy) = args

        self.train_step += 1

        if self.progress and self.train_progress is None:
            self.train_progress = tqdm.tqdm(
                total=total,
                ascii=True
            )

        if self.train_progress:
            self.train_progress.update(1)
            self.train_progress.set_description('Training [{:03d}/{:03d}], loss={:.6f}, acc={:.2f}%'.format(
                count+1,
                total,
                loss,
                acc * 100.
            ))

        if self.train_writer:
            self.train_writer.add_summary(summary, self.train_step)

        if count >= total - 1:
            self.train_progress and self.train_progress.close()
            self.train_progress = None
            ml, ma, summary = self.session.run([
                    self.mean_loss,
                    self.mean_accuracy,
                    self.summary_epoch
                ], feed_dict={
                    self.loss_history: train_losses,
                    self.accuracy_history: train_accuracy,
                })
            self.train_writer and self.train_writer.add_summary(summary, epoch)

    def testing_callback(self, *args):
        (epoch,
        total,
        count,
        loss,
        predict,
        acc,
        summary,
        test_losses, _, test_accuracy) = args

        self.test_step += (self.train_step - self.test_step) // (total - count)

        if self.progress and self.test_progress is None:
            self.test_progress = tqdm.tqdm(
                total=total,
                ascii=True
            )

        if self.test_progress:
            self.test_progress.update(1)
            self.test_progress.set_description('Testing  [{:03d}/{:03d}], loss={:.6f}, acc={:.2f}%'.format(
                count+1,
                total,
                loss,
                acc * 100.
            ))

        if self.test_writer:
            self.test_writer.add_summary(summary, self.test_step)

        if count >= total - 1:
            self.test_progress and self.test_progress.close()
            self.test_progress = None
            ml, ma, summary = self.session.run([
                    self.mean_loss,
                    self.mean_accuracy,
                    self.summary_epoch
                ], feed_dict={
                    self.loss_history: test_losses,
                    self.accuracy_history: test_accuracy,
                })
            self.test_writer and self.test_writer.add_summary(summary, epoch)

    def run_training_epoch(self, current_epoch, train_batch_count, x_train, y_train):
        self.io.enable_training(
            self.session,
            x_train,
            y_train,
            self.batch_size
        )
        train_losses = []
        train_predicts = []
        train_accuracy = []
        for n in range(train_batch_count):
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
                current_epoch,
                train_batch_count,
                n,
                l,
                p,
                a,
                s,
                train_losses,
                train_predicts,
                train_accuracy
            )
        return train_losses, train_predicts, train_accuracy

    def run_test_epoch(self, current_epoch, test_batch_count, x_test, y_test):
        self.io.enable_testing(
            self.session,
            x_test,
            y_test,
            self.batch_size
        )
        test_losses = []
        test_predicts = []
        test_accuracy = []
        for n in range(test_batch_count):
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
                current_epoch,
                test_batch_count,
                n,
                l,
                p,
                a,
                s,
                test_losses,
                test_predicts,
                test_accuracy
            )
        return test_losses, test_predicts, test_accuracy

    def run(self, train_data, test_data, create_training_outputs, device=None):
        x_train, y_train = train_data
        x_test, y_test = test_data

        assert x_train.shape[1:] == x_test.shape[1:], 'training and test features shape mismatch'
        assert y_train.shape[1:] == y_test.shape[1:], 'training and test labels shape mismatch'

        input_shape = x_train.shape[1:]
        output_shape = y_train.shape[1:]
        train_batch_count = x_train.shape[0]//self.batch_size
        test_batch_count = x_test.shape[0]//self.batch_size

        self.create_graphio(
            create_training_outputs,
            input_shape,
            output_shape,
            device,
        )
        self.create_session()

        with self.io:
            self.create_saver()
            self.create_summaries()
            self.init_op = tf.global_variables_initializer()

        self.session.run(self.init_op)
        self.log('\nStart training for max {} epochs'.format(self.max_epochs))
        try:
            for epoch in range(self.max_epochs):
                self.log('{}[ Epoch={} ] =>'.format('\n'*2, epoch+1))

                # Run training epoch
                train_losses, train_predicts, train_accuracy = self.run_training_epoch(
                    epoch,
                    train_batch_count,
                    x_train,
                    y_train
                )

                # Run testing epoch only on every Nth interval
                if epoch == 0 or epoch % self.test_interval == 0:
                    test_losses, test_predicts, test_accuracy = self.run_test_epoch(
                        epoch,
                        test_batch_count,
                        x_test,
                        y_test
                    )
        except KeyboardInterrupt:
            self.log('\nUser stopped training.')
        except Exception as e:
            self.log('\nTraining stopped due to exception:', e)

        self.save_graph()
        self.session.close()
