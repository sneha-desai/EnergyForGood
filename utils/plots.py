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
    plt.savefig('plots/{}.png'.format(title + time))

def multiBarPlot_final(x, y, colors, ylabel, title, legends):
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
    ax.legend((rects[0][0], rects[1][0], rects[2][0], rects[3][0]), legends)
    time = utils.get_timestamp()
    plt.savefig('plots/{}.png'.format(title + time))


def plot_learning_curve(rList):
    x = list(range(len(rList)))
    y = rList
    yerr = np.std(y)

    # plt.plot(x, utils.smooth_list(y))
    plt.errorbar(x, y, yerr, fmt='o', ecolor='r')
    plt.ylabel("Total Reward")
    plt.xlabel("Episodes")
    plt.grid(True)
    plt.title("Q-Learning Curve")

    time = utils.get_timestamp()
    plt.savefig('plots/{}.png'.format("Q-Learning Curve" + time))
    plt.close()


def real_time_plot(y, colors, legends, ax):
    ax.cla()
    ax.set_ylim(0,40)
    N = 1
    ind = np.arange(N)
    width = 1.0 / (5 + 1)
    rects = []

    for i in range(len(y)):
        rects.append(ax.bar(ind + width * i, y[i], width, color=colors[i]))

    ax.legend((rects[0][0], rects[1][0], rects[2][0], rects[3][0], rects[4][0]), legends)
    plt.show(False)
    plt.pause(0.00001)




