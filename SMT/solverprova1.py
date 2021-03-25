import os
import numpy as np
from z3 import And, Or, Int, If, Solver, sat

dazone = "D:\\Uni\\2020-21 2 sem\\opt\\project\\Instances\\8x8.txt" 
dim_pieces = []
with open(dazone, "r") as input:
    #pn the first line we have the dimension of the grid
    h, w = list(map(int,input.readline().replace("\n","").split(" ")))
    
    #on the second line we have the number of pieces
    pieces = int(input.readline().replace("\n",""))
    
    #the following "pieces" lines are the dimentions of the single pieces
    for i in range(0, pieces):
        dim_pieces.append(list(map(int, input.readline().replace("\n","").split(" "))))

#note that the first number indicates which piece we are talking about,
#the second is the dimension:
#   0 = width
#   1 = height
bl_corner = [[Int("p_{}_{}".format(i, dim)) for dim in [0,1] ] for i in range(pieces) ]

#All the low left angles need to stay inside the grid
in_domain = [ And(  bl_corner[i][0] >= 0,
                    bl_corner[i][0] < w, 
                    bl_corner[i][1] >= 0, 
                    bl_corner[i][1] < h) for i in range(pieces)] 

#All the pieces need to fit inside the grid
in_paper = [ And(   bl_corner[i][0] + dim_pieces[i][0] <= w, #TODO: idk if it < or <= 
                    bl_corner[i][1] + dim_pieces[i][1] <= h ) for i in range(pieces)] 

#TODO put all the constraint in one single list and then flatten

#TODO find a different cycle to do this
no_overlap = []		
for i in range(pieces):
    for j in range(pieces):
        if (i<j):
            #given the squares 0, 1 we check that one of the following condition applies:
            #  - 0 is fully on the left of 1
            #  - 1 is fully on the left of 0
            #  - 0 is fully below of 1
            #  - 1 is fully below of 0 
            no_overlap.append(  Or( bl_corner[i][0] + dim_pieces[i][0] <= bl_corner[j][0], 
                                    bl_corner[j][0] + dim_pieces[j][0] <= bl_corner[i][0], 
                                    bl_corner[i][1] + dim_pieces[i][1] <= bl_corner[j][1], 
                                    bl_corner[j][1] + dim_pieces[j][1] <= bl_corner[i][1]))

#??? i dont get this:
#It checks if the summ of all heights of the squares in a given witdth position is less than the grid's hight
#This makes no sense to me as we already know that there is no square that surpass that limit and the square cannot overlap.
#TODO understand if it is usefull (i don't think so)
"""
implied = []
for i in range(width):
    for j in range(number_of_pieces):
        implied.append( Sum(
            [If(And(O[j][x] <= i, i < O[j][x] + pieces[j][x]), 
                                pieces[j][y],0) for j in range(number_of_pieces)]) <= height)

for i in range(height):
    for j in range(number_of_pieces):
        implied.append(Sum([If(And( O[j][y] <= i, i < O[j][y] + pieces[j][y]), pieces[j][x],0) for j in range(number_of_pieces)]) <= width)

"""
#As I was saying before this is not used. 🤢🤮
constraints = in_domain + in_paper + no_overlap 

solver = Solver()
solver.add(constraints)
if solver.check() == sat:

    m = solver.model()
    
    print("{} {}".format(h, w))
    for i in range(pieces):
        print("{:<1} {:<3} {:<1} {:<2}".format(dim_pieces[i][0], dim_pieces[i][1], str(m[bl_corner[i][0]]), str(m[bl_corner[i][1]])))

else:
    print("STO VOLANDO")