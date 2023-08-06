# -*- coding: utf-8 -*-
""" The generic kl-UCB policy for one-parameter exponential distributions.
By default, it assumes Bernoulli arms.
Note: using log(t) + c log(log(t)) for the KL-UCB index of just log(t)
Reference: [Garivier & Cappé - COLT, 2011].
"""
from __future__ import division, print_function  # Python 2 compatibility

__author__ = "Lilian Besson"
__version__ = "0.5"

from math import log
import numpy as np
np.seterr(divide='ignore')  # XXX dangerous in general, controlled here!

try:
    from .klUCB import klUCB
except ImportError:
    from klUCB import klUCB


class klUCBloglog(klUCB):
    """ The generic kl-UCB policy for one-parameter exponential distributions.
    By default, it assumes Bernoulli arms.
    Note: using log(t) + c log(log(t)) for the KL-UCB index of just log(t)
    Reference: [Garivier & Cappé - COLT, 2011].
    """

    def __str__(self):
        return r"kl-UCB({}{}{})".format("" if self.c == 1 else r"$c={:.3g}$, ".format(self.c), r"$\log\log$, ", self.klucb.__name__[5:])

    def computeIndex(self, arm):
        r""" Compute the current index, at time t and after :math:`N_k(t)` pulls of arm k:

        .. math::

           \hat{\mu}_k(t) &= \frac{X_k(t)}{N_k(t)}, \\
           U_k(t) &= \sup\limits_{q \in [a, b]} \left\{ q : \mathrm{kl}(\hat{\mu}_k(t), q) \leq \frac{\log(t) + c \log(\max(1, \log(t)))}{N_k(t)} \right\},\\
           I_k(t) &= U_k(t).

        If rewards are in :math:`[a, b]` (default to :math:`[0, 1]`) and :math:`\mathrm{kl}(x, y)` is the Kullback-Leibler divergence between two distributions of means x and y (see :mod:`Arms.kullback`),
        and c is the parameter (default to 1).
        """
        if self.pulls[arm] < 1:
            return float('+inf')
        else:
            # XXX We could adapt tolerance to the value of self.t
            return self.klucb(self.rewards[arm] / self.pulls[arm], (log(self.t) + self.c * log(max(1, log(self.t)))) / self.pulls[arm], self.tolerance)

    def computeAllIndex(self):
        """ Compute the current indexes for all arms, in a vectorized manner."""
        indexes = self.klucb(self.rewards / self.pulls, (np.log(self.t) + self.c * np.log(np.maximum(1., np.log(self.t)))) / self.pulls, self.tolerance)
        indexes[self.pulls < 1] = float('+inf')
        self.index[:] = indexes
