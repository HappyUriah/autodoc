def extractBrief(line) :
    return line[line.find('\\brief') + len('\\brief'):].strip()

def extractName(line) :
    return line[line.find('}') + 1 : line.find(';')].strip()

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
    f.write('### ' + name + '\n')
    f.write('*枚举描述' + '*\n\n')
    f.write(brief + '\n')
    f.write(" | 枚举名      |    枚举值 | 描述  |\n| :-------- | --------:| :--: |\n")
   
    cnt = (int)(len(ele) / 3)
    for i in range(0, cnt):
        f.write("|" + ele[3 *i] + "|" + ele[3 * i + 1] + "|" + ele[3 * i + 2] + "|\n")
  


def isEnum(block):
    for line in block :
        if ' enum ' in line:
            return True
    return False

def ansisEnumBlock(block, fout):

    num = len(block)
    enumName = extractName(block[num-1])
    enumEle = []
    print(enumName)
    for line in block:
        if "\\brief" in line:
            brief = extractBrief(line)
            print(brief)
        elif '///<' in line and not line.startswith('//'):
            key,value,des = extractEnumEle(line)
            enumEle.append(key)
            enumEle.append(value)
            enumEle.append(des)
            print(key,value, des)

    if len(enumEle) > 0 :
        writeEnumToFile(brief, enumName, enumEle, fout)

def isStruct(block):
    for line in block :
        if ' struct ' in line:
            return True
    return False

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
    for line in block:
        if "\\brief" in line:
            brief = extractBrief(line)
            print(brief)
        elif '///<' in line and not line.startswith('//'):
            typ, val, des = extractStructEle(line)
            structEle.append(typ)
            structEle.append(val)
            structEle.append(des)
           # print(key,des)
    
    print("++++++++++++++++" , len(structEle))

    if len(structEle) > 0 :
        writeStructToFile(brief, Name, structEle, fout)



fout = open('output.md','w')



f = open("/home/gh/Documents/workspace/arcternsdk/src/base/arcternsdk_base.h")               # 返回一个文件对象 
line = f.readline()               # 调用文件的 readline()方法 
block = []
remain = True
while line:
    #print(len(line))
    line = line.strip()
    if line : 
        remain = True;
        block.append(line)
    else :
        remain = False;
    
    
    if remain == False and len(block) > 0  :
        #print(block)
        #print('\n\n\n')

        if isEnum(block) :
            ansisEnumBlock(block,fout)
        elif isStruct(block) :
            ansisStructBlock(block, fout)
        block.clear()



    line = f.readline() 
 
f.close()
fout.close()

