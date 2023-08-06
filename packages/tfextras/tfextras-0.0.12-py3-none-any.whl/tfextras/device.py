from tensorflow.contrib.memory_stats.python.ops.memory_stats_ops import BytesInUse
from tensorflow.python.client import device_lib

def find_free_devices(type='gpu', min_memory=0):
    if type == 'cpu':
        return find_devices(type)
    devices = []
    with tf.Session() as sess:
        for dev in filter(lambda dev: dev.device_type == type.upper(), device_lib.list_local_devices()):
            with tf.device(dev):
                bytes_in_use = sess.run(BytesInUse())
                if dev.memory_limit - bytes_in_use > min_memory:
                    devices.append(dev.name)
    return devices

def find_devices(type='gpu'):
    return list(
        map(
            lambda dev: dev.name,
            filter(
                lambda dev: dev.device_type == type.upper(),
                device_lib.list_local_devices()
            )
        )
    )
