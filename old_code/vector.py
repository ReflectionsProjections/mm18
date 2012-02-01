#! /usr/bin/env python

import unittest

from math import fabs, sqrt, hypot
import random

def distance(pos1, pos2):
	"""Returns the distance between two (x, y) position tuples
	
	@param pos1: First position
	@param pos2: Second position
	"""

	return sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def comp(a, b):
	""" Returns the scalar projection of vector a onto vector b
	@param a: vector a
	@param b: vector b

	@type: number
	@return: scalar projection of a onto b
	"""
	# component projection of a onto b
	comp = (a[0] * b[0] + a[1] * b[1])/(hypot(*b)**2)
	return comp

def proj(a, b):
	""" Returns the projection of vector a onto vector b
	@param a: vector a
	@param b: vector b
	
	@type: tuple
	@return: vector projection of a onto b
	"""
	# component projection of a onto b
	comp = (a[0] * b[0] + a[1] * b[1])/(hypot(*b)**2)
	# now multiply that by b
	proj = (comp * b[0], comp * b[1])
	return proj

def intersect_circle(circle, line):
	""" Checks to see if a line intersects with a circle.
	@param circle: ((x,y), radius) center and radius
	@param line: ((x, y), (x, y)) start point and vector

	@return: True if the line interesects with the circle
	"""
	# start point of line
	start = line[0]
	end = (line[0][0] + line[1][0], line[0][1] + line[1][1])
	# Vector of line
	line_v = line[1]
	# Vector of endpoint to start (reverse)
	neg_line_v = (-line_v[0], -line_v[1])
	# Vector of start to center
	center_v = (circle[0][0] - start[0], circle[0][1] - start[1])
	neg_center_v = (circle[0][0] - end[0], circle[0][1] - end[1])
	# scalar projectections
	comp1 = comp(center_v, line_v)
	comp2 = comp(neg_center_v, neg_line_v)
	# if both positive, then within band
	if comp1 >= 0 and comp2 >= 0:
		# now check if mag of ortho vector is greater than radius
		proj = (comp1*line_v[0], comp1*line_v[1])
		# find  orthoganl complement
		ortho_v = (center_v[0] - proj[0], center_v[1] - proj[1])
		# get the distance from the point to the center
		dist = hypot(*ortho_v)
		# and see if we collide or not
		if dist <= circle[1]:
			return True
		else:
			return False
	elif distance(start, circle[0]) <= circle[1] or \
			distance(end, circle[0]) <= circle[1]:
		return True
	else: return False

def circle_in_rect(circle, rect):
	""" Checks to see if a circle intersects the rectangle.

	@param circle: ((x,y), radius) center and radius
	@param rect: a tuple of fours points, stored CCW

	@return: True if center is in rectangle.
	"""
	# each side has a start point and a vector
	sides = [(rect[0], (rect[1][0] - rect[0][0], rect[1][1] - rect[0][1])),
			(rect[1], (rect[2][0] - rect[1][0], rect[2][1] - rect[1][1])),
			(rect[2], (rect[3][0] - rect[2][0], rect[3][1] - rect[2][1])),
			(rect[3], (rect[0][0] - rect[3][0], rect[0][1] - rect[3][1]))]
	# See if any of the sides intersect the circle
	for side in sides:
		if intersect_circle(circle, side):
			return True

	# Did not work, so test if circle is entirely in rectangle
	# if false, it is outside rectangle entirely.
	for side in sides:
		disp = (circle[0][0] - side[0][0], circle[0][1] - side[0][1])
		if comp(disp, side[1]) < 0:
			return False
	return True

def circle_collision(circle1, circle2):
	"""Checks to see if a circle intersects another circle
False
	@param circle1: ((x,y), radius) center and radius
	@param circle2: Second circle to check

	@return: True if the circles collide with each other
	"""
	min_dist = circle1[1] + circle2[1]
	dist = distance(circle1[0], circle2[0])
	if dist < min_dist:
		return True
	else:
		return False


def jitter_tuple(tuple, min, max):
	t0 = tuple[0] + random.uniform(min, max)
	t1 = tuple[1] + random.uniform(min, max)
	return (t0, t1)

class VectorTests(unittest.TestCase):
	def test_distance(self):
		self.assertEqual(sqrt(10), distance((0,0), (3, 1)))
		self.assertEqual(1, distance((0,0), (0,1)))
		self.assertEqual(0, distance((0,1),(0,1)))

	def test_circle_collision(self):
		circle1 = ((0,0),1)
		circle2 = ((1,1),1)
		self.assertTrue(circle_collision(circle1 , circle2))
		circle3 = ((4,4),1)
		self.assertFalse(circle_collision(circle2, circle3))
		self.assertFalse(circle_collision(circle1, circle3))

	def test_circle_in_rect(self):
		# Testing rectangle
		rect = ((1,1), (1,-1), (-1,-1), (-1,1))
		# Inside rect and touching sides
		circle1 = ((0,0), 1)
		self.assertTrue(circle_in_rect(circle1, rect))
		# completly outside
		circle2 = ((4,4), 2)
		self.assertFalse(circle_in_rect(circle2, rect))
		# To the right and touching
		circle3 = ((2.5, 0), 1.5)
		self.assertTrue(circle_in_rect(circle3, rect))
		# Inside, not touching
		circle4 = ((0,0), 0.5)
		self.assertTrue(circle_in_rect(circle4, rect))
		# Corner
		circle5 = ((1,1),1)
		self.assertTrue(circle_in_rect(circle5, rect))
		# Just touching corner
		circle6 = ((1,2),1)
		self.assertTrue(circle_in_rect(circle6, rect))
		circle7 = ((2,2), sqrt(2))
		self.assertTrue(circle_in_rect(circle7, rect))
		
		rect2 = ((1,0), (5, 3), (4,4), (0,1))
		# Rotated rect, not touching
		circle8 = ((-3,3),2)
		self.assertFalse(circle_in_rect(circle8, rect2))
		# Rotated rect,  touching
		circle9 = ((1, 1.5),2)
		self.assertTrue(circle_in_rect(circle9, rect2))


	def test_intersect_circle(self):
		circle1 = ((1,1),1)
		circle2 = ((-1,-1),1)
		circle3 = ((-10,10),1)
		line = ((0,0), (2,2))
		self.assertTrue(intersect_circle(circle1, line))
		self.assertFalse(intersect_circle(circle3, line))
		self.assertFalse(intersect_circle(circle2, line))

	def test_comp(self):
		a = (1, 5)
		b = (-4, 7)
		mag = hypot(*b)
		self.assertEqual(31.0/mag**2, comp(a,b))

	def test_proj(self):
		a = (7,34)
		b = (85, 32)
		c = comp(a, b)
		p = (c*b[0], c*b[1])
		self.assertEqual(p, proj(a, b))

if __name__=='__main__':
	unittest.main()
