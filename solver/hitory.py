import numpy as np
import time
from solver import chain_and_circle, connectivity_encoding, sat
import os

class HirotySAT():
    def __init__(self, rows, columns, value, configs, method='CC'):
        self.rows = rows
        self.columns = columns
        self.configs = configs
        self.value = value
        self.result = np.full((self.rows, self.columns), False, dtype=bool)
        self.solver = sat.MINISAT()
        self.method = method
        self.number_of_variables = 0
        self.number_of_clauses = 0
        self.max_var_in_borad = 0
        self.white = 0
        self.satisfiable = False

    def get_color_cc(self, output):
        result = np.full((self.rows, self.columns), True, dtype=bool)
        for k in output:
            positive = int(k) > 0
            k = abs(int(k))
            if positive:
                result[(k-1) // self.columns][(k-1) % self.columns] = True
            else: 
                result[(k-1) // self.columns][(k-1) % self.columns] = False
        
        return result
    

    def get_color_ce(self, arr, max_var_in_borad, white):
        result = np.full((self.rows, self.columns), True, dtype=bool)
        leng = len(arr)
        for d in range(leng):
            k = int(arr[d])
            if k == 0 or k > max_var_in_borad or k < -1*max_var_in_borad:
                break
            for i in range(self.rows):
                for j in range(self.columns):
                    if white[i][j] == -k:
                        result[i][j] = False
                        break
        return result

    def encode(self):
        if self.method == 'CC' or self.method == "ChainAndCircle":
            alg = chain_and_circle.ChainAndCircle(self.rows, self.columns, self.value, self.solver)
            alg.encode_vars()
            alg.cnf_rule_01()
            alg.cnf_rule_02()
            alg.cnf_rule_03()

        elif self.method == 'CE' or self.method == "ConnectivityEncoding":
            alg = connectivity_encoding.ConnectivityEncoding(self.rows, self.columns, self.value, self.solver)
            alg.encode_vars()
            alg.cnf_rule_01()
            alg.cnf_rule_02()
            alg.cnf_rule_03()
            self.max_var_in_borad = alg.max_var_in_borad
            self.white = alg.white

        self.number_of_variables = alg.get_number_of_variables()
        self.number_of_clauses = self.solver.get_number_of_clauses()

        with open(self.configs['cnf_in'], 'w') as cnf_in:
            cnf_in.write(f'p cnf {alg.get_number_of_variables()} {self.solver.get_number_of_clauses()}\n')
            for clause in self.solver.clauses:
                for i in clause:
                    cnf_in.write(f'{i} ')
                cnf_in.write(f'0\n')
        
    def decode(self):
        command = f"minisat {self.configs['cnf_in']} {self.configs['cnf_out']}"
        os.system(command)
        
        if self.method == 'CC':
            with open(self.configs['cnf_out'], 'r') as cnf_out:
                lines = [line.strip() for line in cnf_out.readlines()]
            if len(lines) > 1:
                self.satisfiable = True
                output = lines[1].split(" ")[:-1]
                self.result = self.get_color_cc(output)
            else:
                self.satisfiable = False

        elif self.method == 'CE':
            with open(self.configs['cnf_out'], 'r') as cnf_out:
                lines = [line.strip() for line in cnf_out.readlines()]
            if len(lines) > 1:
                self.satisfiable = True
                output = lines[1].split(" ")[:-1]
                self.result = self.get_color_ce(output, self.max_var_in_borad, self.white)
            else:
                self.satisfiable = False

            
