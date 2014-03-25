# -*- coding: utf-8 -*-

import re

regs = ["服务平台", "有限责任公司", "网络科技有限公司", "网络技术有限公司", "技术服务有限公司", "科技有限公司", "信息科技有限公司", "人才管理咨询", "人力资源有限公司", "信息服务有限公司", "文化传播有限公司", "电子商务有限公司", "企业管理咨询有限公司", "计算机科技有限公司", "传媒有限公司", "金融信息服务有限公司", "投资管理有限公司", "科技股份有限公司", "计算机科技发展有限公司", "数码科技有限公司", "文化咨询有限公司", "管理有限公司", "软件有限公司", "教育科技有限公司", "股份有限公司", "广告有限公司", "科技发展有限公司", "数码科技有限公司"]
regs.extend(["服务有限公司"])
regs.extend(["郑州市","重庆市","青岛市","北京市","天津市","南京市","广州市","上海市","深圳市","杭州市"])
regs.extend(["郑州","重庆","青岛","北京","天津","南京","广州","上海","深圳","杭州"])
regs.extend(["沈阳市","沈阳","武汉市","武汉","成都市","成都","广东"])
regs.extend(["有限公司", "科技", "分公司", "公司", "股份", "责任", "全称", "技术"]);
regs.extend(["信息", "服务", "管理"])
regs.extend(["&nbsp;", r"^\s*", r"\(.*$", r"（.*$", r"^[\da-zA-Z \.,\-\+]*$"])
regs.extend(["^请输入.*$", "^.*�.*$"])

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
        if len(l) > 2 and len(l) < 50:
            fo.write(l + "\n")
    f.close()
    fo.close()

filters("d:/newIn.txt", "d:/newOut.txt")
