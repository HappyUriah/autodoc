import sys

f = open(sys.argv[1])               # 返回一个文件对象 
lines = f.read()




while True :

    start = lines.find("/*")
    end = lines.find('*/')
    
    if start != -1 and end != -1 and end > start :
        newlines  =   lines[0:start] + lines[end + 2 :]
        lines = newlines
        newlines = " "
    else :
        break

print(lines)
#print(newlines)
print(type(lines))
f.close()