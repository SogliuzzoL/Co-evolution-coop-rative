# Function to evaluate the "lamp" problem, where we try to place round-shaped lamps to cover a square space
# by Thomas Chabin, Evelyne Lutton, Alberto Tonda, 2018 <alberto.tonda@gmail.com>

import math
import matplotlib.pyplot as plt
import numpy as np
import sys

from matplotlib.patches import Circle, Rectangle

def evaluateLamps(lamps, radius, square, visualize=False) :
	
	globalFitness = 0.0
	individualFitness = [0] * len(lamps)
	
	# this is a very rough discretization of the space
	discretization = 100 # TODO lower discretization here to speed up computation, increase for increased precision
	discretizationStep = square[0] / discretization
	totalArea = square[0] * discretization * square[1] * discretization
	
	# compute coverage of the square, going step by step
	coverage = 0.0
	overlap = 0.0
	
	for x in np.arange(0.0, square[0], discretizationStep) :
		for y in np.arange(0.0, square[1], discretizationStep) :
			coveredByLamps = 0
			for l in range(0, len(lamps)) :
				
				lamp = lamps[l]

				# if the distance between the point and the center of any lamp is less than
				# the radius of the lamps, then the point is lightened up!
				distance = math.sqrt( math.pow(lamp[0] - x, 2) + math.pow(lamp[1] - y, 2) )
				if distance <= radius : 
					coveredByLamps += 1
					individualFitness[l] += 1
			
			# now, if the point is covered by at least one lamp, the global fitness increases 
			if coveredByLamps > 0 : coverage += 1
			# but if it is covered by two or more, there's a 'waste' of light here, an overlap
			if coveredByLamps > 1 : overlap += 1
	
	# the global fitness can be computed in different ways
	globalFitness = coverage / totalArea # just as total coverage by all lamps
	#globalFitness = (coverage - overlap) / totalArea # or maybe you'd like to also minimize overlap!
	
	# if the flag "visualize" is true, let's plot the situation
	if visualize :
		
		figure = plt.figure()
		ax = figure.add_subplot(111, aspect='equal')
		
		# matplotlib needs a list of "patches", polygons that it is going to render
		for l in lamps :
			ax.add_patch( Circle( (l[0],l[1]), radius=radius, color='b', alpha=0.4) )
		ax.add_patch( Rectangle( (0,0), square[0], square[1], color='w', alpha=0.4 ) )
		
		ax.set_title("Lamp coverage of the arena (fitness %.2f)" % globalFitness)
		plt.show()
		plt.close(figure)
	
	return globalFitness


# this main is just here to try the function, and give you an idea of how it works
def main() :
	
	# sides of the square, [width, height]
	square = [1, 1]
	
	# radius of the lamps
	radius = 0.3
	
	# coordinates of the lamps [ [x1,y1], [x2,y2], [x3,y4], ... ]
	lamps = [ [0.3,0.3], [0.3,0.7], [0.7,0.3], [0.7,0.7] ]
	
	# calling the function; the argument "visualize=True" makes it plot the current situation
	fitness = evaluateLamps(lamps, radius, square, visualize=True)
	
	return

if __name__ == "__main__" :
	sys.exit( main() )
