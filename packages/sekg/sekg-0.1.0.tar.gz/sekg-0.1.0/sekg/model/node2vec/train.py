#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

from sekg.model.node2vec import node2vec


class GraphNode2VecTrainer():
    def __init__(self, graph_data):
        self.graph_data = graph_data
        self.node_num = graph_data.get_node_num()
        self.nx_G_instance = None

    def init_graph(self):
        node_ids = self.graph_data.get_node_ids()
        relation_pairs = self.graph_data.get_relation_pairs()
        print("node num=%d" % self.node_num)
        print("relation num=%d" % len(relation_pairs))
        G = nx.DiGraph()
        G.add_nodes_from(node_ids)
        G.add_edges_from(relation_pairs, weight=1.0)
        # todo: a relation weight support
        self.nx_G_instance = G

    def generate_random_path(self, rw_path_store_path, directed=False, p=1, q=1, num_walks=10, walk_length=80,
                             ):
        G = node2vec.Graph(self.nx_G_instance, directed, p, q)
        G.preprocess_transition_probs()
        walks = G.simulate_walks(num_walks, walk_length)
        # todo: may be load all into memory has problem?
        with open(rw_path_store_path, 'w') as write_f:
            for walk in walks:
                path_str = " ".join([str(item) for item in walk])
                write_f.writelines('%s\n' % (path_str))

    @staticmethod
    def train(rw_path_store_path, model_path, dimensions=100,
              workers=4):
        """
        train the graph vector from rw_path
        :param rw_path_store_path: the random walk for one graph
        :param model_path: the output word2vec model path
        :param dimensions: the dimensions of word2vec
        :param workers: the num of pipeline training
        :return:
        """
        # Learn embeddings by optimizing the Skipgram objective using SGD.
        w2v = Word2Vec(LineSentence(rw_path_store_path), size=dimensions, min_count=0, sg=1, workers=workers)
        w2v.wv.save(model_path)
        return w2v
