# coding=utf-8
"""
MATHLIB
Utilitary math library.

GLFW-TOOLBOX
Toolbox for GLFW Graphic Library.
https://github.com/ppizarror/glfw-toolbox

MIT License
Copyright (c) 2019-2020 Pablo Pizarro R.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Library imports
import math as _math

class Vector3(object):
    """
    3 component Vector.
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """
        Constructor.
        :param x: X-coordinate
        :param y: Y-coordinate
        :param z: Z-coordinate
        :type x: float, int, hex, oct, complex
        :type y: float, int, hex, oct, complex
        :type z: float, int, hex, oct, complex
        """
        self.x = x
        self.y = y
        self.z = z

    def get_module(self):
        """
        Returns vector module.
        :return: Module
        :rtype: float
        """
        return self.distance_with(Vector3(0, 0, 0))

    def set_x(self, x):
        """
        Set x-coordinate.
        :param x: X-coordinate
        :type x: float, int, hex, oct, complex
        """
        self.x = x

    def set_y(self, y):
        """
        Set y-coordinate.
        :param y: Y-coordinate
        :type y: float, int, hex, oct, complex
        """
        self.y = y

    def set_z(self, z):
        """
        Set z-coordinate.
        :param z: Z-coordinate
        :type z: float, int, hex, oct, complex
        """
        self.z = z

    def get_x(self):
        """
        Get x-coordinate
        :return: Coordinate
        :rtype: float, int, hex, oct, complex
        """
        return self.x

    def get_y(self):
        """
        Get y-coordinate
        :return: Coordinate
        :rtype: float, int, hex, oct, complex
        """
        return self.y

    def get_z(self):
        """
        Get z-coordinate
        :return: Coordinate
        :rtype: float, int, hex, oct, complex
        """
        return self.z

    def __sub__(self, other):
        """
        Substract vector with another.
        :param other: Vector
        :type other: Vector3, tuple, list
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(other, Vector3):
            return Vector3(self.x - other.get_x(), self.y - other.get_y(),
                           self.z - other.get_z())
        elif type(other) is tuple or type(other) is list:
            if len(other) == 3:
                return Vector3(self.x - other[0], self.y - other[1],
                               self.z - other[2])
        else:
            return self

    def get_normalized(self):
        """
        Generates normalized vector.
        :return: New vector
        :rtype: Vector3
        """
        modl = self.get_module()
        if modl == 0:
            modl = 1
        return Vector3(self.x / modl, self.y / modl, self.z / modl)

    def cross(self, other):
        """
        Return new vector from cross operation.
        :param other: Vector
        :type other: Vector3, tuple, list
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(other, Vector3):
            i = self.y * other.get_z() - self.z * other.get_y()
            j = self.z * other.get_x() - self.x * other.get_z()
            k = self.x * other.get_y() - self.y * other.get_x()
            return Vector3(i, j, k)
        elif type(other) is tuple or type(other) is list:
            return self.cross(Vector3(*other))
        else:
            return self

    def distance_with(self, other):
        """
        Return distance from another vector.
        :param other: Vector
        :type other: Vector3, tuple, list
        :return: Distance
        :rtype: float
        """
        if isinstance(other, Vector3):
            return _math.sqrt(
                (self.x - other.get_x()) ** 2 + (self.y - other.get_y()) ** 2 + (self.z - other.get_y()) ** 2)
        elif type(other) is list or type(other) is tuple:
            return self.distance_with(Vector3(*other))
        else:
            return 0.0

    def export_to_list(self):
        """
        Export vector to list.
        :return: List containing coordinates
        :rtype: list
        """
        return [self.x, self.y, self.z]

    def export_to_tuple(self):
        """
        Export vector to tuple.
        :return: Tuple containing coordinates
        :rtype: tuple
        """
        return self.x, self.y, self.z


def normal_3_points(a, b, c):
    """
    Return normal vector from 3 points.
    :param a: Point a
    :param b: Point b
    :param c: Point c
    :type a: tuple, Point3
    :type b: tuple, Point3
    :type c: tuple, Point3
    :return: Normal vector
    :rtype: Vector3
    """
    if type(a) is list or type(a) is tuple:
        a = Vector3(*a)
        b = Vector3(*b)
        c = Vector3(*c)
    else:
        a = Vector3(*a.export_to_list())
        b = Vector3(*b.export_to_list())
        c = Vector3(*c.export_to_list())
    cross_result = (a - c).cross(b - c).get_normalized()
    if cross_result.get_x() == -0.0:
        cross_result.set_x(0.0)
    if cross_result.get_y() == -0.0:
        cross_result.set_y(0.0)
    if cross_result.get_z() == -0.0:
        cross_result.set_z(0.0)
    return cross_result
