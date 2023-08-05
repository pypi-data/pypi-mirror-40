import tensorflow as tf

def get_graph_nodes():
    return [node.name for node in tf.get_default_graph().as_graph_def().node]
