import torch
# DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
DEVICE = torch.device('cpu')
class TorchRegressionNeuralNetwork(torch.nn.Module):

    def __init__(self, hiddenLayers: int, hiddenNodes: list, inputSize: int, maxScore=1, init=True, function='sigmoid',
                 weightsPath='weight.pkl'):
        super().__init__()
        if len(hiddenNodes) != hiddenLayers:
            Exception("size of hiddenNodes must be the same as hiddenLayers")

        self.hidden = [inputSize] + hiddenNodes + [1]
        self.layers = torch.nn.ModuleList([torch.nn.Linear(i, j) for i, j in zip(self.hidden[:-1], self.hidden[1:])])
        self.weightsPath = weightsPath
        self.functionName = function
        self.maxScore = maxScore
        functions = {'sigmoid': torch.nn.Sigmoid(), 'tanh' : torch.nn.Tanh(), 'softsign' : torch.nn.Softsign()}
        function = functions.get(self.functionName, self._error)
        self.funlist= [function] * hiddenLayers + [torch.nn.Softsign()]
        if not init:
            self.load_state_dict(torch.load(weightsPath))


    def _error(self, input):
        Exception(f"No such function name '{self.functionName}'")

    def forward(self, input):
        if not torch.is_tensor(input):
            input = torch.tensor(input, dtype=torch.float, device = DEVICE)
        for i, l in enumerate(self.layers):
            input = self.funlist[i](l(input))

        if len(input.shape) == 1:
            return input.item()
        else:
            return input



