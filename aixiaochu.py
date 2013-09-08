# encoding=utf-8
'''
Created on 2013-9-8

@author: gudh
'''

import Image

start_pos = (5, 222) # 开始的位置
block_size = (67, 67) # 块大小
rel_pos = (33, 28) # 相对块头位置
colors = (
(255, 255, 255), # 白
(164, 130, 213), # 紫
(247, 214, 82), # 黄
(244, 160, 90), # 土
(90, 186, 238), # 蓝
(247, 69, 95), # 红
(173, 235, 82) # 绿
)
colornames = ('白', '紫', '黄', '土', '蓝', '红', '绿')
ax = (30, 30, 30) # 允许的误差


def get_pix(img):
    '''获取测试开始位置，块大小'''
    m = 5
    n = 222 + 67
    x = 67
    for i in range(7):
        print "c%d = %s" % (i + 1, img.getpixel((m + i * x + 33, n + 20))[0:3])

def get_pos(i, j):
    '''获取块内判断的点'''
    x = start_pos[0] + i * block_size[0] + rel_pos[0]
    y = start_pos[1] + j * block_size[1] + rel_pos[1]
    return (x, y)

def get_block(i, j):
    '''获取块的区域'''
    x = start_pos[0] + i * block_size[0]
    y = start_pos[1] + j * block_size[1]
    w = x + block_size[0]
    h = y + block_size[1]
    return (x, y, w, h)

def similar_color(p, color):
    '''判断是否是相似'''
    print p, color
    for i in range(3):
        if abs(p[i] - color[i]) >= ax [i]:
            return False
    return True

def get_color(img, i, j):
    '''获取像素点的颜色'''
    p = get_pos(i, j)
    print p
    index = 0
    for index in range(len(colors)):
        if similar_color(img.getpixel(p), colors[index]):
            return index
    return -1

def get_pic_info(img):
    '''获取像素矩阵'''
    mat = []
    for j in range(7):
        mx = [] 
        for i in range(7):
            mx.append(colornames[get_color(img, i, j)])
        mat.append(mx)
    return mat

def cut_all(img):
    '''将所有单独的块截图保存'''
    for j in range(7):
        for i in range(7):
            b = get_block(i, j)
            im = img.crop(b)
            im.save("c:/m/%d%d.jpg" % (i, j), "JPEG")

if __name__ == "main":
    img = Image.open(r"c:/m.png")
    mat = get_pic_info(img)
    for m in mat:
        for n in m:
            print n,
        print 


