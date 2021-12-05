import numpy as np
    
class ConnectivityEncoding:
    def __init__(self, rows, columns, value_of_cell):
        self.rows = rows
        self.columns = columns
        self.value_of_cell = value_of_cell
        self.not_fix = np.full((self.rows, self.columns), False, dtype=bool)
        self.zones = np.full((self.rows, self.columns), 0, dtype=int)
        self.path = np.full((self.rows, self.columns, self.rows, self.columns), 0, dtype=int)


    def encode_var(self):
        for i in range(self.rows):                       
            for j in range(self.columns):            
                for k in range(j+1, self.columns):
                    if self.value_of_cell[i][j] == self.value_of_cell[i][k]:
                        self.not_fix[i][j] = True
                        self.not_fix[i][k] = True


        for j in range(self.colums):
            for i in range(self.rows - 1):
                for k in range(i+1, self.rows):
                    if self.value_of_cell[i][j] == self.value_of_cell[k][j]:
                        self.not_fix[i][j] = True
                        self.not_fix[k][j] = True


        # var of board
        number_of_vars = 0
        self.white = np.full((self.rows, self.columns), 0, dtype=int)
        for i in range(self.rows):
            for j in range(self.colums):
                if self.not_fix[i][j]:
                    number_of_vars += 1
                    self.white[i][j] = number_of_vars
                    
        self.max_var_in_borad = number_of_vars

        # zones
        zone_number = 0

        for i in range(self.rows):
            for j in range(self.colums):
                if self.not_fix[i][j] and self.zones[i][j] == 0:
                    zone_number += 1
                    self.find_zone(i,j,zone_number)
        
        # set path
        for i in range(self.rows):
            for j in range(self.colums):
                for k in range(self.rows):
                    for h in range(self.columns):
                        if self.zones[i][j] != 0 and self.zones[i][j] == self.zones[k][h] and self.path[i][j][k][h] == 0:
                            number_of_vars += 1
                            self.path[i][j][k][h] = number_of_vars


    def find_zone(self, i, j, zone_number):
        self.zones[i][j] = zone_number
        if i+1 < self.rows and j+1 < self.columns and self.not_fix[i+1][j+1] and self.zones[i+1][j+1] == 0:
            self.find_zone(i+1, j+1, zone_number)
        if i-1 >= 0 and j+1 < self.columns and self.not_fix[i-1][j+1] and self.zones[i-1][j+1] == 0:
            self.find_zone(i-1, j+1, zone_number)
        if i+1 < self.rows and j-1 >= 0 and self.not_fix[i+1][j-1] and self.zones[i+1][j-1] == 0:
            self.find_zone(i+1, j-1, zone_number)
        if i-1 >= 0 and j-1 >= 0 and self.not_fix[i-1][j-1] and self.zones[i-1][j-1] == 0:
            self.find_zone(i-1, j-1, zone_number)
    
    def in_matrix(self, x, y):
        return x >= 0 and x < self.rows and y >= 0 and y < self.columns
    
    def diff(self, x, y, a, b):
        return x!=a or y!=b

    # CNF Rule 1
    def cnf_rule_01(self):
        for i in range(self.rows):
            for j in range(self.columns):
                for k in range(j+1, self.columns):
                    if self.value_of_cell[i][j] == self.value_of_cell[i][k]:
                        self.solver.add_a_clause(-1 * self.white[i][j], -1*self.white[i][k])
        
        for j in range(self.colums):
            for i in range(self.rows - 1):
                for k in range(i+1, self.rows):
                    if self.value_of_cell[i][j] == self.value_of_cell[k][j]:
                        self.solver.add_a_clause(-1*self.white[i][j],-1*self.white[k][j])
    
    # CNF Rule 2
    def cnf_rule_02(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.not_fix[i][j]:         
                    if i-1 >= 0 and self.not_fix[i-1][j]:
                        self.solver.add_a_clause(self.white[i][j], self.white[i-1][j])

                    if j-1 >= 0 and self.not_fix[i][j-1]:
                        self.solver.add_a_clause(self.white[i][j],self.white[i][j-1])
    
    # Rule 3
    def cnf_rule_03(self):
        # (x,y) Bien thi di vao trong
        for i in range(self.rows):
            for j in range(self.columns):
                if self.not_fix[i][j]:
                    self.solver.add_a_clause(-self.path[i][j][i][j])
                
                if self.in_matrix(i+1, j+1) and self.not_fix[i+1][j+1]:
                    if i == 0 or i == self.rows-1 or j == 0 or j == self.columns-1:
                        self.solver.add_a_clause(
                            self.white[i][j], self.white[i+1][j+1], self.path[i][j][i+1][j+1])
                        
                    elif i+1 == 0 or i+1 == self.rows-1 or j+1 == 0 or j+1 == self.columns-1:
                        self.solver.add_a_clause(
                            self.white[i][j], self.white[i+1][j+1], self.path[i+1][j+1][i][j])
                    else:
                        self.solver.add_a_clause(
                            self.white[i][j], self.white[i+1][j+1], self.path[i][j][i+1][j+1], self.path[i+1][j+1][i][j])
                
                if self.in_matrix(i+1, j-1) and self.not_fix[i+1][j-1]:
                    if i == 0 or i == self.rows-1 or j == 0 or j == self.columns-1:
                        self.solver.add_a_clause(
                            self.white[i][j], self.white[i+1][j-1], self.path[i][j][i+1][j-1])

                    if i+1 == 0 or i+1 == self.rows-1 or j-1 == 0 or j-1 == self.columns-1:
                        self.solver.add_a_clause(
                            self.white[i][j], self.white[i+1][j-1], self.path[i+1][j-1][i][j])

                    if i > 0 and i < self.rows-1 and j > 0 and j < self.columns-1 and i+1 > 0 and i+1 < self.rows-1 and j-1 > 0 and j-1 < self.columns-1:
                        self.solver.add_a_clause(
                            self.white[i][j], self.white[i+1][j-1], self.path[i][j][i+1][j-1], self.path[i+1][j-1][i][j])

        for i in range(self.rows):
            for j in range(self.columns):
                if self.not_fix[i][j]:
                    if self.in_matrix(i+1, j+1) and self.in_matrix(i+1, j-1) and self.not_fix[i+1][j+1] and self.not_fix[i+1][j-1]:
                        self.solver.add_a_clause(-self.path[i+1]
                                                 [j+1][i][j], -self.path[i+1][j-1][i][j])
                    if self.in_matrix(i+1, j+1) and self.in_matrix(i-1, j+1) and self.not_fix[i+1][j+1] and self.not_fix[i-1][j+1]:
                        self.solver.add_a_clause(-self.path[i+1]
                                                 [j+1][i][j], -self.path[i-1][j+1][i][j])
                    if self.in_matrix(i+1, j+1) and self.in_matrix(i-1, j-1) and self.not_fix[i+1][j+1] and self.not_fix[i-1][j-1]:
                        self.solver.add_a_clause(-self.path[i+1]
                                                 [j+1][i][j], -self.path[i-1][j-1][i][j])
                    if self.in_matrix(i+1, j-1) and self.in_matrix(i-1, j-1) and self.not_fix[i+1][j-1] and self.not_fix[i-1][j-1]:
                        self.solver.add_a_clause(-self.path[i+1]
                                                 [j-1][i][j], -self.path[i-1][j-1][i][j])
                    if self.in_matrix(i+1, j-1) and self.in_matrix(i-1, j+1) and self.not_fix[i+1][j-1] and self.not_fix[i-1][j+1]:
                        self.solver.add_a_clause(-self.path[i+1]
                                                 [j-1][i][j], -self.path[i-1][j+1][i][j])
                    if self.in_matrix(i-1, j+1) and self.in_matrix(i-1, j-1) and self.not_fix[i-1][j+1] and self.not_fix[i-1][j-1]:
                        self.solver.add_a_clause(-self.path[i-1]
                                                 [j+1][i][j], -self.path[i-1][j-1][i][j])

        # Path(x,y,a,b) and Path(a,b,a+1,b+1)=> Path(x,y,a+1,b+1) and 
        for i in range(self.rows):
            for j in range(self.columns):
                for k in range(self.rows):
                    for h in range(self.columns):
                        if self.diff(i, j, k, h) and self.self.zones[k][h] == self.self.zones[i][j] and self.self.zones[i][j] != 0:
                            if self.in_matrix(k+1, h+1) and self.zones[k+1][h+1] == self.self.zones[i][j]:
                                self.solver.add_a_clause(
                                    -self.self.path[i][j][k][h], -self.path[k][h][k+1][h+1], self.path[i][j][k+1][h+1])
                            if self.in_matrix(k+1, h-1) and self.zones[k+1][h-1] == self.self.zones[i][j]:
                                self.solver.add_a_clause(
                                    -self.self.path[i][j][k][h], -self.path[k][h][k+1][h-1], self.path[i][j][k+1][h-1])
                            if self.in_matrix(k-1, h+1) and self.zones[k-1][h+1] == self.self.zones[i][j]:
                                self.solver.add_a_clause(
                                    -self.self.path[i][j][k][h], -self.path[k][h][k-1][h+1], self.path[i][j][k-1][h+1])
                            if self.in_matrix(k-1, h-1) and self.zones[k-1][h-1] == self.self.zones[i][j]:
                                self.solver.add_a_clause(
                                    -self.self.path[i][j][k][h], -self.path[k][h][k-1][h-1], self.path[i][j][k-1][h-1])

    def insert_a_clause(self):
        self.number_of_clauses += 1
        leng = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.not_fix[i][j]:
                    leng+=1

        arr = np.full(leng, 0, dtype=int)
        leng = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.not_fix[i][j]:
                    if self.result[i][j]:
                        arr[leng] = -1*self.white[i][j]
                        leng += 1
                    else:
                        arr[leng] = self.white[i][j]
                        leng += 1
        return self.solver.add_a_clause_to_more(self.number_of_vars, arr)
    
    def decode(self, arr):
        leng = len(arr)
        for d in range(leng):
            k = arr[d]
            if k == 0 or k > self.max_var_in_borad or k < -1*self.max_var_in_borad:
                break
            for i in range(self.rows):
                for j in range(self.colums):
                    if self.white[i][j] == -k:
                        self.result[i][j] = False
                        break
        return True