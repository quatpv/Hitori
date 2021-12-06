from solver.hitory import HirotySAT
import json
from solver.support import *
from tqdm import tqdm
import time


configs = json.load(open('configs.json', 'r'))

def hitory_solver(n, value, configs, method):
    rows = n
    columns = n
    start_time = time.time()
    alg = HirotySAT(rows, columns, value, configs, method=method)
    alg.encode()
    alg.decode()
    end_time = time.time()
    running_time = end_time - start_time

    if alg.satisfiable:
        # print("running time: ", alg.running_time)
        # print(alg.number_of_clauses)
        # print(alg.number_of_variables)
        print(f'{n}\t{alg.number_of_variables}\t{alg.number_of_clauses}\t{running_time}')
        # print(alg.result)
    else:
        print("No solution")

if __name__ == '__main__':
    method = 'CE'
    # lis_map = ['4x4.ma', '5x5.ma', '6x6.ma', '7x7.ma', '8x8.ma', '9x9.ma', '10x10.ma', '11x11.ma', '12x12.ma', '13x13.ma', '14x14.ma', '15x15.ma', '16x16.ma', '17x17.ma', '20x20.ma', '22x22.ma', '23x23.ma', '24x24.ma', '25x25.ma', '26x26.ma', '27x27.ma', '28x28.ma', '30x30.ma', '36x36.ma', '48x48.ma']
    lis_map = ['15x15.ma']
    for map_file in tqdm(lis_map):
        map_file = f'map/{map_file}'
        n, value = read_map(map_file)
        hitory_solver(n, value, configs, method)
