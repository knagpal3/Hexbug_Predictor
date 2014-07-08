import hexbug_predictor
import unittest
from math import *

#These tests are for the "calculate_heading_turning" support function
class CalculateBearingTurningTests(unittest.TestCase):

	def testNoTurn(self):
		measurement1 = [0,0]
		measurement2 = [1,0]
		measurement3 = [2,0]
		[heading,turning] = hexbug_predictor.calculate_bearing_turning(measurement1,measurement2,measurement3)
		self.assertEqual(heading, 0)
		self.assertEqual(turning, 0)



	def testRightAngle1(self):
		measurement1 = [0,0]
		measurement2 = [1,0]
		measurement3 = [1,1]
		[heading,turning] = hexbug_predictor.calculate_bearing_turning(measurement1,measurement2,measurement3)
		self.assertEqual(heading, pi)
		self.assertEqual(turning, pi/2)

	def testRightAngle2(self):
		measurement1 = [0,0]
		measurement2 = [1,0]
		measurement3 = [1,-1]
		[heading,turning] = hexbug_predictor.calculate_bearing_turning(measurement1,measurement2,measurement3)
		self.assertEqual(heading, pi)
		self.assertEqual(turning, -pi/2)

	def test45degreeangle1(self):
		measurement1 = [0,0]
		measurement2 = [1,1]
		measurement3 = [1,2]
		[heading,turning] = hexbug_predictor.calculate_bearing_turning(measurement1,measurement2,measurement3)
		self.assertEqual(heading, 3*pi/4)
		self.assertEqual(turning, pi/4)


	def test45degreeangle2(self):
		measurement1 = [0,0]
		measurement2 = [1,-1]
		measurement3 = [1,-2]
		[heading,turning] = hexbug_predictor.calculate_bearing_turning(measurement1,measurement2,measurement3)
		self.assertEqual(heading, 5*pi/4)
		self.assertEqual(turning, -pi/4)


	def test135degreeangle1(self):
		measurement1 = [0,0]
		measurement2 = [1,1]
		measurement3 = [0,1]
		[heading,turning] = hexbug_predictor.calculate_bearing_turning(measurement1,measurement2,measurement3)
		self.assertEqual(heading, 7*pi/4)
		self.assertEqual(turning, 3*pi/4)


if __name__== "__main__":
	unittest.main()