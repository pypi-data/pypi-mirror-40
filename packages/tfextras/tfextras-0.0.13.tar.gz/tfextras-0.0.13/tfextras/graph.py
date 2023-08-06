import tensorflow as tf

def get_graph_nodes(graph=None):
    if graph is None:
        graph = tf.get_default_graph()
    return [ node.name for node in graph.as_graph_def().node ]
