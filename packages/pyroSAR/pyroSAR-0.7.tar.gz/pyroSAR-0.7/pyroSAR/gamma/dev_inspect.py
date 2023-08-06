
from pyroSAR.gamma.api import isp

import inspect


def parnames(f):
    return inspect.getargspec(f)[0]


parameters = {'SLC': 'slc',
              'SLC_par': 'slc.par',
              'MLI': 'mli',
              'MLI_par': 'mli.par',
              'rlks': '4',
              'azlks': '4',
              'bullshit': 'xyz'}


def parametrize(function, parameters):
    selection = {}
    for par in parnames(function):
        if par in parameters.keys():
            selection[par] = parameters[par]
    return selection


parametrize(isp.multi_look, parameters)
