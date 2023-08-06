''' * @Author: romain.egele * @Date: 2018-06-21 15:31:30
'''

from collections import OrderedDict

from nas.contrib.anl_mlp_1 import create_structure
from deephyper.benchmark.candleP1B3Nas.load_data import load_data

class Problem:
    def __init__(self):
        space = OrderedDict()
        space['regression'] = True
        space['load_data'] = {
            'func': load_data,
            'kwargs' : {
                'batch_size': 100,
            }
        }

        # ARCH
        space['create_structure'] = {
            'func': create_structure,
            'kwargs': {
                'num_cells': 6
            }
        }

        # HyperParameters
        space['hyperparameters'] = {
            'eval_freq': 100,
            'batch_size': 100,
            'learning_rate': 0.01,
            'optimizer': 'adam',
            'num_epochs': 10,
            'loss_metric': 'mean_squared_error',
            'test_metric': 'mean_squared_error',
        }
        self.space = space


if __name__ == '__main__':
    instance = Problem()
