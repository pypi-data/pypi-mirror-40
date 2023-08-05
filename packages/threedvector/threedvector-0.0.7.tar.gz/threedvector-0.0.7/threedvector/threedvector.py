from operator import add, sub
from numbers import Number
import math


class Vector:

    @classmethod
    def to_spherical(cls, c_vector):
        x = c_vector[0]
        y = c_vector[1]
        z = c_vector[2]
        r = math.sqrt(x**2 + y**2 + z**2)
        theta = math.atan2(y, x)
        phi = math.atan2(math.sqrt(x**2 + y**2), z)
        return Vector(r, math.degrees(theta), math.degrees(phi))

    def __init__(self, radius_x=0, theta_y=0, phi_z=0, coords="spherical"):
        if coords == "cartesian":
            self.__init_cartesian(radius_x, theta_y, phi_z)
        elif coords == "spherical":
            self.__init_spherical(radius_x, theta_y, phi_z)
        else:
            raise AttributeError(
                "Incorrect parameter for coords keyword in Vector __init__")

    def __init_spherical(self, radius, theta, phi):
        self.radius = radius
        self.theta = theta % 360
        self.phi = phi % 360

    def __init_cartesian(self, x, y, z):
        temp_vector = self.to_spherical([x, y, z])
        self.radius = temp_vector.radius
        self.theta = temp_vector.theta
        self.phi = temp_vector.phi

    def __str__(self):
        return (f"({self.radius}, {self.theta}, {self.phi})")

    def __add__(self, other):
        summed_vectors = list(
            map(add, self.to_cartesian(), other.to_cartesian()))
        return self.to_spherical(summed_vectors)

    def __sub__(self, other):
        subbed_vectors = list(
            map(sub, self.to_cartesian(), other.to_cartesian()))
        return self.to_spherical(subbed_vectors)

    def __rmul__(self, factor):
        return self.__mul__(factor)

    def __mul__(self, factor):
        if not isinstance(factor, Number):
            raise TypeError(
                "Built in mulitplication only valid with scalar values.  For dot product or cross product, use respective dot() and cross() functions.")
        product = self.radius * factor
        return Vector(product, self.theta, self.phi)

    def __div__(self, divisor):
        try:
            division = self.radius / divisor
        except TypeError as ex:
            print(ex)
            print("\nCan only divide vectors by scalar.")
        else:
            return Vector(division, self.theta, self.phi)

    def __eq__(self, other):
        return self.radius == other.radius

    def __gt__(self, other):
        return self.radius > other.radius

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def is_same(self, other):
        return self.radius == other.radius and self.theta == other.theta and self.phi == other.phi

    def to_cartesian(self):
        radius = self.radius
        cos_phi = math.cos(math.radians(self.phi))
        sin_phi = math.sin(math.radians(self.phi))
        cos_theta = math.cos(math.radians(self.theta))
        sin_theta = math.sin(math.radians(self.theta))
        x = radius*sin_phi*cos_theta
        y = radius*sin_phi*sin_theta
        z = radius*cos_phi
        return [x, y, z]

    def dot(self, other):
        c_self = self.to_cartesian()
        c_other = other.to_cartesian()
        return c_self[0]*c_other[0] + \
            c_self[1]*c_other[1] + c_self[2]*c_other[2]

    def cross(self, other):
        c_self = self.to_cartesian()
        c_other = other.to_cartesian()
        cross_x = c_self[1]*c_other[2] - c_self[2]*c_other[1]
        cross_y = c_self[2]*c_other[0] - c_self[0]*c_other[2]
        cross_z = c_self[0]*c_other[1] - c_self[1]*c_other[0]
        return self.to_spherical([cross_x, cross_y, cross_z])

    def angle(self, other):
        return math.degrees(math.acos(self.dot(other)/(self.radius * other.radius)))

    def magnitude(self):
        return self.radius

    def unit(self):
        c_self = self.to_cartesian()
        r = math.sqrt(c_self[0]**2 + c_self[1]**2 + c_self[2]**2)
        return self.to_spherical([x/r for x in c_self])
