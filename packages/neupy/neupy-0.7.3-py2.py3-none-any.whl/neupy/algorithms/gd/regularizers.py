from __future__ import division

from functools import wraps, partial

import tensorflow as tf

from neupy.utils import asfloat
from neupy.layers.utils import iter_parameters


__all__ = ('regularizer', 'l1', 'l2', 'maxnorm')


class Regularizer(object):
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.exclude = kwargs.pop('exclude', ['bias'])

        self.args = args
        self.kwargs = kwargs

    def __call__(self, network):
        return self.function(network, *self.args, **self.kwargs)
        cost = asfloat(0)

        for layer, attrname, param in iter_parameters(network):
            if attrname not in self.exclude:
                cost += self.function(param, *self.args, **self.kwargs)

        return cost

    def __repr__(self):
        kwargs_repr = [repr(arg) for arg in self.args]
        kwargs_repr += ["{}={}".format(k, v) for k, v in self.kwargs.items()]
        kwargs_repr.append("exclude={}".format(self.exclude))
        return "{}({})".format(self.function.__name__, ', '.join(kwargs_repr))


def regularizer(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return Regularizer(function, *args, *kwargs)
    return wrapper


@regularizer
def l1(weight, decay_rate=0.01):
    """
    Applies l1 regularization to the trainable parameters in the network.

    Regularization cost per weight parameter in the layer can be computed
    in the following way (pseudocode).

    .. code-block:: python

        cost = decay_rate * sum(abs(weight))

    Parameters
    ----------
    decay_rate : float
        Controls training penalties during the parameter updates.
        The larger the value the stronger effect regularization
        has during the training. Defaults to ``0.01``.

    exclude : list
        List of parameter names that has to be excluded from the
        regularization. Defauts to ``['bias']``.

    Examples
    --------
    >>> from neupy import algorithms
    >>> from neupy.layers import *
    >>>
    >>> optimizer = algorithms.Momentum(
    ...     Input(5) > Relu(10) > Sigmoid(1),
    ...     step=algorithms.l1(decay_rate=0.01)
    ... )

    With included regularization for bias

    >>> from neupy import algorithms
    >>> from neupy.layers import *
    >>>
    >>> optimizer = algorithms.Momentum(
    ...     Input(5) > Relu(10) > Sigmoid(1),
    ...     step=algorithms.l1(decay_rate=0.01, exclude=[])
    ... )
    """
    return tf.multiply(decay_rate, tf.reduce_sum(tf.abs(weight)))


@regularizer
def l2(weight, decay_rate=0.01):
    """
    Applies l2 regularization to the trainable parameters in the network.

    Regularization cost per weight parameter in the layer can be computed
    in the following way (pseudocode).

    .. code-block:: python

        cost = decay_rate * sum(weight ** 2)

    Parameters
    ----------
    decay_rate : float
        Controls training penalties during the parameter updates.
        The larger the value the stronger effect regularization
        has during the training. Defaults to ``0.01``.

    exclude : list
        List of parameter names that has to be excluded from the
        regularization. Defauts to ``['bias']``.

    Examples
    --------
    >>> from neupy import algorithms
    >>> from neupy.layers import *
    >>>
    >>> optimizer = algorithms.Momentum(
    ...     Input(5) > Relu(10) > Sigmoid(1),
    ...     step=algorithms.l2(decay_rate=0.01)
    ... )

    With included regularization for bias

    >>> from neupy import algorithms
    >>> from neupy.layers import *
    >>>
    >>> optimizer = algorithms.Momentum(
    ...     Input(5) > Relu(10) > Sigmoid(1),
    ...     step=algorithms.l2(decay_rate=0.01, exclude=[])
    ... )
    """
    return tf.multiply(decay_rate, tf.reduce_sum(tf.pow(weight, 2)))


@regularizer
def maxnorm(weight, decay_rate=0.01):
    """
    Applies l-inf regularization to the trainable parameters in the
    network. Also known and max-norm regularization.

    Regularization cost per weight parameter in the layer can be computed
    in the following way (pseudocode).

    .. code-block:: python

        cost = decay_rate * max(abs(weight))

    Parameters
    ----------
    decay_rate : float
        Controls training penalties during the parameter updates.
        The larger the value the stronger effect regularization
        has during the training. Defaults to ``0.01``.

    exclude : list
        List of parameter names that has to be excluded from the
        regularization. Defauts to ``['bias']``.

    Examples
    --------
    >>> from neupy import algorithms
    >>> from neupy.layers import *
    >>>
    >>> optimizer = algorithms.Momentum(
    ...     Input(5) > Relu(10) > Sigmoid(1),
    ...     step=algorithms.maxnorm(decay_rate=0.01)
    ... )

    With included regularization for bias

    >>> from neupy import algorithms
    >>> from neupy.layers import *
    >>>
    >>> optimizer = algorithms.Momentum(
    ...     Input(5) > Relu(10) > Sigmoid(1),
    ...     step=algorithms.maxnorm(decay_rate=0.01, exclude=[])
    ... )
    """
    return tf.multiply(decay_rate, tf.reduce_max(tf.abs(weight)))
