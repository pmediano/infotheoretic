__author__ = 'juancarlosfarah'

import pymongo
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as spi
from copy import deepcopy


def connect(database):
    host = "localhost"
    port = 27017
    mc = pymongo.MongoClient(host=host, port=port)
    return mc.get_database(database)


def plot_one(threshold):
    db = connect("individual_project")

    cursor = db.oscillator_simulation.find({"threshold": threshold})

    beta = []
    global_sync = []
    integrated_information = []

    for doc in cursor:
        beta.append(doc['beta'])
        global_sync.append(doc['global_sync'])
        integrated_information.append(doc['integrated_information_e'])

    fig = plt.figure()
    plt.scatter(global_sync, integrated_information)
    plt.xlabel("Global Synchrony")
    plt.ylabel("Integrated Information Empirical")
    plt.title("Integrated Information Empirical over Global Synchrony\n" +
              "Threshold = " + str(threshold))
    plt.show(fig)

    fig = plt.figure()
    plt.scatter(beta, integrated_information)
    plt.xlabel("Beta")
    plt.ylabel("Integrated Information Empirical")
    plt.title("Integrated Information Empirical over Beta\n" +
              "Threshold = " + str(threshold))
    plt.show(fig)

    return


def plot(phi="integrated_information_e",
         save=False,
         path="$HOME",
         ext="svg",
         query=None):
    db = connect("individual_project")

    duration = "Various"

    if "duration" in query:
        duration = query['duration']

    if not query:
        query = dict()

    q1 = deepcopy(query)
    q1['threshold'] = 0.9

    q2 = deepcopy(query)
    q2['threshold'] = 0.8

    q3 = deepcopy(query)
    q3['threshold'] = 0.7

    q4 = deepcopy(query)
    q4['threshold'] = 0.6

    q5 = deepcopy(query)
    q5['threshold'] = 0.5

    cursors = {
        "0.9": db.oscillator_simulation.find(q1),
        "0.8": db.oscillator_simulation.find(q2),
        "0.7": db.oscillator_simulation.find(q3),
        "0.6": db.oscillator_simulation.find(q4),
        "0.5": db.oscillator_simulation.find(q5)
    }

    beta = dict()
    global_sync = dict()
    integrated_information = dict()
    phi_e_tilde = dict()
    coalition_entropy = dict()
    chi = dict()
    lamda = dict()

    colors = {
        "0.9": "orange",
        "0.8": "red",
        "0.7": "blue",
        "0.6": "green",
        "0.5": "purple"
    }

    for key in cursors:
        beta[key] = []
        global_sync[key] = []
        chi[key] = []
        lamda[key] = []
        integrated_information[key] = []
        coalition_entropy[key] = []
        phi_e_tilde[key] = []
        for doc in cursors[key]:
            beta[key].append(doc['beta'])
            global_sync[key].append(doc['global_sync'])
            lamda[key].append(doc['lambda'])
            chi[key].append(doc['chi'])
            integrated_information[key].append(doc[phi])
            coalition_entropy[key].append(doc['coalition_entropy'])
            phi_e_tilde[key].append(doc['integrated_information_e_tilde'])

    fig = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Global Synchrony")
        plt.ylabel("Integrated Information Empirical")
        plt.title("Integrated Information Empirical vs Global Synchrony\n"
                  "Duration = " + str(duration) + ", Tau = 1")
        handles.append(plt.scatter(global_sync[key],
                                   integrated_information[key],
                                   color=colors[key],
                                   label=key))
    plt.legend(handles, labels, title="Threshold")

    if save:
        fig.savefig(path + "1." + ext)
    else:
        plt.show(fig)

    fig = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Beta")
        plt.ylabel("Integrated Information Empirical")
        plt.title("Integrated Information Empirical vs Beta\n"
                  "Duration = " + str(duration) + ", Tau = 1")
        handles.append(plt.scatter(beta[key],
                                   integrated_information[key],
                                   color=colors[key],
                                   label=key))
    plt.legend(handles, labels, title="Threshold")

    if save:
        fig.savefig(path + "2." + ext)
    else:
        plt.show(fig)

    fig = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Beta")
        plt.ylabel("Chi")
        plt.title("Chi vs Beta\n"
                  "Duration = " + str(duration) + ", Tau = 1")
        handles.append(plt.scatter(beta[key],
                                   chi[key],
                                   color=colors[key],
                                   label=key))
    plt.legend(handles, labels, title="Threshold")

    if save:
        fig.savefig(path + "3." + ext)
    else:
        plt.show(fig)

    fig = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Beta")
        plt.ylabel("Lambda")
        plt.title("Lambda vs Beta\n"
                  "Duration = " + str(duration) + ", Tau = 1")
        handles.append(plt.scatter(beta[key],
                                   lamda[key],
                                   color=colors[key],
                                   label=key))
    plt.legend(handles, labels, title="Threshold")

    if save:
        fig.savefig(path + "4." + ext)
    else:
        plt.show(fig)

    fig = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Chi")
        plt.ylabel("Integrated Information Empirical")
        plt.title("Integrated Information Empirical vs Chi\n"
                  "Duration = " + str(duration) + ", Tau = 1")
        handles.append(plt.scatter(chi[key],
                                   integrated_information[key],
                                   color=colors[key],
                                   label=key))
    plt.legend(handles, labels, title="Threshold")

    if save:
        fig.savefig(path + "5." + ext)
    else:
        plt.show(fig)

    fig = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Lambda")
        plt.ylabel("Integrated Information Empirical")
        plt.title("Integrated Information Empirical vs Lambda\n"
                  "Duration = " + str(duration) + ", Tau = 1")
        handles.append(plt.scatter(lamda[key],
                                   integrated_information[key],
                                   color=colors[key],
                                   label=key))
    plt.legend(handles, labels, title="Threshold")

    if save:
        fig.savefig(path + "6." + ext)
    else:
        plt.show(fig)

    fig = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Beta")
        plt.ylabel("Coalition Entropy")
        plt.title("Coalition Entropy vs Beta\n"
                  "Duration = " + str(duration) + ", Tau = 1")
        handles.append(plt.scatter(beta[key],
                                   coalition_entropy[key],
                                   color=colors[key],
                                   label=key))
    plt.legend(handles, labels, title="Threshold")

    if save:
        fig.savefig(path + "7." + ext)
    else:
        plt.show(fig)

    fig = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Coalition Entropy")
        plt.ylabel("Integrated Information Empirical")
        plt.title("Integrated Information Empirical vs Coalition Entropy\n"
                  "Duration = " + str(duration) + ", Tau = 1")
        handles.append(plt.scatter(coalition_entropy[key],
                                   integrated_information[key],
                                   color=colors[key],
                                   label=key))
    plt.legend(handles, labels, title="Threshold")

    if save:
        fig.savefig(path + "8." + ext)
    else:
        plt.show(fig)

    fig = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Integrated Information Empirical Tilde")
        plt.ylabel("Integrated Information Empirical")
        plt.title("Integrated Information Empirical vs "
                  "Integrated Information Empirical Tilde\n"
                  "Duration = " + str(duration) + ", Tau = 1")
        handles.append(plt.scatter(phi_e_tilde[key],
                                   integrated_information[key],
                                   color=colors[key],
                                   label=key))
    plt.legend(handles, labels, title="Threshold")

    if save:
        fig.savefig(path + "9." + ext)
    else:
        plt.show(fig)

    plt.close()

    return


def plot_curves():
    db = connect("individual_project")

    cursors = {
        "0.9": db.oscillator_simulation.find({"threshold": 0.9}),
        "0.8": db.oscillator_simulation.find({"threshold": 0.8}),
        "0.7": db.oscillator_simulation.find({"threshold": 0.7}),
        "0.6": db.oscillator_simulation.find({"threshold": 0.6}),
        "0.5": db.oscillator_simulation.find({"threshold": 0.5})
    }

    beta = dict()
    global_sync = dict()
    integrated_information = dict()
    chi = dict()
    lamda = dict()

    colors = {
        "0.9": "orange",
        "0.8": "red",
        "0.7": "blue",
        "0.6": "green",
        "0.5": "purple"
    }

    for key in cursors:
        beta[key] = []
        global_sync[key] = []
        chi[key] = []
        lamda[key] = []
        integrated_information[key] = []
        for doc in cursors[key]:
            beta[key].append(doc['beta'])
            global_sync[key].append(doc['global_sync'])
            lamda[key].append(doc['lambda'])
            chi[key].append(doc['chi'])
            integrated_information[key].append(doc['integrated_information_e'])

    fig2 = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Beta")
        plt.ylabel("Integrated Information Empirical")
        plt.title("Integrated Information Empirical over Beta")
        x = beta[key]
        y = integrated_information[key]

        # Combine lists into list of tuples.
        points = zip(x, y)

        # Sort list of tuples by x-value.
        points = sorted(points, key=lambda point: point[0])

        # Split list of tuples into two list of x values any y values.
        x, y = zip(*points)

        # Plot original points.
        plt.plot(x, y, 'ro', color=colors[key], label=key)

        x_new = np.linspace(min(x), max(x), 200)
        spline = spi.InterpolatedUnivariateSpline(x, y)
        spline.set_smoothing_factor(0.15)

        handles.append(plt.plot(x_new,
                                spline(x_new),
                                color=colors[key],
                                label=key))
    plt.ylim(-0.5, 1)
    plt.legend(handles, labels, title="Threshold")
    plt.show(fig2)

    fig3 = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Chi")
        plt.ylabel("Integrated Information Empirical")
        plt.title("Integrated Information Empirical over Chi")
        x = chi[key]
        y = integrated_information[key]

        # Combine lists into list of tuples.
        points = zip(x, y)

        # Sort list of tuples by x-value.
        points = sorted(points, key=lambda point: point[0])

        # Split list of tuples into two list of x values any y values.
        x, y = zip(*points)

        # Plot original points.
        plt.plot(x, y, 'ro', color=colors[key], label=key)

        x_new = np.linspace(min(x), max(x), 200)
        spline = spi.InterpolatedUnivariateSpline(x, y)
        spline.set_smoothing_factor(1.1)

        handles.append(plt.plot(x_new,
                                spline(x_new),
                                color=colors[key],
                                label=key))
    plt.ylim(-0.5, 1)
    plt.legend(handles, labels, title="Threshold")
    plt.show(fig3)

    fig4 = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Lambda")
        plt.ylabel("Integrated Information Empirical")
        plt.title("Integrated Information Empirical over Lambda")
        x = lamda[key]
        y = integrated_information[key]

        # Combine lists into list of tuples.
        points = zip(x, y)

        # Sort list of tuples by x-value.
        points = sorted(points, key=lambda point: point[0])

        # Split list of tuples into two list of x values any y values.
        x, y = zip(*points)

        # Plot original points.
        plt.plot(x, y, 'ro', color=colors[key], label=key)

        x_new = np.linspace(min(x), max(x), 200)
        spline = spi.InterpolatedUnivariateSpline(x, y)
        spline.set_smoothing_factor(1.1)

        handles.append(plt.plot(x_new,
                                spline(x_new),
                                color=colors[key],
                                label=key))
    plt.ylim(-0.5, 1)
    plt.legend(handles, labels, title="Threshold")
    plt.show(fig4)

    fig5 = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Global Synchrony")
        plt.ylabel("Integrated Information Empirical")
        plt.title("Integrated Information Empirical over Global Synchrony")
        x = global_sync[key]
        y = integrated_information[key]

        # Combine lists into list of tuples.
        points = zip(x, y)

        # Sort list of tuples by x-value.
        points = sorted(points, key=lambda point: point[0])

        # Split list of tuples into two list of x values any y values.
        x, y = zip(*points)

        # Plot original points.
        plt.plot(x, y, 'ro', color=colors[key], label=key)

        x_new = np.linspace(min(x), max(x), 200)
        spline = spi.InterpolatedUnivariateSpline(x, y)
        spline.set_smoothing_factor(0.2)

        handles.append(plt.plot(x_new,
                                spline(x_new),
                                color=colors[key],
                                label=key))
    plt.ylim(-0.5, 1)
    plt.legend(handles, labels, title="Threshold")
    plt.show(fig5)


if __name__ == "__main__":
    q = {
        "duration": 5000
    }

    plot(phi="integrated_information_e",
         save=True,
         path="/Users/juancarlosfarah/Git/infotheoretic/docs/phi_e/",
         ext="svg",
         query=q)
    plot(phi='integrated_information_e_tilde',
         save=True,
         path="/Users/juancarlosfarah/Git/infotheoretic/docs/phi_e_tilde/",
         ext="svg",
         query=q)
    # plot_curves()