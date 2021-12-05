from solver.hitory import HirotySAT
import json

configs = json.load(open('configs.json', 'r'))

n = 14
# value = [[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2], [4, 1, 2, 1]]
value = [[13,9,12,6,8,2,3,1,4,10,7,13,11,3],[6,13,5,13,1,1,12,8,12,3,14,7,14,10],[1,14,3,11,13,7,13,6,9,1,12,5,2,8],[8,4,12,1,3,11,14,1,13,12,2,1,6,4],[14,10,13,7,9,8,6,2,5,11,8,1,12,4],[3,11,14,8,1,4,7,3,8,12,9,10,13,5],[11,14,10,4,6,3,3,1,2,8,5,12,9,1],[5,1,4,12,14,8,13,7,10,2,13,6,3,9],[9,1,8,2,4,12,1,14,14,6,3,10,7,5],[3,12,1,9,13,5,8,4,7,5,10,8,14,6],[10,6,9,3,5,4,2,12,1,7,5,11,8,14],[8,3,10,14,2,10,13,7,12,1,1,8,5,11],[3,5,2,10,12,3,9,5,13,14,11,4,1,7],[12,8,11,10,7,1,11,14,3,9,6,5,10,10]]
method = 'CC'


def hitory_solver(n, value, configs, method):
    rows = n
    columns = n
    alg = HirotySAT(rows, columns, value, configs, method=method)
    alg.encode()
    alg.decode()

    print("running time: ", alg.running_time)
    print(alg.result)

if __name__ == '__main__':
    hitory_solver(n, value, configs, method)
