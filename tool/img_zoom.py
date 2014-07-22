# coding=utf-8
'''
压缩图片，相机图片太大了，批量压缩用
需要依赖PIL包：http://www.pythonware.com/products/pil/
'''
import Image,os

def get_size(img, s=1000):
    '''获取相对大小，s参数为宽高较大的一个数，另一个按比例计算'''
    i_size = img.size
    size = [1000, 750]
    if i_size[0] > i_size[1]:
        size[0] = s
        size[1] = int(s * i_size[1] / i_size[0])
    else:
        size[1] = s
        size[0] = int(s * i_size[0] / i_size[1])
    return tuple(size)
        

def zoom_img(src, dest, q=0.85):
    '''压缩一张图片'''
    img = Image.open(src)
    size = get_size(img)
    img = img.resize(size, Image.ANTIALIAS)
    img.save(dest)
    print "zoom: %s" % dest

def zoom_dir(src, dest):
    '''压缩路径'''
    for filename in os.listdir(src):
        if filename.endswith(('.jpg', '.bmp', '.png')):
            zoom_img(os.path.join(src, filename), os.path.join(dest, filename))

def zoom(src, dest):
    '''自动判断路径或者文件压缩'''
    if os.path.isdir(src):
        zoom_dir(src, dest)
    elif os.path.isfile(src):
        zoom_img(src, dest)


zoom(r"D:\xj", r"d:\s")
