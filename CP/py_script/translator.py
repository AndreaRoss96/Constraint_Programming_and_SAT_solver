import os
import numpy as np 

dir_ = "..\\..\\Instances\\"

for filename in os.listdir(dir_):
    file_read = open(dir_+filename, 'r')


    first_line = file_read.readline().strip().split(" ") # find the dimansion of w and h
    w = "w = " + first_line[0] + ";\n"
    h = "h = " + first_line[1] + ";\n"

    sec_line = file_read.readline().strip().split(" ")  # number of pieces of paper
    n_pieces = "n_pieces = " + sec_line[0] + ";\n"

    remaining_lines = file_read.readlines()
    remaining_lines = [line.strip() for line in remaining_lines if line.strip()]	

    # Processing of the remaining lines
    sizes = "size = ["
    rect_size = "rect_size = [" # used in the general version 
    rect_offset = "rect_offset = ["
    shape = "shape = ["
    shapeind = "shapeind = ["
    i = 0
    
    ncopy = "ncopy = "
    couples = {}


    for line in remaining_lines:
        couple = line.replace(" ", "").strip()
        size = line.split(" ")
        if size[0] != size[1]:
            # If the rectangle is not a square then save this information
            i+=1
            rect_size += "|"+ size[0] + ", " + size[1] + "\n"
            rect_offset += "|"+ str(0) + ", " + str(0) + "\n"
            shape += "{" + str(i) + "}" + ", "
            shapeind += "{" + str(i) + ", "
            i+=1
            rect_size += "|"+ size[1] + ", " + size[0] + "\n"
            rect_offset += "|"+ str(0) + ", " + str(0) + "\n"
            shape += "{" + str(i) + "}" + ", "
            shapeind += str(i) + "}, "
        else:
            i+=1
            rect_size += "|"+ size[0] + ", " + size[1]  + "\n"
            rect_offset += "|"+ str(0) + ", " + str(0) + "\n"
            shape += "{" + str(i) + "}" + ", "
            shapeind += "{" + str(i) + "}, "
        sizes += "|"+ size[0] + ", " + size[1] + "\n"
        couples[couple] = couples.get(couple,0) + 1
    
    sizes += "|];\n"
    
    rect_size += "|];\n"
    rect_offset += "|];\n"
    shape = shape[:-2]
    shape += "];\n"
    shapeind = shapeind[:-2]
    shapeind += "];\n"
    
    ncopy += str(str(list(couples.values()))) + ";\n"
    #manca la print di w, h e n_pieces
    print(sizes)
    print(rect_size)
    print(rect_offset)
    print(shape)
    print(shapeind)
    print(ncopy)
    file_read.close()
    tmp_file = filename.strip().split(".")
    new_file = tmp_file[0] + ".dzn"
    file_read = open("general/g" + new_file, "w")
    file_read.write(h)
    file_read.write(w)
    file_read.write(n_pieces)
    file_read.write(sizes)
    file_read.write(rect_size)
    file_read.write(rect_offset)
    file_read.write(shape)
    file_read.write(shapeind)
    file_read.write(ncopy)

    file_read.write("c = " + str(np.array([list(couples.values())]).size) + ";\n")
    file_read.write("m = " + str(i) + ";\n")

    file_read.close() 