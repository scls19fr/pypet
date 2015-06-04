__author__ = 'Henri Bunting'

import sys

import numpy as np
if (sys.version_info < (2, 7, 0)):
    import unittest2 as unittest
else:
    import unittest

from pypet.parameter import PickleParameter, ArrayParameter, SparseParameter
from brian2.units.stdunits import mV, mA, kHz,ms
from pypet.tests.unittests.parameter_test import ParameterTest, ResultTest
from pypet.tests.testutils.ioutils import parse_args, run_suite
from pypet.brian2.parameter import Brian2Parameter
from pypet.utils.explore import cartesian_product

import logging
logging.basicConfig(level=logging.DEBUG)


class Brian2ParameterTest(ParameterTest):

    '''
    def __init__(self, other):
        self.data = {}
        super(Brian2ParameterTest,self).__init__()
    '''

    def setUp(self):

        if not hasattr(self,'data'):
            self.data = {}

        self.data['mV1'] = 1*mV
        self.data['ampere1'] = 1*mA
        self.data['msecond17'] = 16*ms
        self.data['kHz05'] = 0.5*kHz
        self.data['b2a'] = np.array([1., 2.]) * mV

        super(Brian2ParameterTest, self).setUp()


    def make_params(self):
        self.param = {}
        for key, val in self.data.items():
            self.param[key] = Brian2Parameter(self.location+'.'+key, val, comment=key)



    def explore(self):
        self.explore_dict=cartesian_product({'npstr': [np.array(['Uno', 'Dos', 'Tres']),
                                                       np.array(['Cinco', 'Seis', 'Siette']),
                                                       np.array(['Ocho', 'Nueve', 'Diez'])],
                                             'val0': [1, 2, 3],
                                             'mV1': [42.0*mV, 3*mV, 4*mV],
                                             'b2a': np.array([1., 2.]) * mV})
        #print self.explore_dict




        ## Explore the parameter:
        for key, vallist in self.explore_dict.items():
            self.param[key]._explore(vallist)
            self.assertTrue(self.param[key].v_explored and self.param[key].f_has_range())

    pass

class Brian2ParameterSupportsTest(Brian2ParameterTest):

    tags = 'unittest', 'brian2', 'parameter', 'supports', 'henri'

    def make_params(self):
        self.param = {}
        for key, val in self.data.items():
            self.param[key] = Brian2Parameter(self.location+'.'+key, val, comment=key)
            self.param[key].v_storage_mode = Brian2Parameter.FLOAT_MODE

class Brian2ParameterDuplicatesInStoreTest(Brian2ParameterTest):

    tags = 'unittest', 'brian2', 'parameter', 'store', 'henri'

    def setUp(self):
        self.data = {}
        self.data['b2dupa'] = np.array([1., 2.]) * mV
        self.data['b2dupb'] = np.array([3., 4.]) * mV

        super(Brian2ParameterTest, self).setUp()

    def make_params(self):
        self.param = {}
        for key, val in self.data.items():
            self.param[key] = Brian2Parameter(self.location+'.'+key, val, comment=key)

    def explore(self):
        print("~~~ Brian2ParameterDuplicatesInStoreTest explore START ~~~")
        import itertools
        for element in itertools.product([np.array([1., 2.]) * mV, np.array([3., 4.]) * mV]):
            print element
        self.explore_dict = cartesian_product({'b2dupa': np.array([1., 2.]) * mV, 'b2dupb': np.array([3., 4.]) * mV})

        print(self.explore_dict)


        ## Explore the parameter:
        for key, vallist in self.explore_dict.items():
            self.param[key]._explore(vallist)
            self.assertTrue(self.param[key].v_explored and self.param[key].f_has_range())

        print("~~~ Brian2ParameterDuplicatesInStoreTest explore END ~~~")

    '''
    def test_storage_and_loading(self):
        print("~~~Brian2ParameterDuplicatesInStoreTest test_storage_and_loading~~~")

        for key, param in self.param.items():
            store_dict = param._store()

            # Due to smart storing the storage dict should be small and only contain 5 items or less
            # 1 for data, 1 for reference, and 3 for the array/matrices/items
            if param.f_has_range():
                if isinstance(param,(ArrayParameter, PickleParameter)) and \
                        not isinstance(param, SparseParameter):
                    self.assertTrue(len(store_dict)<7)
                # For sparse parameter it is more:
                if isinstance(param, SparseParameter):
                    self.assertTrue(len(store_dict)<23)



            constructor = param.__class__

            param.f_unlock()
            param.f_empty()

            param = constructor('')

            param._load(store_dict)

            param._rename(self.location+'.'+key)

            self.param[key] = param


        self.test_the_insertion_made_implicetly_in_setUp()

        self.test_exploration()

        self.test_meta_settings()
    '''



if __name__ == '__main__':
    opt_args = parse_args()
    run_suite(**opt_args)
