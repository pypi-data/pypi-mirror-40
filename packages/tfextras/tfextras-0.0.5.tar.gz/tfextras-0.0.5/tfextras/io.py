import tensorflow as tf

class GraphIO:

    def __init__(self, input_shape, output_shape, device=None, log_placement=False):
        self.config = tf.ConfigProto(
            log_device_placement=log_placement,
            allow_soft_placement=True,
        )
        self.config.gpu_options.allow_growth = True
        self.graph = None
        self.device = device
        with self:
            self.create(input_shape, output_shape)

    def __enter__(self, *args):
        self.graph = self.graph or tf.Graph()
        self.graph_context = self.graph.as_default()
        self.graph_context.__enter__()
        self.device_context = tf.device(self.device)
        self.device_context.__enter__()
        return self

    def __exit__(self, *args):
        self.graph_context.__exit__(*args)
        self.device_context.__exit__(*args)

    def create(self, input_shape, output_shape):
        with tf.name_scope('io'):
            self.x = tf.placeholder(tf.float32, shape=[None, *input_shape], name='x')
            self.y = tf.placeholder(tf.float32, shape=[None, *output_shape], name='y')
            self.batch_size = tf.placeholder(tf.int64, name='batch_size_placeholder')

            with tf.name_scope('train_data'):
                train_dataset = tf.data.Dataset.from_tensor_slices((self.x, self.y)).batch(
                        self.batch_size
                    ).repeat()

            with tf.name_scope('test_data'):
                test_dataset = tf.data.Dataset.from_tensor_slices((self.x, self.y)).batch(
                        self.batch_size
                    ).repeat()

            with tf.name_scope('data_iterator'):
                iter_data = tf.data.Iterator.from_structure(
                    train_dataset.output_types,
                    train_dataset.output_shapes
                )

            self.features, self.labels = iter_data.get_next()

            self.train_init_op = iter_data.make_initializer(train_dataset, name='train_init_op')
            self.test_init_op = iter_data.make_initializer(test_dataset, name='test_init_op')

    def enable_training(self, session, x_train, y_train, batch_size):
        session.run(
            self.train_init_op,
            feed_dict={
                self.x: x_train,
                self.y: y_train,
                self.batch_size: batch_size
            }
        )

    def enable_testing(self, session, x_test, y_test, batch_size):
        session.run(
            self.test_init_op,
            feed_dict={
                self.x: x_test,
                self.y: y_test,
                self.batch_size: batch_size
            }
        )
