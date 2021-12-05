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
        self.running_time = 0

    def get_color(self, output):
        result = np.full((self.rows, self.columns), True, dtype=bool)
        for k in output:
            positive = int(k) > 0
            k = abs(int(k))
            if positive:
                result[(k-1) // self.columns][(k-1) % self.columns] = True
            else: 
                result[(k-1) // self.columns][(k-1) % self.columns] = False
        
        return result

    def encode(self):
        if self.method == 'CC' or self.method == "ChainAndCircle":
            alg = chain_and_circle.ChainAndCircle(self.rows, self.columns, self.value, self.solver)
            alg.encode_vars()
            alg.cnf_rule_01()
            alg.cnf_rule_02()
            alg.cnf_rule_03()
            # print()
            # print()
            # with open()

        elif self.method == 'CE' or self.method == "ConnectivityEncoding":
            solver = sat.MINISAT()
            connectivity_encoding.ConnectivityEncoding(self.rows, self.columns, solver)

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
        start_time = time.time()
        os.system(command)
        self.running_time = time.time() - start_time
        
        with open(self.configs['cnf_out'], 'r') as cnf_out:
            lines = [line.strip() for line in cnf_out.readlines()]
        
        output = lines[1].split(" ")[:-1]
        self.result = self.get_color(output)
    


    
