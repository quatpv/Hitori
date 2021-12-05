import numpy as np

class Checker:
    def __init__(self, rows, colums, data, paint):
        self.rows = rows
        self.colums = colums
        self.data = data
        self.paint = paint
        self.result = None

    def check_rule_01(self, arr):
        # In rows
        for k in range(self.rows):
            for i in range(self.colums):
                for j in range(i+1, self.colums):
                    if self.data[k][i] == self.data[k][j] and self.paint[k][i] != 1 and self.paint[k][j] != 1:
                        arr[k][i] = True
                        arr[k][j] = True
                        return False, arr

        # In colums
        for k in range(self.colums):
            for i in range(self.rows):
                for j in range(i+1, self.rows):
                    if self.data[i][k] == self.data[j][k] and self.paint[i][k] != 1 and self.paint[j][k] != 1:
                        arr[i][k] = True
                        arr[j][k] = True
                        return False, arr
        return True, arr

    def check_rule_02(self, arr):
        for i in range(self.rows):
            for j in range(i+1, self.colums):
                if i+1 < self.rows and self.paint[i][j] == 1 and self.paint[i+1][j] == 1:
                    arr[i][j] = True
                    arr[i+1][j] = True
                    return False, arr
                
                if j+1 < self.colums and self.paint[i][j] == 1 and self.paint[i][j+1] == 1:
                    arr[i][j] = True
                    arr[i][j+1] = True
                    return False, arr
                
        return True, arr

    def find_cus(self, x, y, arr):
        if self.paint[x][y] == 1 or arr[x][y] == True:
            return arr

        arr[x][y] = True
        if x+1 >= 0 and x+1 < self.rows:
            self.find_cus(x+1, y, arr)

        if x-1 >= 0 and x-1 < self.rows:
            self.find_cus(x-1, y, arr)

        if y+1 >= 0 and y+1 < self.columns:
            self.find_cus(x, y+1, arr)
        
        if y-1 >= 0 and y-1 < self.columns:
            self.find_cus(x, y-1, arr)

    def check_rule_03(self, arr):
        if self.paint[0][0] != 1:
            arr = self.find_cus(0, 0, arr)
        else:
            arr = self.find_cus(0, 1, arr)
        
        margin = True
        for i in range(self.rows):
            for j in range(self.columns):
                if (self.paint[i][j] == 1 and arr[i][j] == True) or (self.paint[i][j] != 1 and arr[i][j] == False):
                    margin = False
        
        return margin, arr

    def check_all_rule(self):
        arr = np.full((self.rows, self.columns), False, dtype=bool)

        arr, check01 = self.check_rule_01(arr)
        if check01:
            self.result = arr
            return False

        arr, check02 = self.check_rule_02(arr)
        if check02:
            self.result = arr
            return False

        arr, check03 = self.check_rule_03(arr)
        if check03:
            self.result = arr
            return False

        return True
    
    def get_result(self):
        return self.result
