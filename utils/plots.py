import numpy as np
import matplotlib.pyplot as plt 
import utils.utils as utils

def multiBarPlot(x, y, colors, ylabel, title, legends):
    N = len(x)
    ind = np.arange(N)
    width = 1.0 / (len(y) + 1)
    fig, ax = plt.subplots()

    rects = []
    for i in range(len(y)):
        rects.append(ax.bar(ind + width * i, y[i], width, color=colors[i]))
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(x)
    ax.legend((rects[0][0], rects[1][0], rects[2][0], rects[3][0], rects[4][0]), legends)
    time = utils.get_timestamp()
    plt.savefig('{}.png'.format(title)) # + time))


def plot_learning_curve(rList):
    x = list(range(len(rList)))
    y = rList

    plt.plot(x, utils.smooth_list(y))
    plt.ylabel("Total Reward")
    plt.xlabel("Episodes")
    plt.grid(True)
    plt.title("Q-Learning Curve")

    time = utils.get_timestamp()
    plt.savefig('{}.png'.format("Q-Learning Curve")) # + time))
    plt.close()



