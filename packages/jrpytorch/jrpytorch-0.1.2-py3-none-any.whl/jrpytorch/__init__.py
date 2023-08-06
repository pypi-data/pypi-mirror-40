__version__ = '0.1.0'

from . import datasets
from . import visualiser
import torch
import matplotlib.pyplot as plt
import numpy as np


def vis_binary_classification(model, loss_fn, optimiser, X, y, epochs=1000):
    x_tensor = torch.tensor(X).float()
    y_tensor = torch.tensor(y.reshape(-1, 1)).float()
    plt.ion()
    min = np.min(X)-0.2
    max = np.max(X)+0.2
    x1 = np.linspace(min, max, 100)
    grid = np.array([(x, y) for x in x1 for y in x1])
    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    real_x = x1
    real_y = x1
    dx = (real_x[1]-real_x[0])/2.
    dy = (real_y[1]-real_y[0])/2.
    extent = [real_x[0]-dx, real_x[-1]+dx, real_y[0]-dy, real_y[-1]+dy]

    ax.set_xlim([min, max])
    ax.set_ylim([min, max])
    ax2.set_xlim([0, epochs])
    line1, = ax2.plot([], [], 'r-')
    # first image
    output = model(torch.from_numpy(grid).float()).detach().numpy()
    img = ax.imshow(output.reshape(100, 100), extent=extent)

    ax.scatter(X[:, 0], X[:, 1], c=y, edgecolor='black')

    losses = []

    for epoch in range(epochs):
        optimiser.zero_grad()
        output = model(x_tensor)
        loss = loss_fn(output, y_tensor)
        loss.backward()
        optimiser.step()

        losses.append(loss.item())
        if epoch == 0:
            ax2.set_ylim([0, loss.item()*1.1])

        with torch.no_grad():
            # update plot
            output = model(torch.from_numpy(grid).float())
            arr_output = output.detach().numpy().reshape(100, 100)
            img.set_data(arr_output)
            ax.set_title('Epoch: %d Loss %.3f' % (epoch + 1, loss.item()))
            line1.set_data(list(range(epoch+1)), losses)
            fig.canvas.draw()
            fig.canvas.flush_events()
    plt.ioff()
