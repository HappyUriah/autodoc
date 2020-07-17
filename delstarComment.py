

def rmStarComment(input,output):

    f = open(input)               # 返回一个文件对象 
    lines = f.read()
    f.close()

    while True :

        start = lines.find("/*")
        end = lines.find('*/')
    
        if start != -1 and end != -1 and end > start :
            newlines  =   lines[0:start] + lines[end + 2 :]
            lines = newlines
            newlines = " "
        else :
            break
    
    fout = open(output, "w")
    fout.write(lines)
    fout.close()


    