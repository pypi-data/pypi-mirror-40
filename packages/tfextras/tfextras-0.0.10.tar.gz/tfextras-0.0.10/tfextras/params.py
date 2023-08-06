import tensorflow as tf
import yaml

class Hyperparams(tf.contrib.training.HParams):

    def __init__(self, **kwargs):
        super(Hyperparams, self).__init__(**self.from_kwargs(kwargs))

    def __getitem__(self, key):
        return getattr(self, key)

    def from_kwargs(self, kwargs):
        result = dict()
        for key, value in kwargs.items():
            if isinstance(value, dict):
                result[key] = Hyperparams(**value)
            else:
                result[key] = value
        return result

    def to_dict(self):
        result = dict()
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, Hyperparams):
                    result[key] = value.to_dict()
                else:
                    result[key] = value
        return result

    def from_yaml(self, content):
        self.__dict__.update(Hyperparams(**yaml.load(content)).__dict__)

    def to_yaml(self):
        return yaml.dump(self.to_dict(), default_flow_style=False)
