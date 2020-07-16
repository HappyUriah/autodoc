#!/usr/bin/python
# -*- coding: UTF-8 -*-

def isEnum(strs):
    eles = strs.split()
    print(eles)

    if len(eles) < 3:
        return False
    
    if eles[0] == "enum":
        return True
    if eles[0] == "typedef" and eles[1] == "enum" :
        return True
    return False

def rmComment(line):
    if line.find("//") != -1 :
        return line[:line.find("//")]
    else :
        return line

#提取描述信息
def extractBrief(blocks) :
    word="\\brief "
    brief = ""
    start = -1
    num = len(blocks)
    for id in range(0, num):
        line = blocks[id].strip()
        if word in line :
            start = id + 1
            brief += line[line.find(word) + len(word):]
        elif id == start and   line.startswith("//") :
            start +=1
            brief += line.strip('/')

    #print("brief = " , brief)
    return brief

#解析枚举名称
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

# 校验合法性，主要判断是否存在多行项
def valid(blocks) :
    for line in blocks:
        line = line.strip()
        if line.startswith("//"):
            continue
        else :
            line = rmComment(line).strip()
            if line.count(",") + line.count("{") + line.count("}") > 1:
                print("wrong format!!!!,请注意换行")
                return False
            elif line.count(",") == 1 and not line.endswith(","):
                print("wrong format!!!!,请注意换行")
                return False
          
    
    return True




def extractEnumEle(blocks) :

    start = -1
    end = -1
    num = len(blocks)
    for i in range(0,num):
        line = blocks[i].strip()
        if line.startswith("//"):
            continue
        else :
            #print(line)
            line = rmComment(line)
            #print(line)
            if "{" in line:
                start = i
                #print("start = ", start)
            elif "}" in line:
                end = i
    #print("start = ", start)
    #print("end = ", end)
    
    assert start != -1
    assert end != -1
    assert start < end

    keyword = '///<'
    items = []
    for i in range(start + 1, end):
        line = blocks[i].strip()
        if not line or line.startswith("//"):
           continue

        assert line.find(keyword) != -1
        des = line[line.find(keyword) + len(keyword): ]
        assert des
        line = rmComment(line)
        strs = line.split()

        #print(strs)
        assert   len(strs) > 2
        
        key = strs[0];
        value = strs[2].strip(',')
        kvd=(key,value, des)
        items.append(kvd)

    return items


    
def writeEnumToFile(brief, name, ele, f) :
    f.write('\n\n### ' + name + '\n')
    f.write('*枚举描述*\n\n')
    f.write(brief + '\n\n')
    f.write("|枚举名      |    枚举值 | 描述  |\n| :-------- | --------:| :--: |\n")
   
    cnt = (int)(len(ele) / 3)
    for i in range(0, cnt):
        f.write("|" + ele[3 *i] + "|" + ele[3 * i + 1] + "|" + ele[3 * i + 2] + "|\n")
  




def ansisEnumBlock(strs, blocks):

    name = extractName(strs).strip()
    print("name = ", name);
    assert name

    brief = extractBrief(blocks)
    print("brief = ", brief)
    assert brief

    assert valid(blocks)

    items = extractEnumEle(blocks)
    print("enum items = ", items);
    