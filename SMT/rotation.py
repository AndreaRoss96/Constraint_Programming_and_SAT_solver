import os
import numpy as np
from z3 import And, Or, Int, If, Solver, sat, Implies

dazone = "D:\\Uni\\2020-21 2 sem\\opt\\project\\Instances\\provaRotazione.txt" 
dazone = "D:\\Uni\\2020-21 2 sem\\opt\\projguyez\\Present-Wrapping-Problem\\Instances\\3x3.txt"
dim_pieces = []
with open(dazone, "r") as input:
    # On the first line we have the dimension of the grid

    h, w = list(map(int,input.readline().replace("\n","").split(" ")))
    
    # On the second line we have the number of pieces
    pieces = int(input.readline().replace("\n",""))
    
    # The following "pieces" lines are the dimentions of the single pieces
    for i in range(0, pieces):
        dim_pieces.append(list(map(int, input.readline().replace("\n","").split(" "))))

# Note that the first number indicates which piece we are talking about,
# the second is the dimension:
#   0 = width
#   1 = height
bl_corner = [[Int("p_{}_{}".format(i, dim)) for dim in [0,1] ] for i in range(pieces) ]
# The rotation is handled by simply having a new list that will hold how the dimentions are oriented
true_dim = [[Int("dim_{}_{}".format(i, dim)) for dim in [0,1] ] for i in range(pieces) ]

# The rotation clause tells the true_dimention variable that it has to take certain values
rotation = [Or( And(true_dim[i][0] == dim_pieces[i][0], 
                    true_dim[i][1] == dim_pieces[i][1]), 
                And(true_dim[i][0] == dim_pieces[i][1],
                    true_dim[i][1] == dim_pieces[i][0])
            ) for i in range(pieces)]


in_domain = [ And(  bl_corner[i][0] >= 0,
                    bl_corner[i][0] < w, 
                    bl_corner[i][1] >= 0, 
                    bl_corner[i][1] < h) for i in range(pieces)] 

# All the pieces need to fit inside the grid
in_paper = [ And(   bl_corner[i][0] + true_dim[i][0] <= w, #TODO: idk if it < or <= 
                    bl_corner[i][1] + true_dim[i][1] <= h ) for i in range(pieces)] 

#TODO put all the constraint in one single list and then flatten

#TODO find a different cycle to do this
no_overlap = []		
for i in range(pieces):
    for j in range(pieces):
        if (i<j):
            # Given the squares 0, 1 we check that one of the following condition applies:
            #  - 0 is fully on the left of 1
            #  - 1 is fully on the left of 0
            #  - 0 is fully below of 1
            #  - 1 is fully below of 0 
            no_overlap.append(  Or( bl_corner[i][0] + true_dim[i][0] <= bl_corner[j][0], 
                                    bl_corner[j][0] + true_dim[j][0] <= bl_corner[i][0], 
                                    bl_corner[i][1] + true_dim[i][1] <= bl_corner[j][1], 
                                    bl_corner[j][1] + true_dim[j][1] <= bl_corner[i][1]))

# This constraint is used to limit the simmetry of the pieces, if two pieces are equals 
# they will have a designed relative position in the positioning
no_simmetry = []
for i in range(pieces):
    for j in range(i, pieces):
        #check if two pieces have the same dimention or can be rotated to have that
        if( (dim_pieces[i][0] == dim_pieces[j][0] and dim_pieces[i][1] == dim_pieces[j][1]) or
            (dim_pieces[i][0] == dim_pieces[j][1] and dim_pieces[i][1] == dim_pieces[j][0])):
            #if that's so assign a position relative to the two
            no_simmetry.append(And(bl_corner[i][0] <= bl_corner[j][0],
                                    Implies(bl_corner[i][0] == bl_corner[j][0],
                                            bl_corner[i][1] <= bl_corner[j][1])))

constraints = in_domain + in_paper + no_overlap + rotation + no_simmetry

solver = Solver()
solver.add(constraints)
if solver.check() == sat:

    m = solver.model()
    
    print("{} {}".format(h, w))
    for i in range(pieces):
        print("{:<1} {:<3} {:<1} {:<2}".format(str(m[true_dim[i][0]]), str(m[true_dim[i][1]]), str(m[bl_corner[i][0]]), str(m[bl_corner[i][1]])))

else:
    print("STO VOLANDO")