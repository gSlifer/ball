
import glfw
from OpenGL.GL import *
import numpy as np
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
from esfera import Ball
from typing import List

#lista que contiene las esferas
balls: List[Ball] = []

class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = False

controller = Controller()

def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

def createGPUShape(pipeline, shape):
    gpu_shape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpu_shape)
    gpu_shape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpu_shape

if __name__ == "__main__":

    #iniciamos glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1280
    height = 720
    title = "Tarea 1 parte 2"

    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    glfw.set_key_callback(window, on_key)

    pPipeline = ls.SimplePhongShaderProgram()

    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
    lightingPipeline = pPipeline

    glClearColor(0.1, 0.1, 0.1, 1.0)

    #activamos 3D
    glEnable(GL_DEPTH_TEST)

    #creamos el eje
    gpuAxis = createGPUShape(mvpPipeline, bs.createAxis(4))

    #creamos los bordes de la caja
    arista = createGPUShape(lightingPipeline, bs.createColorNormalsCube(0.8, 0.8, 0.8))
    cubo = [
        (tr.matmul([tr.translate(0, 1, -1), tr.scale(2, 0.01, 0.01)]), arista),
        (tr.matmul([tr.translate(0, -1, -1), tr.scale(2, 0.01, 0.01)]), arista),
        (tr.matmul([tr.translate(-1, 0, -1), tr.scale(0.01, 2, 0.01)]), arista),
        (tr.matmul([tr.translate(1, 0, -1), tr.scale(0.01, 2, 0.01)]), arista),
        (tr.matmul([tr.translate(-1, -1, 0), tr.scale(0.01, 0.01, 2)]), arista),  
        (tr.matmul([tr.translate(1, -1, 0), tr.scale(0.01, 0.01, 2)]), arista),  
        (tr.matmul([tr.translate(-1, 1, 0), tr.scale(0.01, 0.01, 2)]), arista), 
        (tr.matmul([tr.translate(1, 1, 0), tr.scale(0.01, 0.01, 2)]), arista),
        (tr.matmul([tr.translate(0, 1, 1), tr.scale(2, 0.01, 0.01)]), arista),
        (tr.matmul([tr.translate(0, -1, 1), tr.scale(2, 0.01, 0.01)]), arista),
        (tr.matmul([tr.translate(-1, 0, 1), tr.scale(0.01, 2, 0.01)]), arista),
        (tr.matmul([tr.translate(1, 0, 1), tr.scale(0.01, 2, 0.01)]), arista),
    ]

    #creamos las bolas
    for i in range(2):
        ball = Ball(lightingPipeline, radius=0.1)
        ball_collide = False
        for j in balls:
            if ball.collides(j):
                ball_collide = True
                break
        if not ball_collide:
            balls.append(ball)

    #creamos cámara
    camera_theta = 90

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    while not glfw.window_should_close(window):

        #eventos
        glfw.poll_events()

        #actualiza los tiempos de iteración
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))
        dt = perfMonitor.getDeltaTime()

        #actualizamos la cámara
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            camera_theta -= (2 * np.pi/15)
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            camera_theta += (2 * np.pi/15)
            
        projection = tr.perspective(45, float(width) / float(height), 0.1, 100)
        camX = 4 * np.sin(camera_theta)
        camY = 4 * np.cos(camera_theta)
        viewPos = np.array([camX, camY, 0.5])
        view = tr.lookAt(
            viewPos,
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
        )

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #cambia modo dibujo
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        #ejes
        if controller.showAxis:
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawCall(gpuAxis, GL_LINES)

        #luces
        glUseProgram(lightingPipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), -5, -5, 5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 100)

        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        #dibujamos el cubo
        for i in cubo:
            glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE, i[0])
            lightingPipeline.drawCall(i[1])

        #actualizamos
        for b in balls:
            b.update(dt)
            b.collide_border()

        #chequeamos las colisiones y dibujamos
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                if balls[i].collides(balls[j]):
                    balls[i].collide(balls[j])
            balls[i].draw()

        #hacemos swap
        glfw.swap_buffers(window)

    #borramos la memoria
    gpuAxis.clear()
    glfw.terminate()
