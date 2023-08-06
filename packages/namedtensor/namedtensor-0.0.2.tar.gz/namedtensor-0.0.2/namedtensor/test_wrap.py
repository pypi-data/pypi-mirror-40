import torch.nn
from .torch_nn import _wrap

def test_linear():
    mod = nn.Linear(10, 20)
    return _wrap(mod, [("h")], [("h")])
