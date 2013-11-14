# coding=utf-8
'''
Created on 2013-11-13
解决数独的问题
@author: gudh
'''
# 测试1
matrix = [
          [0, 2, 6, 4, 0, 3, 7, 0, 0],
          [0, 5, 1, 6, 0, 0, 0, 3, 8],
          [0, 7, 3, 0, 8, 0, 2, 0, 9],
          [2, 0, 5, 9, 0, 4, 0, 0, 0],
          [1, 9, 8, 2, 5, 0, 3, 4, 0],
          [0, 0, 7, 8, 6, 1, 0, 2, 0],
          [6, 3, 0, 5, 2, 0, 1, 0, 4],
          [7, 8, 4, 3, 1, 0, 5, 9, 0],
          [0, 1, 0, 7, 0, 9, 6, 0, 0]
          ]
# 测试2
matrix = [
          [6, 4, 0, 0, 0, 7, 3, 0, 1],
          [5, 2, 9, 1, 3, 4, 0, 0, 0],
          [3, 1, 7, 5, 0, 6, 9, 0, 0],
          [0, 5, 0, 0, 9, 2, 0, 4, 8],
          [0, 3, 2, 0, 1, 5, 6, 7, 9],
          [0, 0, 4, 7, 6, 8, 0, 3, 0],
          [0, 0, 0, 0, 0, 1, 8, 0, 2],
          [9, 8, 0, 2, 0, 3, 5, 0, 0],
          [2, 6, 0, 8, 7, 0, 4, 1, 0]
          ]

matrix = [
          [8, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 6, 0, 0, 0, 0, 0, 2],
          [3, 0, 0, 7, 0, 0, 0, 8, 6],
          [4, 5, 0, 0, 0, 0, 6, 0, 0],
          [0, 0, 9, 0, 8, 5, 0, 2, 0],
          [0, 0, 2, 6, 3, 0, 0, 0, 0],
          [0, 7, 4, 0, 0, 2, 0, 0, 0],
          [0, 0, 0, 0, 9, 0, 0, 0, 8],
          [0, 0, 3, 5, 0, 0, 0, 7, 0]
          ]

def print_matrix():
    for line in matrix:
        print line

def is_avail(x, y, v):
    # 横竖是否存在满足
    for i in range (9):
        if matrix[x][i] == v:
            return False
        if matrix[i][y] == v:
            return False
    
    # 同一9宫格是否满足
    xx = x / 3
    yy = y / 3
    for i in range(xx * 3, xx * 3 + 3):
        for j in range(yy * 3, yy * 3 + 3):
            if i == x and j == y:
                continue
            if matrix[i][j] == v:
                return False
            
    return True

def is_right(x, y, v):
    xx = x / 3
    yy = y / 3
    for i in range(xx * 3, xx * 3 + 3):
        for j in range(yy * 3, yy * 3 + 3):
            if i == x and j == y:
                continue
            if matrix[i][j] == 0 and is_avail(i, j, v):
                return False
    return True

def deal_loc(x, y):
    for i in range(1, 10):
        if is_avail(x, y, i) and is_right(x, y, i):
            print "set", x + 1, y + 1, i
            matrix[x][y] = i
            return True
    return False

def step():
    for x in range(9):
        for y in range(9):
            if matrix[x][y] == 0 and deal_loc(x, y):
                return True
    return False

if __name__ == '__main__':
    count = 0
    while True:
        # print_matrix()
        count += 1
        x = raw_input(str(count) + ' ===========: ' )
        xm = x.split(" ")
        if len(xm) == 3:
            matrix[int(xm[0])][int(xm[1])] = int(xm[2])
            print_matrix()
        step()
    
