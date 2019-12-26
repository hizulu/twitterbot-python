import matplotlib.pyplot as plt
import json
import numpy as np
import threading


def text_visualisation(data):
    label, freq = zip(*data['text_result'])
    plt.rcdefaults()
    fig, ax = plt.subplots()
    y_pos = np.arange(len(label))
    ax.barh(y_pos, freq, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(label)
    ax.invert_yaxis()
    ax.set_xlabel('Word Count')
    ax.set_title('Frequent Word of Tweet about Jokowi')
    plt.show()


def hashtag_visualisation(data):
    label, freq = zip(*data['hashtag_result'])
    plt.rcdefaults()
    fig, ax = plt.subplots()
    y_pos = np.arange(len(label))
    ax.barh(y_pos, freq, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(label)
    ax.invert_yaxis()
    ax.set_xlabel('Hashtag Count')
    ax.set_title('Frequent Hahstag of Tweet about Jokowi')
    plt.show()


def souce_visualization(data):
    label, freq = zip(*data['source_result'])
    fig1, ax1 = plt.subplots()
    ax1.pie(freq, labels=label, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()


with open('result_jokowi.json', 'r') as file:
    data = json.loads(file.read())

    print('Select visualization data:')
    print('1. Tweet')
    print('2. Hashtags')
    print('3. Source')
    option = int(input("Enter your name : "))

    if(option == 1):
        text_visualisation(data)
    elif(option == 2):
        hashtag_visualisation(data)
    elif(option == 3):
        souce_visualization(data)
    else:
        exit()
