import os
import numpy as np 

def process(user_path):
    dir_ = r"Instances\\"
    # r"../../Instances/"

    for filename in os.listdir(dir_):
        print(f'file name: {filename}')
        file_read = open(dir_+filename, 'r')
        first_line = file_read.readline().strip().split(" ") # find the dimansion of w and h
        sec_line = file_read.readline().strip().split(" ")  # number of pieces of paper
        remaining_lines = file_read.readlines() # pieces of paper theirselfes
        file_read.close()

        w = "w = " + first_line[0] + ";\n"
        h = "h = " + first_line[1] + ";\n"
        n_pieces = "n_pieces = " + sec_line[0] + ";\n"

        remaining_lines = [line.strip() for line in remaining_lines if line.strip()]

        # Processing of the remaining lines
        rectangles = "rectangles = ["
        # variables used by geost_bb
        rect_size = "rect_size = ["
        rect_offset = "rect_offset = ["
        shape = "shape = ["
        shape_index = "shape_index = ["
        
        couples = {}
        c = 1
        for i, line in enumerate(remaining_lines):
            couple = line.replace(" ", "").strip()
            rectangle = line.split(" ")
            rect_size += f"|{rectangle[0]}, {rectangle[1]}\n"
            rect_offset += f"|{str(0)}, {str(0)}\n"
            shape += "{" + str(i+c) + "}, "
            shape_index += "{" + str(i+c)# + "}, "
            if rectangle[0] != rectangle[1]:
                # If the rectangle is not a square then save this information
                shape_index += ", "
                c+=1
                rect_size += f"|{rectangle[1]}, {rectangle[0]}\n"
                rect_offset += f"|{str(0)}, {str(0)}\n"
                shape += "{" + str(i+c) + "}, "
                shape_index += str(i+c) + "}, "
            else :
                shape_index += "}, "
            rectangles += f"|{rectangle[0]}, {rectangle[1]}\n"
            couples[couple] = couples.get(couple,0) + 1
        
        rectangles += "|];\n"
        rect_size += "|];\n"
        rect_offset += "|];\n"
        shape = shape[:-2] + "];\n"
        shape_index = shape_index[:-2] + "];\n"

        rect_rep = "rect_rep = " # repetition of rectangles
        rect_rep_values = list(couples.values())
        rect_copies = np.array([list(couples.values())]).size

        print("couples:", rect_rep_values)

        coordinate_shapes = [0 if i == 1 else sum(rect_rep_values[:i-1]) for i in range(1,rect_copies+1)]

        rect_rep += str(rect_rep_values) + ";\n"
        coordinate_shapes = f"coordinate_shapes = {coordinate_shapes};\n"
        print(coordinate_shapes)

        #manca la print di w, h e n_pieces
        print(rectangles)
        print(rect_size)
        print(rect_offset)
        print(shape)
        print(shape_index)
        print(rect_rep)
        
        tmp_file = filename.strip().split(".")
        new_file = tmp_file[0] + ".dzn"
        rect_copies = f"rect_copies = {str(rect_copies)};\n"
        n_shapes = f"n_shapes = {str(len(remaining_lines)+c-1)};\n"
        
        writer(h,w,n_pieces,user_path,new_file,rectangles,
                    shape=shape,
                    shape_index=shape_index,
                    rect_rep=rect_rep,
                    rect_copies=rect_copies,
                    coordinate_shapes=str(coordinate_shapes),
                    n_shapes=n_shapes,
                    rect_size=rect_size,
                    rect_offset=rect_offset,
                    final_dir="general")
        writer(h,w,n_pieces,user_path,new_file,rectangles,
                    final_dir="base")

def writer(h,w,n_pieces,user_path,new_file, rectangles,
            shape=0,shape_index=0,rect_rep=0,rect_copies=0,
            coordinate_shapes=0,n_shapes=0,rect_size=0,
            rect_offset=0,final_dir="general"):
    file_read = open(r"" + user_path + "CP\\py_script\\"+ final_dir +"\\new_" + new_file, "w+")
    file_read.write(h)
    file_read.write(w)
    file_read.write(n_pieces)
    if final_dir=="general" :
        file_read.write(n_shapes)
        file_read.write(shape)
        file_read.write(shape_index)
        file_read.write(rect_rep)
        file_read.write(rect_copies)
        file_read.write(coordinate_shapes)
        file_read.write(rect_size)
        file_read.write(rect_offset)
    file_read.write(rectangles)
    file_read.close()
 
if __name__=="__main__":
    print("start")
    user_path = r"C:\\Users\\admin\\Desktop\\toGitHub\\Constraint_Programming_and_SAT_solver\\"
    process(user_path)