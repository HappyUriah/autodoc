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

def extractName(line) :
    return line[line.find('}') + 1 : line.find(';')].strip()



def extractArrayEle(note) :
    strs = note.split()

    idx = 0
    for str1 in strs:
        idx = idx + 1
        if('[' in str1) :
            val = str1[:str1.find('[')]
            break
    typ = note[0: note.find(val)]
    typ += '[]'
    return typ, val

def extractValEle(note) :
    strs = note.split()
    lastStr = strs[len(strs) - 1]
    if lastStr == ";" :
        val = strs[len(strs) - 2]
    else :
        val = lastStr[0:-1]
    typ = note[0: note.find(val)]
    return typ, val
    




def extractStructEle(line) :
    keyword = '///<'
    des = line[line.find(keyword) + len(keyword): ]

    note = line[0:line.find(keyword)]

    if '[' in note :
        # 数组
        typ, val = extractArrayEle(note)
        return typ, val , des

    else :
        typ, val = extractValEle(note)
        return typ, val, des

    

def writeStructToFile(brief, name, ele, f) :
    f.write('### ' + name + '\n')
    f.write('*结构体描述' + '*\n\n')
    f.write(brief + '\n')
    f.write(" | 类型      |    变量 | 描述  |\n| :-------- | --------:| :--: |\n")
   
    cnt = (int)(len(ele) / 3)
    for i in range(0, cnt):
        f.write("|" + ele[3 *i] + "|" + ele[3 * i + 1] + "|" + ele[3 * i + 2] + "|\n")
  
  



def ansisStructBlock(block, fout):

    num = len(block)
    Name = extractName(block[num-1])
    structEle = []
    print(Name)

    briefIdx = []
    for idx in range(0, num):
        line = block[idx]
        if "\\brief" in line:
            briefIdx.append(idx)
        
            #brief = extractBrief(line)
            #print(brief)
        elif '///<' in line and not line.startswith('///'):
            typ, val, des = extractStructEle(line)
            structEle.append(typ)
            structEle.append(val)
            structEle.append(des)
        elif line.strip().startswith('///') :
            briefIdx.append(idx);

    
    
    print("==================" , briefIdx)

    start = briefIdx[0]
    briefs=[]
    for idx in briefIdx:
        if idx == start:
            briefs.append(block[idx])
        else:
            break
        start +=1

    brief = extractBrief(briefs)
    
    #print("++++++++++++++++" , len(structEle))

    if len(structEle) > 0 :
        writeStructToFile(brief, Name, structEle, fout)