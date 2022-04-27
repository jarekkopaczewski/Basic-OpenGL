#!/usr/bin/env python3
import sys

import math
import numpy as np
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.0, 1.0, 0.0, 1.0]
light_diffuse = [0.0, 1.0, 0.0, 1.0]
light_specular = [1.0, 1.0, 0.0, 0.5]
light_position = [0.0, 0.0, 10.0, 1.0]

changes = [light_ambient, light_diffuse, light_specular]
currentX = 0
currentY = 0

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


def shutdown():
    pass

def spin(angle):
    glRotatef(angle, 0.1, 0.0, 0.0)
    glRotatef(angle, 0.0, 0.2, 0.0)
    glRotatef(angle, 0.0, 0.0, 0.5)


def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    spin(time * 180 / math.pi)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 1.5, 25, 25)
    gluDeleteQuadric(quadric)

    quadric2 = gluNewQuadric()
    gluQuadricDrawStyle(quadric2, GLU_LINE)
    gluSphere(quadric2, 3, 10, 10)
    gluDeleteQuadric(quadric2)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def key_callback(window,  key,  scancode,  action,  mods):
    global currentY
    global currentX
    global changes
    global light_position

    if action == GLFW_PRESS:
        if key == GLFW_KEY_W:
            if currentY < 3:
                currentY += 1
            print("Twoja pozycja w tablicy: (" + str(currentX) + ", " + str(currentY) + ")")
        if key == GLFW_KEY_S:
            if currentY > 0:
                currentY -= 1
            print("Twoja pozycja w tablicy: (" + str(currentX) + ", " + str(currentY) + ")")
        if key == GLFW_KEY_A:
            if currentX > 0:
                currentX -= 1
            print("Twoja pozycja w tablicy: (" + str(currentX) + ", " + str(currentY) + ")")
        if key == GLFW_KEY_D:
            if currentX < 2:
                currentX += 1
            print("Twoja pozycja w tablicy: (" + str(currentX) + ", " + str(currentY) + ")")
        if key == GLFW_KEY_K:
            if changes[currentX][currentY] >= 0.1:
                changes[currentX][currentY] = round(changes[currentX][currentY] - 0.1, 1)
            print("changes[" + str(currentX) + "][" + str(currentY) + "] = " + str(changes[currentX][currentY]))
        if key == GLFW_KEY_L:
            if changes[currentX][currentY] <= 0.9:
                changes[currentX][currentY] = round(changes[currentX][currentY] + 0.1, 1)
            print("changes[" + str(currentX) + "][" + str(currentY) + "] = " + str(changes[currentX][currentY]))
        if key == GLFW_KEY_R:
            changes = np.zeros((3, 4))
            print("-- Restart --\n")
        elif key == GLFW_KEY_M:
            print(changes[0])
            print(changes[1])
            print(changes[2])

    glEnable(GL_DEPTH_TEST)

    glLightfv(GL_LIGHT0, GL_AMBIENT, changes[0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, changes[1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, changes[2])
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetKeyCallback(window, key_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
