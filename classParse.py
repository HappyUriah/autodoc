import funcParse as func
import enumParse as enum
import structParse as struct
import otherParse as other

def isComment(line):
    return line.strip().startswith('//')

def isStatement(line) :
    if line.find('//') != -1 :
        return line[0:line.find('//')].strip().endswith(";")
    else :
        return line.strip().endswith(';')

def isClass(strs):

    if strs.strip().startswith("class ") and strs.count('{') > 0 :
        return True
    else :
        return False

def ansisBlock(strs, blocks,fout):
    if func.isFunction(strs):
        func.ansisFunctionBlock(strs, blocks, fout)
    elif enum.isEnum(strs):
        enum.ansisEnumBlock(strs, blocks,fout)
    elif struct.isStruct(strs):
        struct.ansisStructBlock(strs, blocks, fout)
    elif isClass(strs):
        ansisClassBlock(strs, blocks,fout)
    else :
        other.ansisOtherBlock(strs, blocks)


def ansisClassBlock(strs, blocks, fout):
    print("is class")
    num = len(blocks)

    start = 0
    for i in range(0, num):
        line = blocks[i].strip()
        if line and not isComment(line):
            start = i;
            break
    

    print("blocks[start] = ", blocks[start])

    assert blocks[start].find('{') != -1 and  blocks[start].find('}') == -1
    newblocks=[]
    newstrs=""
    for i in range(1 + start, num):
        line = blocks[i]
        if isComment(line):
            newblocks.append(line)
        elif isStatement(line):
            newblocks.append(line)
            newstrs = newstrs + line[:line.find('//')]
            if newstrs.count("{") == newstrs.count("}") :
                print(newstrs)
                print("###")
                print(newblocks)
                ansisBlock(newstrs, newblocks, fout)

                newstrs=""
                newblocks.clear()
                print('\n###################\n\n\n\n')
        else :
            newblocks.append(line)
            newstrs = newstrs + line[:line.find('//')]
            if newstrs.count("{") == newstrs.count("}") and newstrs.count('{') > 0 :
                print(newstrs)
                print("###")
                print(newblocks)
                ansisBlock(newstrs, newblocks,fout)

                newstrs=""
                newblocks.clear()
                print('\n###################\n\n\n\n')

