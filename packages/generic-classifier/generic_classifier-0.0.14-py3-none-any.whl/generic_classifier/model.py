from wisepy.talking import Talking
from Redy.Tools.PathLib import Path
import numpy as np
import torch
import os
import re
try:
    from .utils import and_then, img_scale, img_redim, dump_model, load_model, read_directory
except:
    from utils import and_then, img_scale, img_redim, dump_model, load_model, read_directory

cmd = Talking()
D = torch.autograd.grad


def var(v):
    return torch.autograd.Variable(v, requires_grad=True)


def val(v):
    return torch.autograd.Variable(v, requires_grad=False)


class ConvStack(torch.nn.Module):
    def __init__(self, input_dims, pipeline=((12, 2), (8, 3), (16, 3))):
        super(ConvStack, self).__init__()
        filters, w, h = input_dims
        layers = []
        for (next_filters, stride) in pipeline:
            layers.append(torch.nn.Conv2d(filters, next_filters, stride))
            filters = next_filters
            w -= stride - 1
            h -= stride - 1
            layers.append(torch.nn.MaxPool2d(2, stride=2))
            w //= 2
            h //= 2
            layers.append(torch.nn.Dropout(0.3))

        self.layer = torch.nn.Sequential(*layers)
        self.dims = (filters, w, h)

    def forward(self, x):
        return self.layer(x)


class Mapper:
    def __init__(self, source):
        self.source = source

    def to_long(self, search_name):
        return next(long for name, long in self.source if name == search_name)

    def to_name(self, search_long):
        return next(name for name, long in self.source if long == search_long)


class SSP(torch.nn.Module):
    def __init__(self,
                 input_dims,
                 categories=2,
                 mapper: Mapper = None,
                 use_cuda=True):
        super(SSP, self).__init__()
        self.ssp = ConvStack(input_dims)
        filters, w, h = self.ssp.dims
        dim = filters * w * h
        self.predictor = torch.nn.Sequential(
            torch.nn.Linear(dim, dim // 2),
            torch.nn.ReLU(),
            torch.nn.Linear(dim // 2, categories),
        )
        self.mapper = mapper
        self.use_cuda = use_cuda
        if use_cuda:
            self.cuda()

    def set_mapper(self, mapper):
        self.mapper = mapper

    def forward(self, x):
        x = self.ssp(x)
        x = (lambda v: v.view(v.shape[0], -1))(x)
        x = self.predictor(x)
        return x

    def fit(self, samples, labels, lr=1e-3, epochs=100):
        labels = val(torch.from_numpy(labels).long())
        samples = val(torch.from_numpy(samples).float())
        if self.use_cuda:
            labels = labels.cuda()
            samples = samples.cuda()

        optimizer = torch.optim.Adam(self.parameters(), lr=lr)
        criterion = torch.nn.CrossEntropyLoss()

        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = self(samples)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            print('Epoch [%d/%d], Loss: %s' % (epoch + 1, epochs, str(loss)))

        return loss.cpu().data.numpy().flatten()[0]

    def predict_with_names(self, samples):
        mapper = self.mapper
        return [((lambda x: x) if not mapper else mapper.to_name)(each)
                for each in self.predict(samples)]

    def predict(self, samples):
        samples = val(torch.from_numpy(samples).float())
        if self.use_cuda:
            samples = samples.cuda()
        return np.argmax(self(samples).cpu().data.numpy(), axis=1)


# net = SSP((3, 51, 51)).cuda()
#
# x1 = np.random.sample((30, 3, 51, 51)) + 2
# y1 = np.repeat(0, 30)
# x2 = np.random.sample((30, 3, 51, 51))
# y2 = np.repeat(1, 30)
#
# net.fit(np.vstack((x1, x2)), np.hstack((y1, y2)), epochs=100)
# print(net.predict(x1))
# print(net.predict(x2))


def make_data(X, y, size):
    filters, w, h = size
    size = w, h
    X = np.array([img_redim(img_scale(x, size)) for x in X])
    X = X / 255.0

    def batch(batch_size=50):
        batch_size = min(batch_size, len(X))
        while True:
            ids = np.random.permutation(len(X))[:batch_size]
            yield X[ids], y[ids]

    return X, batch


@cmd
def get_module(indir: str,
               outdir: str,
               size,
               md_name='mml',
               new=False,
               lr='0.0001',
               minor_epoch='50',
               batch_size='80',
               epoch='15'):
    try:
        if new:
            raise Exception
        return load_model(f'{outdir}/{md_name}')
    except:
        ssp = None
        pass

    size, batch_size, epoch, minor_epoch, lr = map(eval, (size, batch_size, epoch, minor_epoch, lr))
    matcher = re.compile('cls_(.+)')

    cls = []
    X = []
    y = []
    for each in os.listdir(indir):
        m = matcher.match(each)
        if not m:
            continue
        name = m.groups()[0]

        long = len(cls)
        cls.append((name, long))
        x, y_ = read_directory(f'{indir}/cls_{name}', long)
        X += x
        y.append(y_)

    mapper = Mapper(cls)
    if ssp is None:
        ssp = SSP(size, categories=len(cls), mapper=mapper)

    print('training data loaded...')
    y = np.hstack(y)
    X, data_helper = make_data(X, y, size)
    i = 0
    print('data preprocessed.')
    try:
        for batch_x, batch_y in data_helper(batch_size):
            i += 1
            if i > epoch:
                break
            loss = ssp.fit(batch_x, batch_y, epochs=minor_epoch, lr=lr)
            if loss == .0:
                break
    except KeyboardInterrupt:
        pass
    dump_model(ssp, f'{outdir}/{md_name}')
    dump_model(ssp, f'{outdir}/{md_name}')
    from sklearn.metrics.classification import classification_report, confusion_matrix
    pred = ssp.predict(X)
    print(classification_report(y.flatten(), pred))
    print(confusion_matrix(y.flatten(), pred))
    return ssp


def run():
    cmd.on()


# get_module('./../test', './../test', '3, 200, 200')
