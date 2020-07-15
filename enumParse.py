#!/usr/bin/python
# -*- coding: UTF-8 -*-


def extractBrief(lines) :
    brief = ""

    for line in lines:

        if line.find("\\brief") != -1:
            brief += line[line.find('\\brief') + len('\\brief'):].strip()

        else :
            brief += line.strip('/\n ')
        brief +=' '
    return brief

def extractName(strs) :
    eles = strs.split()
    if eles[0] == "enum" and eles[1] == "class" :
        return eles[2].strip('{};')
    elif eles[0] == "enum":
        return eles[1].strip('{};')
    elif eles[0] == "typedef" and eles[-1] == ';' :
        return eles[-2].strip('{};')
    else :
        return eles[-1][:-1].strip('{};')


def extractEnumEle(line) :
    keyword = '///<'
    des = line[line.find(keyword) + len(keyword): ]
    strs = line.split()
    key = strs[0];

    if strs[1].strip() == "=" :
        value = strs[2].strip(',')
    else :
        value = strs[1][1:].strip(',')
    
    return key, value, des
    
def writeEnumToFile(brief, name, ele, f) :
    f.write('\n\n### ' + name + '\n')
    f.write('*枚举描述*\n\n')
    f.write(brief + '\n\n')
    f.write("|枚举名      |    枚举值 | 描述  |\n| :-------- | --------:| :--: |\n")
   
    cnt = (int)(len(ele) / 3)
    for i in range(0, cnt):
        f.write("|" + ele[3 *i] + "|" + ele[3 * i + 1] + "|" + ele[3 * i + 2] + "|\n")
  




def ansisEnumBlock(strs, blocks):
    name = extractName(strs)
    print("name = ", name);
    # num = len(block)
    # enumName = extractName(block[num-1])
    # enumEle = []
    # print(enumName)
    # briefIdx = []
    # for idx in range(0, num):
    #     line = block[idx]
    #     if "\\brief" in line:
    #         print(idx)
    #         briefIdx.append(idx)
    #     elif line.strip().startswith('///') :
    #         briefIdx.append(idx);
    #     elif '///<' in line and not line.startswith('//'):
    #         key,value,des = extractEnumEle(line)
    #         enumEle.append(key)
    #         enumEle.append(value)
    #         enumEle.append(des)
    #         print(key,value, des)
    
    # print(briefIdx)

    # start = briefIdx[0]
    # briefs=[]
    # for idx in briefIdx:
    #     if idx == start:
    #         briefs.append(block[idx])
    #     else:
    #         break
    #     start +=1

    # brief = extractBrief(briefs)

    # if len(enumEle) > 0 :
    #     writeEnumToFile(brief, enumName, enumEle, fout)