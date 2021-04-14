#this scipt houses all the possible functions needed for integrating over a region
from math import sin, cos, tan, asin, acos, atan, pi, sqrt

def inflower(x, z, r, loops, M):
        return sqrt(x**2 + z**2) <= r*M*cos(loops*atan(z/x)) and atan(z/x) <= pi/8

def outflower(x, z, r, loops, M):
        if atan(z/x) <= pi/8:
                return sqrt(x**2 + z**2) >= r*M*cos(loops*atan(z/x)) and atan(z/x) <= pi/8
        elif pi/8 <= atan(z/x) <= pi/2:
                return True
        else:
                return False
def sphere1(x, r):
        """sphere of radius r. used in 1d"""
        return x <= r

def ellipsoid(x, z, a , b):
        """a = radius in x. b = radius in z"""
        return ((x/a)**2 + (z/b)**2 <= 1)

def sphere2(x, z, r):
        """r = radius. used in 2d"""
        return(x**2 + z**2 <= r**2)

def cylinder(x, z, r, zmax=100000):
        """r = radius. zmax (optional) = distance above and below xy plane. May need to increase default zmax for large distance scales"""
        return(x <= r and abs(z) <=zmax)

def all():
	return True
