from os import listdir
from os.path import join, isfile
import numpy as np
from z3 import And, Or, Int, If, Solver, sat, Implies 
output_dir ="D:\\Uni\\2020-21 2 sem\\opt\\Constraint_Programming_and_Sat_solver\\SMT\\out_static\\"
dazone = "D:\\Uni\\2020-21 2 sem\\opt\\Constraint_Programming_and_Sat_solver\\all_the_rest"
files = [filename for filename in listdir(dazone) if isfile(join(dazone, filename))]
for i in range(5):
    for filename in files:
        dim_pieces = []
        with open(join(dazone, filename), "r") as input:
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

        # This constraint is used to impose a no overlap condition so that the pieces occupy a different spaces
        no_overlap = []
        for i in range(pieces):
            for j in range(i,pieces):
                #given the squares p0, p1 we check that one of the following condition applies:
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

        '''
        for i in range(pieces):
            for j in range(i, pieces):
                #check if two pieces have the same dimention or can be rotated to have that
                if( (dim_pieces[i][0] == dim_pieces[j][0] and dim_pieces[i][1] == dim_pieces[j][1]) or
                    (dim_pieces[i][0] == dim_pieces[j][1] and dim_pieces[i][1] == dim_pieces[j][0])):
                    #if that's so assign a position relative to the two
                    no_simmetry.append(And(bl_corner[i][0] <= bl_corner[j][0],
                                            Implies(bl_corner[i][0] == bl_corner[j][0],
                                                    bl_corner[i][1] <= bl_corner[j][1])))
        constraints += no_simmetry
        '''
        #Implied constraint helps the solver with a different approach 
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

        solver = Solver()
        solver.add(constraints)
        if solver.check() == sat:

            m = solver.model()

            print("{} {}".format(h, w))
            with open(join(output_dir,filename), "a") as out:
                '''    
                for i in range(pieces):
                    print("{:<1} {:<3} {:<1} {:<2}".format(dim_pieces[i][0], dim_pieces[i][1], str(m[bl_corner[i][0]]), str(m[bl_corner[i][1]])))
                    out.write("{:<1} {:<3} {:<1} {:<2}\n".format(dim_pieces[i][0], dim_pieces[i][1], str(m[bl_corner[i][0]]), str(m[bl_corner[i][1]])))
                '''
                #for this iteraction I just want to save the statistics
                out.write("\n {}".format(solver.statistics()))
        else:
            print("STO VOLANDO")
