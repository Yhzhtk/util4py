# -*- coding: utf-8 -*-

import re

regs = ["有限公司", "科技", "分公司", "公司", "股份", "责任", "全称", "技术"];
regs.extend(["上海市", "北京市", "广州市", "深圳市", "杭州市", "上海", "北京", "广州", "深圳", "杭州"])
regs.extend(["&nbsp;", r"^\s*", r"\(.*$", r"（.*$", r"^[\da-zA-Z \.,]*$"])
regs.extend(["信息", "服务", "管理"])
regcs = [re.compile(reg, re.DOTALL) for reg in regs]

def rematch(src):
    for reg in regcs:
        src = re.sub(reg, "", src)
    src = src.strip()
    return src

def filters(inFile, outFile):
    f = open(inFile)
    fo = open(outFile, "w")
    i = 0
    while True:
        l = f.readline()
        if len(l) == 0:
            break;
        l = rematch(l)
        if len(l) > 2 and len(l) < 100:
            fo.write(l + "\n")
    f.close()
    fo.close()


filters("d:/cout.txt", "d:/exat.txt")
