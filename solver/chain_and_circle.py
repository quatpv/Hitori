import numpy as np
from solver.support import *

class ChainAndCircle:
    def __init__(self, rows, columns, value, solver):
        self.rows = rows
        self.columns = columns
        self.value_of_cell = value
        self.is_able_paint = np.full((self.rows, self.columns), False, dtype=bool)
        self.solver = solver
        self.number_of_vars = self.rows * self.columns
        self.white = np.full((self.rows, self.columns), 0, dtype=int)

    def encode_vars(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.white[i][j] = i*self.columns + j + 1    

    # CNF Rule 1
    def cnf_rule_01(self):
        for i in range(self.rows):
            for j in range(self.columns-1):
                for k in range(j + 1, self.columns):
                    if self.value_of_cell[i][j] == self.value_of_cell[i][k]:
                    # tren mot hang khong the co 2 self.value_of_cell cung mot gia tri
                        self.solver.add_a_clause([-1 * self.white[i][j], -1*self.white[i][k]])
                        self.is_able_paint[i][j] = True
                        self.is_able_paint[i][k] = True

        for j in range(self.columns):
            for i in range(self.rows - 1):
                for k in range(i + 1, self.rows):
                    if self.value_of_cell[i][j] == self.value_of_cell[k][j]:
                        # Mot cot khong the co 2 o cung gia tri
                        self.solver.add_a_clause([-1 * self.white[i][j], -1*self.white[k][j]])
                        self.is_able_paint[i][j] = True
                        self.is_able_paint[k][j] = True

        # Tranh truong hop nhieu O khong nhat thiet phai xoa ma van xoa
        for i in range(self.rows):
            for j in range(self.columns):
                if not self.is_able_paint[i][j]:
                    self.solver.add_a_clause([self.white[i][j]])

    # CNF Rule 2
    def cnf_rule_02(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.is_able_paint[i][j]:
                    if i-1 >= 0 and self.is_able_paint[i-1][j]:
                        self.solver.add_a_clause([self.white[i][j], self.white[i-1][j]])

                    if j-1 >= 0 and self.is_able_paint[i][j-1]:
                        self.solver.add_a_clause([self.white[i][j], self.white[i][j-1]])

    # Tim nhung vong trong bang
    def find_cycle(self, x, y, cycle):
        if not (len(cycle) != 1 or y > (cycle[0]-1) % self.columns) or not (x >= 0 and x < self.rows and y >= 0 and y < self.columns) or not self.is_able_paint[x][y] or self.white[x][y] < cycle[0] or get_index(cycle, self.white[x][y]) >= 0:
            return cycle
        

        c = 0
        k = [0, 0, 0]

        for a in [-1, 1]:
            for b in [-1, 1]:
                if x+a >= 0 and x+a < self.rows and y+b >= 0 and y+b < self.columns and self.white[x+a][y+b] < len(cycle) and not cycle[len(cycle)-1] == self.white[x+a][y+b]:
                    k[c] = get_index(cycle, self.white[x+a][y+b])
                    c += 1

        for i in range(c):
            if k[i] > 0:
                return cycle

        for i in range(c):
            if k[i] == 0:
                ints = np.full(len(cycle) + 1, 0, dtype=int)
                for j in range(len(cycle)):
                   ints[j]=cycle[j]
                ints[len(cycle)] = self.white[x][y]
                self.solver.add_a_clause(ints)
                return cycle


        # Tiep tuc tim voi cac o tiep theo
        cycle.append(self.white[x][y])
        for a in [-1, 1]:
            for b in [-1, 1]:
                cycle = self.find_cycle(x+a, y+b, cycle)
        if cycle:
            if get_index(cycle, self.white[x][y]) >= 0:
                cycle.pop(get_index(cycle, self.white[x][y]))
        return cycle

    def find_chain(self, x, y, chain):
        if not (x >= 0 and x < self.rows and y >= 0 and y < self.columns) or not self.is_able_paint[x][y] or get_index(chain, self.white[x][y]) >= 0:
            return chain

        for a in [-1, 1]:
            for b in [-1, 1]:
                if x+a >= 0 and x+a < self.rows and y+b >= 0 and y+b < self.columns and not chain[len(chain)-1] == self.white[x+a][y+b]:
                    if get_index(chain, self.white[x+a][y+b]) >= 0:
                        return chain

        if (x == 0 or y == 0 or x == self.rows-1 or y == self.columns-1) and self.white[x][y] > chain[0]:
            ints = np.full(len(chain) + 1, 0, dtype=int)
            for i in range(len(chain)):
                    ints[i]=chain[i]
            ints[len(chain)] = self.white[x][y]
            self.solver.add_a_clause(ints)
            return chain
        
        chain.append(self.white[x][y])
        for a in [-1, 1]:
            for b in [-1, 1]:
                chain = self.find_chain(x+a, y+b, chain)

        if chain:
            if get_index(chain, self.white[x][y]) >= 0:
                chain.pop(get_index(chain, self.white[x][y]))
        return chain

    def find_cycle_tmp(self, x, y, cycle):
        if not self.is_able_paint[x][y]:
            return cycle
        cycle.append(self.white[x][y])
    
        for a in [-1, 1]:
            for b in [-1, 1]:
                cycle = self.find_cycle(x+a, y+b, cycle)
        if cycle:
            if get_index(cycle, self.white[x][y]) >= 0:
                cycle.pop(get_index(cycle, self.white[x][y]))
        return cycle

    def find_chain_tmp(self, x, y, chain):
        if not self.is_able_paint[x][y]:
            return chain
        chain.append(self.white[x][y])

        for a in [-1, 1]:
            for b in [-1, 1]:
                self.find_chain(x+a, y+b, chain)

        if chain:
            if get_index(chain, self.white[x][y]) >= 0:
                chain.pop(get_index(chain, self.white[x][y]))
        return chain


    # Rule 3
    def cnf_rule_03(self):
        cycle = []
        # bat dau tim cycle
        for i in range(self.rows):
            for j in range(self.columns):
                cycle = self.find_cycle_tmp(i, j, cycle)

        # tim chain voi nhung O bat dau o bien cua bang
        for i in range(self.rows):
            cycle = self.find_chain_tmp(i, 0, cycle)
            cycle = self.find_chain_tmp(i, self.columns-1, cycle)

        for j in range(1, self.columns - 1):
            cycle = self.find_chain_tmp(0, j, cycle)
            cycle = self.find_chain_tmp(self.rows-1, j, cycle)

    def get_result(self):
        return self.is_able_paint
    
    def get_number_of_variables(self):
        return self.number_of_vars