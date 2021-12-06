def read_map(input_file):
    n = int(input_file[input_file.rfind('/') + 1:].split('x')[0])
    value = []
    with open(input_file, 'r') as f:
        m = int(f.readline().strip())
        for i in range(m):
            id = f.readline()
            for j in range(n):
                line = [int(x) for x in f.readline().strip().split('\t')]
                value.append(line)
            break
    return n, value

def get_index(a, v):
    if v in a:
        return a.index(v)
    else:
        return -1