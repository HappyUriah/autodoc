#!/usr/bin/python
# -*- coding: UTF-8 -*-


def extractBrief(blocks) :
    brief = ""
    hasBrief = 0

    for line in blocks:

        line = line.strip()
        if line.startswith('/// ') and line.find("\\brief") != -1:
            hasBrief = 1
            brief += line[line.find('\\brief') + len('\\brief'):].strip()

        elif line.startswith('///') and hasBrief == 1 :
            brief += line.strip('/\n ')
        
        elif hasBrief == 1 :
            break
        else :
            pass
       
    return brief

def extractName(strs) :
    eles = strs.split()
    if eles[0] == "struct":
        return eles[1].strip('{};')
    elif eles[0] == "typedef" and eles[-1] == ';' :
        return eles[-2].strip('{};')
    else :
        return eles[-1][:-1].strip('{};')


def findItemComment(item, blocks) :
    return True
    # item = item.strip()
    # eles = item.split(",")
    # for line in blocks:
    #     if line.find(item) != -1 :
        
    #         otherEles = line.split(",")
    #      #   print(item, line, otherEles)
    #         assert item == otherEles[0].strip()

    #         assert otherEles[0].find('///<') != -1 or otherEles[1].find('///<') != -1

    #         if otherEles[0].find('///<') != -1:
    #             return otherEles[0][otherEles[0].find('///<') + 4:].strip() 
    #         elif otherEles[1].find('///<') != -1 :
    #             return otherEles[1][otherEles[1].find('///<') + 4:].strip() 



# def extractEnumEle(strs, blocks) :

#     strs = strs[strs.find('{') + 1 : strs.find('}')]
#   #  print(strs)
#     items = strs.split(',')
#    # print(items)
#     for item in items:
#         print(item)
#         eles = item.split()
#         assert len(eles) == 3 or len(eles) == 0

#         if len(eles) == 3 :
#             comment = findItemComment(item, blocks)
#             print(comment)
    
    # keyword = '///<'
    # des = line[line.find(keyword) + len(keyword): ]
    # strs = line.split()
    # key = strs[0];

    # if strs[1].strip() == "=" :
    #     value = strs[2].strip(',')
    # else :
    #     value = strs[1][1:].strip(',')
    
    # return key, value, des
    
# def writeEnumToFile(brief, name, ele, f) :
#     f.write('\n\n### ' + name + '\n')
#     f.write('*枚举描述*\n\n')
#     f.write(brief + '\n\n')
#     f.write("|枚举名      |    枚举值 | 描述  |\n| :-------- | --------:| :--: |\n")
   
#     cnt = (int)(len(ele) / 3)
#     for i in range(0, cnt):
#         f.write("|" + ele[3 *i] + "|" + ele[3 * i + 1] + "|" + ele[3 * i + 2] + "|\n")
  




def ansisStructBlock(strs, blocks):
    name = extractName(strs).strip()
    print("name = ", name);
    assert name
    brief = extractBrief(blocks)
    print("brief = ", brief)
    assert brief
   # extractEnumEle(strs, blocks)
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