mList = ['wildan','anugrah','putra']

result = ""
for m in mList:
    if(result == ""):
        result += m
    else:
        result += "," + m
print(result)