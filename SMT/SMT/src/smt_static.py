# Orazi Filippo 
# Rossolini Andrea


from os import listdir
from os.path import join, isfile
import numpy as np
from z3 import And, Or, Int, If, Solver, sat, Implies , Sum
from printer import printer

# Path to the outputs
output_dir = ""
#Path to the inputs the program 
inputs_dir = ""
files = [filename for filename in listdir(inputs_dir) if isfile(join(inputs_dir, filename))]
for filename in files:

    dim_pieces = []
    with open(join(inputs_dir, filename), "r") as input:
        #on the first line we have the dimension of the grid
        w, h = list(map(int,input.readline().replace("\n","").split(" ")))

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
    constraints = []
    
    #All the low left angles need to stay inside the grid
    constraints += [ And(  bl_corner[i][0] >= 0,
                        bl_corner[i][0] < w,
                        bl_corner[i][1] >= 0,
                        bl_corner[i][1] < h) for i in range(pieces)]

    #All the pieces need to fit inside the grid
    constraints += [ And(   bl_corner[i][0] + dim_pieces[i][0] <= w, #TODO: idk if it < or <=
                        bl_corner[i][1] + dim_pieces[i][1] <= h ) for i in range(pieces)]

    # This constraint is used to limit the simmetry of the pieces, if two pieces are equals 
    # they will have a designed relative position in the positioning
    no_simmetry = []

    # This constraint is used to impose a no overlap condition so that the pieces occupy  
    # different spaces
    no_overlap = []
    for i in range(pieces):
        for j in range(i+1, pieces):
            #  - p0 is fully on the left of 1
            #  - p1 is fully on the left of 0
            #  - p0 is fully below of 1
            #  - p1 is fully below of 0
            no_overlap.append(  Or( bl_corner[i][0] + dim_pieces[i][0] <= bl_corner[j][0],
                                    bl_corner[j][0] + dim_pieces[j][0] <= bl_corner[i][0],
                                    bl_corner[i][1] + dim_pieces[i][1] <= bl_corner[j][1],
                                    bl_corner[j][1] + dim_pieces[j][1] <= bl_corner[i][1]))
            
            #check if two pieces have the same dimention or can be rotated to have that
            if( (dim_pieces[i][0] == dim_pieces[j][0] and dim_pieces[i][1] == dim_pieces[j][1]) or
                (dim_pieces[i][0] == dim_pieces[j][1] and dim_pieces[i][1] == dim_pieces[j][0])):
                #if that's so assign a position relative to the two
                no_simmetry.append(And(bl_corner[i][0] <= bl_corner[j][0],
                                        Implies(bl_corner[i][0] == bl_corner[j][0],
                                                bl_corner[i][1] <= bl_corner[j][1])))
    constraints += no_simmetry
    constraints += no_overlap
    
    # Implied constraint as requested in the second point 
    implied = []
    for i in range(w):
        for j in range(pieces):
            implied.append( Sum(
                [If(And(bl_corner[j][0] <= i, i < bl_corner[j][0] + dim_pieces[j][0]),
                                    dim_pieces[j][1],0) for j in range(pieces)]) <= h)

    for i in range(h):
        for j in range(pieces):
            implied.append(Sum(
                [If(And( bl_corner[j][1] <= i, i < bl_corner[j][1] + dim_pieces[j][1]), 
                                    dim_pieces[j][0],0) for j in range(pieces)]) <= w)

    solver = Solver()
    solver.add(constraints)
    if solver.check() == sat:

        m = solver.model()

        printer(m, 
                dim_pieces, 
                bl_corner,
                h, 
                w, 
                pieces, 
                solver,
                # If you want to save the solution uncomment this parameter and specify the path in output_dir variable
                #file = join(output_dir,filename).replace(".txt", "-out.txt"),
                rotation = False,
                solution = True,
                statistics = False
                console_output = True )
    else:
        print("Not satisfiable")

