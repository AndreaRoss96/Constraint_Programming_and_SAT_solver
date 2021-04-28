def printer(m, dim_pieces, bl_corner, h, w, pieces, solver, file = None, solution = True, rotation = False, statistics = False, console_output = True):
    # Print file
    if file is not None:
        with open(file, "a") as out:
            #out.write(str(solver.statistics().get_key_value("time")) + "\n")

            if solution:
                out.write("{} {}\n".format(h, w))
                out.write("{}\n".format(pieces))

                for i in range(pieces):
                    if rotation:
                        out.write("{:<1} {:<3} {:<1} {:<2}\n".format(str(m[dim_pieces[i][0]]), str(m[dim_pieces[i][1]]), str(m[bl_corner[i][0]]), str(m[bl_corner[i][1]])))
                    else:
                        out.write("{:<1} {:<3} {:<1} {:<2}\n".format(dim_pieces[i][0], dim_pieces[i][1], str(m[bl_corner[i][0]]), str(m[bl_corner[i][1]])))


            if statistics:
                out.write("{}\n".format(solver.statistics()))

    #Print console
    if console_output:
        #print("{} {}".format(h, w))
        #print("{}".format(pieces))
        print(str(solver.statistics().get_key_value("time")) + "\n")
        if solution:
            for i in range(pieces):
                if rotation:
                    print("{:<1} {:<3} {:<1} {:<2}\n".format(str(m[dim_pieces[i][0]]), str(m[dim_pieces[i][1]]), str(m[bl_corner[i][0]]), str(m[bl_corner[i][1]])))
                else:
                    print("{:<1} {:<3} {:<1} {:<2}\n".format(dim_pieces[i][0], dim_pieces[i][1], str(m[bl_corner[i][0]]), str(m[bl_corner[i][1]])))

        if statistics:
            print("{}\n".format(solver.statistics()))
