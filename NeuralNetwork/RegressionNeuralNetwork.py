import math
from random import random
from Board import Board

class RegressionNeuralNetwork:

    def __init__(self, hiddenLayers : int, hiddenNodes : list, inputSize : int, maxScore = 100,
                 init = True, function = 'sigmoid', weightsPath = 'weight.py'):
        if len(hiddenNodes) != hiddenLayers:
            Exception("size of hiddenNodes must be the same as hiddenLayers")
        self.hiddenLayers = hiddenLayers
        self.hiddenNodes = hiddenNodes
        self.inputSize = inputSize
        self.weightsPath = weightsPath
        self.functionName = function
        self.maxScore = maxScore
        functions = {'sigmoid': self._sigmoid, 'arctan' : self._tanh}
        functionDerivatives = {'sigmoid' : self._sigmoidDerivative, 'arctan' : self._tanhDerivative}
        function = functions.get(self.functionName, self._error)
        derivativeFunction = functionDerivatives.get(self.functionName, self._error)
        self.funlist= [function] * hiddenLayers + [self._specialtanH]
        self.dfunlist = [self._stanhDerivative] + [derivativeFunction] * hiddenLayers
        if init:
            self.createWeight()
            self.saveToFile()
        else:
            from NeuralNetwork.weight import weights
            self.network = weights


    def createWeight(self):
        self.network = []
        nodes = [self.inputSize] + self.hiddenNodes + [1]
        for i in range(len(nodes) - 1):
            inputs, outputs = nodes[i], nodes[i + 1]
            weights = [[random() for _ in range(inputs + 1)] for _ in range(outputs)]
            self.network.append(weights)


    def _sigmoid(self, input):
        return 1.0 / (1.0 + math.exp(-input))

    def _sigmoidDerivative(self, input):
        return input * (1.0 - input)

    def _tanh(self, input):
        return math.tanh(input)

    def _tanhDerivative(self, input):
        return 1 - (math.tanh(input))**2

    def _specialtanH(self, input):
        return self.maxScore * math.tanh(input)

    def _stanhDerivative(self, input):
        return self.maxScore * (1 - (math.tanh(input))**2)


    def _error(self, input):
        Exception(f"No such function name '{self.functionName}'")


    def saveToFile(self):
        f = open(self.weightsPath, 'w')
        f.write(f'weights = {self.network}')
        f.close()


    def predict(self, inputs):
        return self.forward_propagate(inputs)[0]


    def forward_propagate(self, inputs):
        self.output = []
        for i in range(self.hiddenLayers + 1):
            # print(self.network[i])
            inputs = [self.funlist[i](self._sumWeights(neuron, inputs)) for neuron in self.network[i]]
            self.output.append(inputs)
        return inputs


    def _sumWeights(self, inputs, weights):
        activation = weights[-1] # add bias
        for i in range(len(weights) - 1):
            activation += weights[i] * inputs[i]
        return activation


    def updateNetwork(self, train, result, l_rate):
        self._train_network(train, result, l_rate)

    def _train_network(self, train, result, l_rate):
        train = [Board.convert(board) for board in train]
        self.error_delta = []
        for i in range(len(train)):
            output = self.predict(train[i])
            self._backPropogate(result[i], i)
            self._update_weights(train[i], l_rate)


    def _backPropogate(self, expected, no_trained):
        for i in range(self.hiddenLayers, -1, -1):
            layer = self.network[i]
            errors = []
            if i == len(self.network) - 1:
                for j in range(len(layer)):
                    errors.append(expected - self.output[i][j])
            else:
                for j in range(len(layer)):
                    error = 0.0
                    for neuron in self.network[i + 1]:
                        for k in range(len(self.error_delta[self.hiddenLayers - (i + 1)])):
                            error += (neuron[j] * self.error_delta[self.hiddenLayers - (i + 1)][k])
                    errors.append(error)

            error = [errors[k] * self.dfunlist[i](self.output[i][k]) for k in range(len(layer))]
            if bool(no_trained):
                self._averageDelta(error, no_trained, i)
            else:
                self.error_delta.append(error)


    def _averageDelta(self, error, no_trained, i):
        row = self.error_delta[self.hiddenLayers - i]
        for i in range(len(row)):
            row[i] = row[i] + (error[i] - row[i])/(no_trained + 1)


    # Update network weights with error
    def _update_weights(self, inputs, l_rate):
        for i in range(self.hiddenLayers + 1):
            if i != 0:
                inputs = self.output[i][:-1]
            for neuron in self.network[i]:
                for j in range(len(inputs)):
                    for k in range(len(self.error_delta[self.hiddenLayers - (i + 1)])):
                        neuron[j] += l_rate * self.error_delta[self.hiddenLayers - (i + 1)][k] * inputs[j]
                neuron[-1] += l_rate * self.error_delta[self.hiddenLayers - (i + 1)][-1]


