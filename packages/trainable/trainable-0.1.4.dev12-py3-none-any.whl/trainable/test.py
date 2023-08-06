import torch

import torch.nn as nn
from torch.utils.data import Dataset
from torch.optim import Adam


def title(title):
    s = f"# --- {title.upper()} TESTS "
    s = s + "-" * (78 - len(s)) + " #"
    print(s, flush=True)


def subtest(n, desc):
    print(f"# ({n}) {desc}: ", end='', flush=True)


def evaluate(test):
    print(end='', flush=True)
    print("PASS" if test == True else "FAIL", flush=True)


def end():
    print("# " + "-" * 76 + " #", flush=True)
    print(flush=True)


def device(device):
    return torch.device(device)


def optim(params, lr=1e-4):
    return Adam(params, lr)

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Conv2d(3, 3, kernel_size=3, padding=1)

    def forward(self, x):
        return self.net(x)


class Dataset(Dataset):
    def __init__(self, size=16, length=1000):
        super().__init__()
        self.set = torch.randn(length, 3, size, size)

    def __getitem__(self, item):
        return self.set[item]

    def __len__(self):
        return self.set.size(0)


