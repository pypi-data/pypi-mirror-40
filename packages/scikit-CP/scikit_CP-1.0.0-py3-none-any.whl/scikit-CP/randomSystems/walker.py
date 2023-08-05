#   File: walker.py
#   Author: Nawaf Abdullah
#   Creation Date: 19/Mar/2018
#   Description: Modeling of the random walker problem in 1D, 2D and 3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from itertools import count
import numpy as np


class Walker:
    _ids = count(0)
    g_visited = []

    def __init__(self, xi=0, yi=0, zi=0, i_key=None):
        """
        :param xi: initial x position
        :param yi: initial y position
        :param zi: initial z position
        :param i_key: instance identification key
        """
        self.id = next(self._ids)
        self.z_switch = False
        self.x = [xi]
        self.y = [yi]
        self.z = [zi]
        if i_key is None:
            self.key = "walker " + str(self.id)
        else:
            if isinstance(i_key, str):
                self.key = i_key
            else:
                raise TypeError("Key value must be a string type")

    def reset(self):
        """
        Resets the walker's path
        """
        del self.x[:]
        del self.y[:]
        del self.z[:]

    def walk_1d(self, num_steps):
        """
        Calculates the walker path in 1D over time steps
            - In this method, the y-axis (self.y) is used as a time axis
        :param num_steps: number of steps
        :return: the walker path (self.x) vs time (self.y)
        """
        for i in range(num_steps - 1):
            r = random.randint(0, 100)
            if r > 50:
                self.x.append(self.x[i] + 1)
            else:
                self.x.append(self.x[i] - 1)
            self.y.append(self.y[i] + 1)
        self.z_switch = False
        return self.x, self.y

    def walk_2d(self, num_steps):
        """
        Calculates the walker path in 2D
        :param num_steps: number of steps
        :return: the walker path in 2D: self.x, self.y
        """
        for i in range(num_steps-1):
            r = random.randint(0, 100)
            if r <= 25:
                self.x.append(self.x[i] + 1)
                self.y.append(self.y[i])
            elif 25 < r <= 50:
                self.x.append(self.x[i] - 1)
                self.y.append(self.y[i])
            elif 50 < r <= 75:
                self.y.append(self.y[i] + 1)
                self.x.append(self.x[i])
            else:
                self.y.append(self.y[i] - 1)
                self.x.append(self.x[i])
        self.z_switch = False
        return self.x, self.y

    def saw_2d(self, num_steps, avoid_all=False):
        """
        Calculates self avoiding walker path in 2D
        :param num_steps: number of steps
        :param avoid_all: Enables/disables avoiding the paths of other walker instances, as opposed to just self-avoid
        :return: the walker path in 2D: self.x, self.y
        """

        if avoid_all is True:
            visited = self.g_visited
        else:
            visited = []
        for i in range(num_steps - 1):
            r = random.randint(0, 100)
            if r <= 25:
                if (self.x[i] + 1, self.y[i]) in visited:
                    self.x.append(self.x[i])
                    self.y.append(self.y[i])
                    continue
                else:
                    self.x.append(self.x[i] + 1)
                    self.y.append(self.y[i])
                    visited.append((self.x[i] + 1, self.y[i]))
            elif 25 < r <= 50:
                if (self.x[i] - 1, self.y[i]) in visited:
                    self.x.append(self.x[i])
                    self.y.append(self.y[i])
                    continue
                else:
                    self.x.append(self.x[i] - 1)
                    self.y.append(self.y[i])
                    visited.append((self.x[i] - 1, self.y[i]))
            elif 50 < r <= 75:
                if (self.x[i], self.y[i] + 1) in visited:
                    self.x.append(self.x[i])
                    self.y.append(self.y[i])
                    continue
                else:
                    self.y.append(self.y[i] + 1)
                    self.x.append(self.x[i])
                    visited.append((self.x[i], self.y[i] + 1))
            else:
                if (self.x[i], self.y[i] - 1) in visited:
                    self.x.append(self.x[i])
                    self.y.append(self.y[i])
                    continue
                else:
                    self.y.append(self.y[i] - 1)
                    self.x.append(self.x[i])
                    visited.append((self.x[i], self.y[i] - 1))
        if avoid_all is True:
            self.g_visited = visited
        self.z_switch = False
        print(len(self.x), len(self.y))
        return self.x, self.y

    def walk_3d(self, num_steps):
        """
        Calculates the walker path in 3D
        :param num_steps: number of steps
        :return: the walker path in 3D: self.x, self.y, self.z
        """
        for i in range(num_steps-1):
            r = random.randint(0, 100)
            if r <= 16.66:
                self.x.append(self.x[i] + 1)
                self.y.append(self.y[i])
                self.z.append(self.z[i])
            elif 16.66 < r <= 33.32:
                self.x.append(self.x[i] - 1)
                self.y.append(self.y[i])
                self.z.append(self.z[i])
            elif 33.32 < r <= 49.98:
                self.y.append(self.y[i] + 1)
                self.x.append(self.x[i])
                self.z.append(self.z[i])
            elif 49.98 < r <= 66.64:
                self.y.append(self.y[i] - 1)
                self.x.append(self.x[i])
                self.z.append(self.z[i])
            elif 66.64 < r < 83.33:
                self.z.append(self.z[i] + 1)
                self.x.append(self.x[i])
                self.y.append(self.y[i])
            else:
                self.z.append(self.z[i] - 1)
                self.x.append(self.x[i])
                self.y.append(self.y[i])
        self.z_switch = True
        return self.x, self.y, self.z

    def saw_3d(self, num_steps, avoid_all):
        """
        Calculates self avoiding walker path in 3D
        :param num_steps: number of steps
        :param avoid_all: Enables/disables avoiding the paths of other walker instances, as opposed to just self-avoid
        :return: the walker path in 3D: self.x, self.y, self.z
        """

        if avoid_all is True:
            visited = self.g_visited
        else:
            visited = []

        for i in range(num_steps-1):
            r = random.randint(0, 100)
            # -------------------------- +X --------------------------#
            if r <= 16.66:
                if (self.x[i] + 1, self.y[i], self.z[i]) in visited:
                    self.x.append(self.x[i])
                    self.y.append(self.y[i])
                    self.z.append(self.z[i])
                    continue
                else:
                    self.x.append(self.x[i] + 1)
                    self.y.append(self.y[i])
                    self.z.append(self.z[i])
                    visited.append((self.x[i] + 1, self.y[i], self.z[i]))
            # -------------------------- -X --------------------------#
            elif 16.66 < r <= 33.32:
                if (self.x[i] - 1, self.y[i], self.z[i]) in visited:
                    self.x.append(self.x[i])
                    self.y.append(self.y[i])
                    self.z.append(self.z[i])
                    continue
                else:
                    self.x.append(self.x[i] - 1)
                    self.y.append(self.y[i])
                    self.z.append(self.z[i])
                    visited.append((self.x[i] - 1, self.y[i], self.z[i]))
            # -------------------------- +Y --------------------------#
            elif 33.32 < r <= 49.98:
                if (self.x[i], self.y[i] + 1, self.z[i]) in visited:
                    self.y.append(self.y[i])
                    self.x.append(self.x[i])
                    self.z.append(self.z[i])
                    continue
                else:
                    self.x.append(self.x[i])
                    self.y.append(self.y[i] + 1)
                    self.z.append(self.z[i])
                    visited.append((self.x[i], self.y[i] + 1, self.z[i]))
            # -------------------------- -Y --------------------------#
            elif 49.98 < r <= 66.64:
                if (self.x[i], self.y[i] - 1, self.z[i]) in visited:
                    self.y.append(self.y[i])
                    self.x.append(self.x[i])
                    self.z.append(self.z[i])
                    continue
                else:
                    self.x.append(self.x[i])
                    self.y.append(self.y[i] - 1)
                    self.z.append(self.z[i])
                    visited.append((self.x[i], self.y[i] - 1, self.z[i]))
            # -------------------------- +Z --------------------------#
            elif 66.64 < r < 83.33:
                if (self.x[i], self.y[i], self.z[i] + 1) in visited:
                    self.x.append(self.x[i])
                    self.y.append(self.y[i])
                    self.z.append(self.z[i])
                    continue
                else:
                    self.x.append(self.x[i])
                    self.y.append(self.y[i])
                    self.z.append(self.z[i] + 1)
                    visited.append((self.x[i], self.y[i], self.z[i] + 1))
            # -------------------------- -Z --------------------------#
            else:
                if (self.x[i], self.y[i], self.z[i] - 1) in visited:
                    self.x.append(self.x[i])
                    self.y.append(self.y[i])
                    self.z.append(self.z[i])
                    continue
                else:
                    self.x.append(self.x[i])
                    self.y.append(self.y[i])
                    self.z.append(self.z[i] + 1)
                    visited.append((self.x[i], self.y[i], self.z[i] - 1))
        self.z_switch = True
        return self.x, self.y, self.z

    def set_key(self, i_key):
        """
        sets a key for Walker instance which can be used later to identify it
        :param i_key: key as a string
        """
        if isinstance(i_key, str):
            self.key = i_key
        else:
            raise TypeError("Key must be a string value")

    def plot(self):
        """

        Plots the walker's path in 2D or 3D
        """
        if self.z_switch is True:
            ax = plt.axes(projection='3d')
            ax.plot3D(self.x, self.y, self.z, 'gray')
            plt.show()
        else:
            fig1 = plt.figure(1)
            fig1.suptitle("Walker's Path")
            plt.xlabel("x-position")
            plt.ylabel("y-position")
            plt.plot(self.x, self.y)
            plt.show()


