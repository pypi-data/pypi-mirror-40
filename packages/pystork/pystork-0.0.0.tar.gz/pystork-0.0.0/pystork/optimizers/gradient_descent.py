"""
This file contains the code for a gradient descent optimizer
"""
from math import floor
from typing import List, Tuple

import numpy as np

from pystork.model import Model
from pystork.optimizers.abstract_optimizer import AbstractOptimizer
from pystork import helpers


class MiniBatchGradientDescent(AbstractOptimizer):

    def __init__(
        self,
        iterations_number: int = 1000,
        mini_batch_size: int = 64,
        learning_rate: float = 0.1,
        print_cost: bool = True,
    ):

        self.iterations_number = iterations_number
        self.learning_rate = learning_rate
        self.print_cost = print_cost
        self.mini_batch_size = mini_batch_size

    def optimize_cost(
        self, model: Model, training_inputs: np.array, training_labels: np.array
    ) -> List[float]:

        self.check_dimensions(model, training_inputs, training_labels)
        model.initialize_layers()
        training_inputs = model.normalize_inputs(training_inputs)
        shuffled_training_inputs, shuffled_training_labels = helpers.shuffle_data(
            training_inputs, training_labels
        )

        costs = []

        for i in range(self.iterations_number):
            self._execute_one_iteration(
                model, shuffled_training_inputs, shuffled_training_labels
            )
            cost = model.last_cost_computation
            costs.append(cost)

            for layer in model.layers:
                assert layer.W is not None and layer.layer_cache.d_W is not None
                assert layer.b is not None and layer.layer_cache.d_b is not None
                new_W = layer.W - self.learning_rate * layer.layer_cache.d_W
                new_b = layer.b - self.learning_rate * layer.layer_cache.d_b
                layer.set_parameters(new_W, new_b)

            if i % 100 == 0 and self.print_cost:
                print("Iteration {}, cost = {}".format(i, cost))
        if self.print_cost:
            print("Final cost = {}".format(costs[-1]))
        return costs

    def _get_minibatches(
        self, training_inputs: np.array, training_labels: np.array
    ) -> List[Tuple[np.array, np.array]]:
        """
        :return: A list of mini batches on which we will iterate.
        Each element is a tuple of inputs and labels
        """
        complete_mini_batches_number = floor(
            training_inputs.shape[1] / self.mini_batch_size
        )
        mini_batches = []

        for k in range(complete_mini_batches_number):

            mini_batch_indexes = range(
                k * self.mini_batch_size, (k + 1) * self.mini_batch_size
            )
            mini_batch_X = training_inputs[:, mini_batch_indexes]
            mini_batch_Y = training_labels[:, mini_batch_indexes]

            mini_batches.append((mini_batch_X, mini_batch_Y))

        if training_inputs.shape[1] % complete_mini_batches_number != 0:
            mini_batch_indexes = range(
                complete_mini_batches_number * self.mini_batch_size,
                training_inputs.shape[1],
            )
            mini_batch_X = training_inputs[:, mini_batch_indexes]
            mini_batch_Y = training_labels[:, mini_batch_indexes]
            mini_batches.append((mini_batch_X, mini_batch_Y))

        return mini_batches

    def _execute_one_iteration(
        self, model: Model, training_inputs: np.array, training_labels: np.array
    ):

        for (mini_batch_X, mini_batch_Y) in self._get_minibatches(
            training_inputs, training_labels
        ):

            model.execute_forward_propagation(mini_batch_X, mini_batch_Y)
            model.execute_backward_propagation(training_labels=mini_batch_Y)


class GradientDescent(MiniBatchGradientDescent):
    def __init__(
        self,
        iterations_number: int = 1000,
        learning_rate: float = 0.1,
        print_cost: bool = True,
    ):
        # The size of minibatch will be set automatically when we optimize
        super().__init__(
            iterations_number=iterations_number,
            mini_batch_size=0,
            learning_rate=learning_rate,
            print_cost=print_cost,
        )

    def optimize_cost(
        self, model: Model, training_inputs: np.array, training_labels: np.array
    ) -> List[float]:
        self.mini_batch_size = training_inputs.shape[1]

        return super().optimize_cost(model, training_inputs, training_labels)
