import funcParse as func
import enumParse as enum
import structParse as struct
import otherParse as other
import common as comm



def isClass(strs):

    if strs.strip().startswith("class ") and strs.count('{') > 0 :
        return True
    else :
        return False



def ansisBlock(strs, blocks,fout, clsname):
    if func.isFunction(strs):
        func.ansisFunctionBlock(strs, blocks, fout, clsname)
    elif enum.isEnum(strs):
        enum.ansisEnumBlock(strs, blocks,fout, clsname)
    elif struct.isStruct(strs):
        struct.ansisStructBlock(strs, blocks, fout, clsname)
    elif isClass(strs):
        ansisClassBlock(strs, blocks,fout)
    else :
        other.ansisOtherBlock(strs, blocks, fout, clsname)

def extractClassName(line):
    return line.split()[1]

keyword=("\\brief", "\\param", "\\return", "\\tparam")
def isContainKeyword(line) :
    for word in keyword:
        if word in line:
            return True
    
    return False

def extractClassBrief(blocks, nonCommentline):
    word="\\brief "
    brief = ""
    start = -1
    #num = len(block)
    for id in range(0, nonCommentline):
        line = blocks[id].strip()
        if word in line :
            start = id + 1
            brief += line[line.find(word) + len(word):]
        elif id == start and  not isContainKeyword(blocks[id]) and line.startswith("//") :
            start +=1
            brief += line.strip('/')

    #print("brief = " , brief)
    return brief

def writeClassToFile(clsname, brief, fout):
    fout.write('## ' + clsname + '\n\n')
    fout.write('*类描述*\n\n')

    comm.assertStr(brief, clsname  + "类  无描述信息")
    fout.write(brief + "\n")

    fout.write('\n\n')


def ansisClassBlock(strs, blocks, fout):
    print("is class")
    num = len(blocks)

    start = 0
    for i in range(0, num):
        line = blocks[i].strip()
        if line and not comm.isComment(line):
            start = i;
            break
    

    print("blocks[start] = ", blocks[start])

    desc = blocks[start].strip() + " 行应该跟{，请注意代码格式"

    comm.assertStr(blocks[start].find('{') != -1 and  blocks[start].find('}') == -1, desc)
  

    classname = extractClassName(blocks[start])
    brief = extractClassBrief(blocks, start)

    writeClassToFile(classname, brief, fout)

    newblocks=[]
    newstrs=""
    for i in range(1 + start, num):
        line = blocks[i]
        if comm.isComment(line):
            newblocks.append(line)
        elif comm.isStatement(line):
            newblocks.append(line)
            newstrs = newstrs + comm.rmComment(line)
            if newstrs.count("{") == newstrs.count("}") :
                print(newstrs)
                print("###")
                print(newblocks)
                ansisBlock(newstrs, newblocks, fout, classname)

                newstrs=""
                newblocks.clear()
                print('\n###################\n\n\n\n')
        else :
            newblocks.append(line)
            newstrs = newstrs + comm.rmComment(line)
            if newstrs.count("{") == newstrs.count("}") and newstrs.count('{') > 0 :
                print(newstrs)
                print("###")
                print(newblocks)
                ansisBlock(newstrs, newblocks,fout, classname)

                newstrs=""
                newblocks.clear()
                print('\n###################\n\n\n\n')
        
        if newstrs.count('{') < newstrs.count("}") :
            newstrs = ""
            newblocks.clear()
            print('\n###################\n\n\n\n')

            

