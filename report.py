from solver.hitory import HirotySAT
import json
from solver.support import *
import glob

configs = json.load(open('configs.json', 'r'))

def hitory_solver(n, value, configs, method):
    rows = n
    columns = n
    alg = HirotySAT(rows, columns, value, configs, method=method)
    alg.encode()
    alg.decode()

    if alg.satisfiable:
        # print("running time: ", alg.running_time)
        # print(alg.number_of_clauses)
        # print(alg.number_of_variables)
        print(f'{n}\t{alg.number_of_variables}\t{alg.number_of_clauses}\t{alg.running_time}')
        # print(alg.result)
    else:
        print("No solution")

if __name__ == '__main__':
    method = 'CC'
    for map_file in sorted(glob.glob('map/*.ma')):
        n, value = read_map(map_file)
        if n >= 20:
            continue
        hitory_solver(n, value, configs, method)
