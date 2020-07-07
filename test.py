import enum
import struct




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

        if enum.isEnum(block) :
            enum.ansisEnumBlock(block,fout)
        elif struct.isStruct(block) :
            struct.ansisStructBlock(block, fout)
        block.clear()



    line = f.readline() 
 
f.close()
fout.close()

