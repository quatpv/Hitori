from solver.hitory import HirotySAT
import json
import time

configs = json.load(open('configs.json', 'r'))

n = 4
value = [[2,2,2,2],[2,2,2,3],[2,3,2,1],[3,4,1,2]]
method = 'CC'


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
        print("running time: ", running_time)
        print("number_of_clauses: ", alg.number_of_clauses)
        print("number_of_variables: ", alg.number_of_variables)
        print(alg.result)
    else:
        print("No solution")

if __name__ == '__main__':
    hitory_solver(n, value, configs, method)
