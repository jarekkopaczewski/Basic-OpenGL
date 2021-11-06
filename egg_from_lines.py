#!/usr/bin/env python3
import sys
import math
from glfw.GLFW import *
from OpenGL.GL import *
import numpy
import random


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def vertex(arr, n):
    for i in range(0, n):
        for j in range(0, n):
            glColor3f(random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0))

            if i + 1 < n:
                glBegin(GL_LINES)
                glVertex3fv(arr[i][j])
                glVertex3fv(arr[i + 1][j])
                glEnd()

            if j + 1 < n:
                glBegin(GL_LINES)
                glVertex3fv(arr[i][j])
                glVertex3fv(arr[i][j + 1])
                glEnd()

            if i + 1 < n and j + 1 < n:
                glBegin(GL_LINES)
                glVertex3fv(arr[i][j])
                glVertex3fv(arr[i + 1][j + 1])
                glEnd()

            if j + 1 < n and i > 0:
                glBegin(GL_LINES)
                glVertex3fv(arr[i][j])
                glVertex3fv(arr[i - 1][j + 1])
                glEnd()


def spin(angle):
    glRotatef(angle, 0.1, 0.0, 0.0)
    glRotatef(angle, 0.0, 0.2, 0.0)
    glRotatef(angle, 0.0, 0.0, 0.5)


def render(time, arr, n):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 30 / math.pi)
    vertex(arr, n)
    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def generate_vertex(n):
    arr = numpy.zeros((n, n, 3))

    for i in range(0, n):
        u = float(i) / n
        for j in range(0, n):
            v = float(j) / n
            temp = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u)
            arr[i][j][0] = temp * math.cos(math.pi * v)
            arr[i][j][1] = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2
            arr[i][j][2] = temp * math.sin(math.pi * v)
    return arr


def main():
    random.seed()
    read = 0
    number_of_vertex = 0

    while read == 0:
        try:
            number_of_vertex = (int(input("Podaj ilość wierzchołków: ")))
            read = 1
        except:
            print("Podaj liczbe!")

    arr = generate_vertex(number_of_vertex)

    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), arr, number_of_vertex)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


main()
