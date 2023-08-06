'''
 * @Author: romain.egele, dipendra.jha
 * @Date: 2018-06-21 15:31:30
'''

from collections import OrderedDict
from nas.cell.structure import create_sequential_structure
from nas.cell.mlp import create_dense_cell_example
from deephyper.benchmark.candleNT3Nas.load_data import load_data

class Problem:
    def __init__(self):
        space = OrderedDict()
        space['num_outputs'] = 2
        space['regression'] = False
        space['load_data'] = {
            'func': load_data
        }

        # ARCH
        space['num_cells'] = 2
        space['create_structure'] = {
            'func': create_sequential_structure,
            'kwargs': {
                'num_cells': 2
            }
        }
        space['create_cell'] = {
            'func': create_dense_cell_example
        }

        # HyperParameters
        space['hyperparameters'] = {'batch_size': 64,
                                    'activation': 'relu',
                                    'learning_rate': 0.0001,
                                    'optimizer': 'adam',
                                    'num_epochs': 10,
                                    'loss_metric': 'softmax_cross_entropy',
                                    'test_metric': 'accuracy',
                                    'eval_freq': 1
                                }
        self.space = space


if __name__ == '__main__':
    instance = Problem()
