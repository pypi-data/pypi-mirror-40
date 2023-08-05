

def read(fileName):
    file = open(fileName)
    lines = []
    for line in file:
        lines.append(line)
    return lines

def read(file, data):
    lines = []
    for line in file:
        for d in data:
            if(d == line[0:len(s)]):
                lines.append(line)
    return lines

def getLineData(line, array):
    data = []
    begin = 0
    for i in array:
        data.append(line[begin:i])
        begin = i
    return data  

def generateMatrix(pos, lines, size = 1):
    matriz = []
    i = 0
    x = 1
    while(i < lines):
        l = []
        while(x <= pos):
            l.append(x)
            x = x + size
        i = i + 1
        matriz.append(l)
    return matriz

def lineString(line):
    return ''.join(map(str, line))
