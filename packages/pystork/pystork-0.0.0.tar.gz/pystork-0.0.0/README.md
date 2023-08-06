[![Circle CI](https://circleci.com/gh/yassineameur/pystork/tree/master.svg?style=shield&circle-token=cafe12cef1c92e9282e2fd01dd67e68725edbf34)](https://circleci.com/gh/yassineameur/pystork/tree/master)
[![codecov](https://codecov.io/gh/yassineameur/pystork/branch/master/graph/badge.svg)](https://codecov.io/gh/yassineameur/pystork)

# pystork
Pystork is a python library that has three goals:
- Make deep learning easy to use
- Support easiy custom activation or cost functions
- Test new innovative optimization algorithms

Pystork uses `numpy` to handle vectorisation efficiently and make operations fast.

Pystork does not aim to support big data: All operations are executed on one machine.

We are currently working on phase one where the goal is to implement the most-known optimization algorithms. Once this phase tested, benshmarked and validated, we will go further and test new in-house designed optimization algorithms.

### Install pystork
 Pystork can be installed via pip
 `pip install pystork`

### Use pystork

Pystork is designed to be so easily used. We will soon create some small colab projects to give some concrete use cases.
Here is an example of how it works.

#### Build a layer
Layers in pystork support many activation functions, we have implemented until now: Relu, Tanh, Sigmoid and Softmax.

If you have another activation function that you want to use, no problem: All you need is to implement the interface `AbstractActivationFunction`
When you build a layer, you need to specify:
- The units number
- The number of units in the previous layer (If it is the first layer, this will be the number of features)
- The activation function

Example of a Relu layer with 5 units and where the previous layer has 2 units)
```
from pystork.activation import Relu
from pystork.layer import Layer

relu_layer = Layer(units_number=5, inputs_number=2, activation_function=Relu())
```

### Build a model
To build a model, you have to specify:
- The list of layer (See the section above to see how to build a layer)
- The cost function that you want to optimize. For the moment, we have built the standard cost function for a binary classifier ( 2 classes)
- The initializer: How tou want to initialize your variables; You have two implemented initializers:
    - Zeros initializers (Not recommended)
    - Random initializer: initializes parameters with small random numbers (Recommended)

Here is an example of a model for a binary classification problem, where we have a 3-dimension features, one hidden layer of 2 units, and one output layer with one unit.
```
from pystork.activation import Relu, Sigmoid
from pystork.layer import Layer
from pystork.model import Model
from pystork.initializers import RandomInitializer
from pystork.costs.binary_classfier import BinaryClassificationCost

hidden_layer = Layer(units_number=2, inputs_number=3, activation_function=Relu())
output_layer = Layer(units_number=1, inputs_number=2, activation_function=Sigmoid())

model = Model(layers=[hidden_layer, output_layer], cost_function=BinaryClassificationCost(), initializer=RandomInitializer())
```


### Fit a model
To fit a model, you have to supply:
- The training inputs: features and labels
- The optimizer
The model fitting is handled by the optimization algorithm: It will optimize the weights and the biases of layers.
In the code below, we show how an example where we use gradient descent to optimize the model. Each optimization has its own parameters.

```
from pystork.optimizers.gradient_descent import GradientDescent

# We instantiate the gradient descent
algorithm = GradientDescent(learning_rate = 0.01)
algorithm.optimize_cost(model=model, training_inputs=X, training_labels=Y)
```

After this code is executed, you model will be optimized and ready to predict.

### Predict data
In order to predict, you just need your optimized model and the data you want to predict

```
predictions = model.predict(x=data)
```

## You want to contribute ?
If you want to contribute, you are welcomed. Here is all you need to do to start developing.
- Install python 3.6.3
- Create a virtual environment
- Install pipenv
- Install dependencies: `pipenv install --dev`
- To run test: `make test`
