def printer(m, dim_pieces, bl_corner, h, w, pieces,  file = None, solution = True, rotation = False, statistics = False, console_output = True):
    with open(file, "a") as out:
        if solution:
            if True:
                print("{} {}".format(h, w))
                print("{}".format(pieces))
            if file is not None:
                out.write("{} {}\n".format(h, w))
                out.write("{}\n".format(pieces))

            for i in range(pieces):
                if console_output:
                    print("{:<1} {:<3} {:<1} {:<2}\n".format(dim_pieces[i][0], dim_pieces[i][1], str(m[bl_corner[i][0]]), str(m[bl_corner[i][1]])))
                if file is not None:
                    if rotation:
                        out.write("{:<1} {:<3} {:<1} {:<2}\n".format(str(m[dim_pieces[i][0]]), str(m[dim_pieces[i][1]]), str(m[bl_corner[i][0]]), str(m[bl_corner[i][1]])))
                    else:
                        out.write("{:<1} {:<3} {:<1} {:<2}\n".format(dim_pieces[i][0], dim_pieces[i][1], str(m[bl_corner[i][0]]), str(m[bl_corner[i][1]])))


        if statistics:
            if console_output:
                print("{}\n".format(solver.statistics()))
            if file is not None:
                out.write("{}\n".format(solver.statistics()))
