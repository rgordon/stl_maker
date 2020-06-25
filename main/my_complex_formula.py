# A sample import to show how a person can create a compelx formula by writing their own module

import math
import numpy as np

def return_my_z(x,y):
	'''Return a Z value given the imput X and Y'''
	
	# convert X and Y to polar coordinates (r, theta)
	
	r = np.sqrt(x**2 + y**2)
	theta = np.arctan2(y,x) *180/2*np.pi
	
	
	z= (10**(-r/5)) * math.cos(2*r)
	
	
	
	
	return (z)