#!/usr/bin/env python3
import sys
from OpenGL.GL import *
from glfw.GLFW import *
import random


def startup():
    update_viewport(400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(x, y, a, b):
    glClear(GL_COLOR_BUFFER_BIT)

    d = random.uniform(0.0, b/5)
    z = random.uniform(0.0, a/5)

    # wartość d odpowiada za oddalanie lewego górnego oraz prawego dolnego wierzhcołka
    # wartość z odpowiada za zbliżanie się lewego dolnego oraz prawego górnego wierzchołka
    glColor3f(random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0))
    glBegin(GL_TRIANGLES)
    glVertex2f(x + z, y + z)
    glVertex2f(x - d, y + a + d)
    glVertex2f(x + b + d, y - d)
    glEnd()

    glColor3f(random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0))
    glBegin(GL_TRIANGLES)
    glVertex2f(x + b - z, y + a - z)
    glVertex2f(x - d, y + a + d)
    glVertex2f(x + b + d, y - d)
    glEnd()

    glFlush()


def update_viewport(width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    random.seed()
    params = []
    messages = ["x", "y", "a", "b"]

    i = 0
    while i < 4:
        try:
            params.append(float(input("Podaj wartość " + messages[i] + ": ")))
            i += 1
        except:
            print("Podaj liczbe typu float!")

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
        render(params[0], params[1], params[2], params[3])
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


main()
