import tensorflow as tf
import numpy as np

from tfextras.io import GraphIO

class GraphTrainer:

    def __new__(cls, *args):
        np.set_printoptions(suppress=True)
        return super(GraphTrainer, cls).__new__(cls)

    def __init__(self, epochs=500, batch_size=32):
        self.epochs = epochs
        self.batch_size = batch_size

    def run_training_epoch(self, batch_count, callback=lambda *args: None):
        train_losses = []
        train_predicts = []
        train_accuracy = []
        for n in range(batch_count):
            _, l, p, a = self.session.run([
                self.train_op,
                self.loss_op,
                self.predict_op,
                self.accuracy_op
            ])
            train_losses = np.append(
                train_losses,
                l
            )
            train_predicts = np.append(
                train_predicts,
                p
            )
            train_accuracy = np.append(
                train_accuracy,
                a
            )
            callback(l, c, a, train_losses, train_predicts, train_accuracy)
        return train_losses, train_predicts, train_accuracy

    def run_test_epoch(self, test_count, callback=lambda *args: None):
        test_losses = []
        test_predicts = []
        test_accuracy = []
        for n in range(test_count):
            l, p, a = self.session.run([
                self.loss_op,
                self.predict_op,
                self.accuracy_op
            ])
            test_losses = np.append(
                test_losses,
                l
            )
            test_predicts = np.append(
                test_predicts,
                p
            )
            test_accuracy = np.append(
                test_accuracy,
                a
            )
            callback(l, c, a, test_losses, test_predicts, test_accuracy)
        return test_losses, test_predicts, test_accuracy

    def run(self, device, train_data, test_data, create_graph_outputs):
        tf.reset_default_graph()

        x_train, y_train = train_data
        x_test, y_test = test_data

        assert x_train.shape[1:] == x_test.shape[1:], 'training and test features shape mismatch'
        assert y_train.shape[1:] == y_test.shape[1:], 'training and test labels shape mismatch'

        input_shape = x_train[1:]
        output_shape = y_train[1:]
        batch_count = x_train.shape[0]//self.batch_size
        test_count = x_test.shape[0]//self.batch_size

        # TODO: Accumulation & graph saving
        max_val_acc = 0

        self.io = GraphIO(
            device,
            input_shape,
            output_shape
        )

        with self.io:
            (self.output,
             self.train_op,
             self.loss_op,
             self.prediction_op,
             self.accuracy_op) = create_graph_outputs(self.io.features, self.io.labels)

        self.session = tf.Session(config=self.io.config)
        self.session.run(tf.global_variables_initializer())

        try:
            for epoch in range(epochs):

                # Run training epoch
                self.io.enable_training(
                    self.session,
                    x_train,
                    y_train,
                    batch_size
                )
                train_losses, train_predicts, train_accuracy = self.run_training_epoch(
                    batch_count,
                    # TODO: callback
                )

                # Run testing epoch
                self.io.enable_testing(
                    self.session,
                    x_test,
                    y_test,
                    batch_size
                )
                test_losses, test_predicts, test_accuracy = self.run_test_epoch(
                    test_count,
                    # TODO: callback
                )

                # TODO: Summary writer

        except KeyboardInterrupt:
            pass
            # TODO: Logging
            # TODO: Clean up & save
