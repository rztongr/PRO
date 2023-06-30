import random 


line=[]
with open('/home/renzt/task/sequence/10_mer_dataset.txt',"r") as f:  
    data = f.readlines()                                               
for m in range(len(data)):
    line.append(data[m].strip('\n'))
print(line[0],line[-1])
print(len(line))