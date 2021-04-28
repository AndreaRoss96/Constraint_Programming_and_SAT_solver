import pandas as pd
import numpy as np
from os import listdir
from os.path import join, isfile
from statistics import mean, stdev
tr = 4


# Rotation
dazone ="D:\\Uni\\2020-21 2 sem\\opt\\Constraint_Programming_and_Sat_solver\\SMT\\time_rotation_no_implied\\"
out ="D:\\Uni\\2020-21 2 sem\\opt\\Constraint_Programming_and_Sat_solver\\SMT\\analisys_tr.txt"
'''


#Static implied
dazone ="D:\\Uni\\2020-21 2 sem\\opt\\Constraint_Programming_and_Sat_solver\\SMT\\times_static\\"
out ="D:\\Uni\\2020-21 2 sem\\opt\\Constraint_Programming_and_Sat_solver\\SMT\\analisys_tsi.txt"
'''
'''
#Static not implied
dazone ="D:\\Uni\\2020-21 2 sem\\opt\\Constraint_Programming_and_Sat_solver\\SMT\\time_static_no_implied\\"
out ="D:\\Uni\\2020-21 2 sem\\opt\\Constraint_Programming_and_Sat_solver\\SMT\\analisys_ts.txt"
'''

files = [filename for filename in listdir(dazone) if isfile(join(dazone, filename))]

f = lambda x: float(x.replace("\n", ""))

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

for filename in files:
    with open(join(dazone, filename), "r") as input:
        a = input.readlines()
        b = list(map(f, a))
    with open(out, "a") as output:
        try:
            output.write(filename[:5] +" & " + str(truncate(mean(b), tr)) +" & " + str(truncate(stdev(b),tr)) + "\n")
            print(filename + " statistics mean: " + str(truncate(mean(b),tr)) +", std: " + str(truncate(stdev(b),tr)) )
        except:
            output.write(filename[:5] +" & " + str(truncate(mean(b), tr)) +" & " + " ----- " + "\n")
            print(filename + " statistics mean: " + str(truncate(mean(b),tr)) +", std: None" )

