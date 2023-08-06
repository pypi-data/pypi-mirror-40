#!/usr/bin/env python3


"""
@author: xi
@since: 2019-01-04
"""

import tensorflow as tf

import photinia as ph

_BIG_NUMBER = 1e30


class ScaledDotProductAttention(ph.Widget):

    def __init__(self, name):
        super(ScaledDotProductAttention, self).__init__(name)

    def _build(self):
        pass

    def _setup(self, query, key, value, query_mask, key_mask):
        dim_q = tf.shape(query)[-1]

        # (batch_size, query_length, emb_size) @ (batch_size, emb_size, key_length)
        # => (batch_size, query_length, key_length)
        score = query @ tf.transpose(key, (0, 2, 1))
        score /= tf.sqrt(tf.cast(dim_q, ph.float))

        # (batch_size, query_length)
        # => (batch_size, query_length, 1)
        query_mask = tf.expand_dims(query_mask, 2)

        # (batch_size, key_length)
        # => (batch_size, 1, key_length)
        key_mask = tf.expand_dims(key_mask, 1)

        # => (batch_size, query_length, key_length)
        att = tf.nn.softmax(score - (1.0 - key_mask) * _BIG_NUMBER, axis=2)
        att *= query_mask

        # (batch_size, query_length, key_length) @ (batch_size, key_length, emb_size)
        # => (batch_size, query_length, emb_size)
        result = att @ value
        return result, att


class MultiHeadAttention(ph.Widget):

    def __init__(self,
                 name,
                 input_size,
                 state_size,
                 num_heads):
        """Multi-head attention.

        Args:
            name (str): Widget name.
            input_size (int): Input size. It is usually "vocabulary size" or "word embedding size".
            state_size (int): The state size for every sequence element.
            num_heads (int): Number of heads.

        """
        self._input_size = input_size
        self._state_size = state_size
        self._num_heads = num_heads
        super(MultiHeadAttention, self).__init__(name)

    def _build(self):
        self._linear_q = ph.Linear('linear_q', self._input_size, self._state_size)
        self._linear_k = ph.Linear('linear_k', self._input_size, self._state_size)
        self._linear_v = ph.Linear('linear_v', self._input_size, self._state_size)
        self._sdp_attention = ScaledDotProductAttention('attention')

    def _setup(self, query, key, query_mask, key_mask):
        # => (batch_size, seq_len, state_size]
        wq = self._linear_q.setup(query, axes=((-1,), (0,)))
        wk = self._linear_k.setup(key, axes=((-1,), (0,)))
        wv = self._linear_v.setup(key, axes=((-1,), (0,)))

        # (batch_size, seq_length, state_size)
        # => (batch_size * num_heads, seq_len, state_size / num_heads)
        wq_ = tf.concat(tf.split(wq, self._num_heads, axis=2), axis=0)
        wk_ = tf.concat(tf.split(wk, self._num_heads, axis=2), axis=0)
        wv_ = tf.concat(tf.split(wv, self._num_heads, axis=2), axis=0)

        # (batch_size, seq_length)
        # => (batch_size * num_heads, seq_length)
        query_mask = tf.tile(query_mask, (self._num_heads, 1))
        key_mask = tf.tile(key_mask, (self._num_heads, 1))

        # result.shape = [batch_size*H, query_len, state_size/H]
        # => (batch_size  * num_heads, query_length, state_size / num_heads)
        result, attention = self._sdp_attention.setup(wq_, wk_, wv_, query_mask, key_mask)
        # => (batch_size, query_length, state_size)
        result = tf.concat(tf.split(result, self._num_heads, axis=0), axis=2)

        return result, attention


class LayerNorm(ph.Widget):

    def __init__(self, name, size, eps=1e-6):
        self._name = name
        self._size = size
        self._eps = eps
        super(LayerNorm, self).__init__(name)

    def _build(self):
        self._w = self._variable(
            name='w',
            initializer=tf.ones(shape=(self._size,), dtype=ph.float),
            shape=(self._size,),
            dtype=ph.float,
        )
        self._b = self._variable(
            name='b',
            initializer=tf.zeros(shape=(self._size,), dtype=ph.float),
            shape=(self._size,),
            dtype=ph.float,
        )

    def _setup(self, seq):
        mean, var = tf.nn.moments(seq, axes=-1)
        normalized = (seq - mean) / tf.sqrt(var + self._eps)
        result = self._w * normalized + self._b
        return result
