import numpy as np
from OpenGL.GL import *
from grafica.basic_shapes import Shape
import grafica.transformations as tr
import grafica.easy_shaders as es
import random
from vector3 import normal_3_points

def esfera(r, ntheta=10, nphi=10, color=(1, 0, 0)):
    assert len(color) == 3
    dtheta = np.pi / (ntheta - 1)
    dphi = 2 * np.pi / nphi
    v = [] 
    theta = 0 
    for j in range(ntheta):
        phi = 0 
        for i in range(nphi):
            x = r * np.sin(theta) * np.cos(phi)
            y = r * np.sin(theta) * np.sin(phi)
            z = r * np.cos(theta)
            v.append((x, y, z))
            phi += dphi
        theta += dtheta

    esf_vertices = []
    esf_indices = []

    def triangulo_esfera(points, vertices, indices, i1, i2, i3):
        v1 = points[i1]
        v2 = points[i2]
        v3 = points[i3]
        n = normal_3_points(v1, v2, v3)
        tl = len(indices)
        for tr in (v1, v2, v3):
            triangle = [*tr, *color, *n.export_to_tuple()]
            vertices += triangle
        indices += [tl, tl + 1, tl + 2]

    for j in range(ntheta - 1):
        for i in range(nphi):
            next_i = (i + 1 + j * nphi) % nphi
            triangulo_esfera(
                points=v,
                vertices=esf_vertices,
                indices=esf_indices,
                i1=i + (j + 1) * nphi,
                i2=next_i + j * nphi,
                i3=i + j * nphi
            )
            triangulo_esfera(
                points=v,
                vertices=esf_vertices,
                indices=esf_indices,
                i1=next_i + j * nphi,
                i2=i + (j + 1) * nphi,
                i3=next_i + (j + 1) * nphi
            )
    return Shape(esf_vertices, esf_indices)


class Ball(object):
    def __init__(self, pipeline, radius, color=None, pos=None, v=None, g=-0.75):
        color = np.array([
            random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1)
        ])
        shape = esfera(radius, color=color, ntheta=40, nphi=40)
        gpu_shape = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpu_shape)
        gpu_shape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
        pos = np.array([0,0,random.uniform(-0.8, 0.8)])
        v = np.array([
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        ])

        self.shape = gpu_shape  
        self.pipeline = pipeline  
        self.pos = pos  
        self.tr = tr.translate(*self.pos)  
        self.v = v  
        self.g = g 
        self.r = radius  
        self.ignore_collision = {}

    def update(self, dt):
        self.v[2] += self.g * dt
        self.pos += self.v * dt
        self.pos[2] = max(-1 + 0.5 * self.r, self.pos[2])
        self.tr = tr.translate(*self.pos)
        for k in list(self.ignore_collision.keys()):
            if self.ignore_collision[k] == 0:
                del self.ignore_collision[k]
                continue
            self.ignore_collision[k] -= 1

    def collide_border(self):
        for i in (0, 1, 2):
            if self.pos[i] + self.r > 1.0:
                self.v[i] = -abs(self.v[i]) 

            if self.pos[i] - self.r < -1.0:
                self.v[i] = abs(self.v[i])
 

    def collides(self, ball: 'Ball'):
        if ball == self:
            return False
        difference = self.pos - ball.pos
        distance = np.linalg.norm(difference)
        collision_distance = ball.r + self.r
        return distance < collision_distance

    def collide(self, ball: 'Ball'):
        if self == ball or self._ignore_collision(ball):
            return
        n = self.pos - ball.pos
        n /= np.linalg.norm(n)
        vrel = self.v - ball.v
        vnormal = np.dot(vrel, n) * n
        self.v = self.v - vnormal
        ball.v = ball.v + vnormal

        #temporizador para las colisiones
        self.ignore_collision[ball] = 60

    def _ignore_collision(self, ball: 'Ball'):
        if ball not in self.ignore_collision.keys():
            return False
        return self.ignore_collision[ball] != 0

    def draw(self):
        glUniformMatrix4fv(glGetUniformLocation(self.pipeline.shaderProgram, "model"), 1, GL_TRUE, self.tr)
        self.pipeline.drawCall(self.shape)
