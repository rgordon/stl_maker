# A sample import to show how a person can create a compelx formula by writing their own module

import math
import numpy as np

def return_my_z(x,y):
	'''Return a Z value given the imput X and Y'''
	
	# convert X and Y to polar coordinates (r, theta)
	r = np.sqrt(x**2 + y**2)
	theta = np.arctan2(y,x) *180/np.pi
	
	# Several interesting equations - uncomment whichever you want to use
	
	#  radiating waves from the origin
	#z = math.cos(2*r)
	
	
	#  damped radiating waves from the origin
	'''z= (6/(r**2+4)) * math.cos(2*r)'''
	
	#  damped radiating waves interference
	'''x1 = x+2
	r1 = np.sqrt(x1**2 + y**2)
	x2 = x-2
	r2 = np.sqrt(x2**2 + y**2)
	z= (6/(r1**2+4)) * math.cos(2*r1) + (6/(r2**2+4)) * math.cos(2*r2)'''
	
	#  damped radiating waves superposition
	'''x1 = x+2
	r1 = np.sqrt(x1**2 + y**2)
	x2 = x-2
	r2 = np.sqrt(x2**2 + y**2)
	z= max((6/(r1**2+4)) * math.cos(2*r1) , (6/(r2**2+4)) * math.cos(2*r2) )'''
	
	# half donut
	'''r1 = r-4.5
	if 3<r<6:
		z= math.sqrt(1.5**2 -r1**2)
	else: z=0'''
	
	
	#  waves wrapping around the origin
	'''z = math.sin(np.pi*theta/180)'''
	
	
	# coiled snake (single arm spiral with a half circle cross section)
	a = 1            # radius where spiral starts
	growth_per_wrap = 4  # How much the spiral moves out per cycle
	b = growth_per_wrap/360        # units of radial movement per degree of angle
	r_bump = growth_per_wrap/4     # radius of the snake's body 
	#start_angle = 45 # sngle where the spiral starts
	#  equation of the spiral's radius at angle theta   r_spiral =  a + b*(start_angle + theta)
	r_bump_squared = r_bump**2
	
	# Find closest spiral arm at this r, theta
	# step out one wrap at a time

	found_z = False
	r_last_wrap = 0
	distance_last_wrap = 100
	
	for i in range(10):
		if r< a: #we are within the center of the spiral
			z=-r_bump
			return (z)
		distance_to_spiral = abs(  r -  (a + b*(360*i + theta) )   )
		if distance_to_spiral <= r_bump: # We are close enough to this wrap of spiral arm to be part of the snake
			z = math.sqrt(r_bump_squared - distance_to_spiral**2)
			return (z)
		else:   # we might be between bumps. Test whether the distance to spiral is growing
			if distance_to_spiral > distance_last_wrap: # we are between bumps, but closer on the last wrap
				distance_to_spiral = abs(  r -  (a + b*(360*(i-1) + theta) )   )
				z = -1 * math.sqrt(r_bump_squared - (2*r_bump -distance_to_spiral)**2)
				#z = 0
				return (z)
			else: distance_last_wrap = distance_to_spiral
			

	return (z)