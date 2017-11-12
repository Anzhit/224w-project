import sys

inputPath = sys.argv[1]
edgesPath = sys.argv[2]
attribsPath = sys.argv[3]

inFile = open(inputPath, 'r')
lines = inFile.readlines()

mapping = dict()
num = 0
def f(x):
    global num
    if x in mapping.keys():
        return mapping[x]
    num+=1
    mapping[x]=str(num)
    return str(num)

outFile = open(edgesPath, 'w')
outFile2 = open(attribsPath, 'w')

it = 0.0
for line in lines:
    it += 1
    print it/len(lines)
    line = line[:-2]
    fields = line.split('\t')
    related = fields[9:]
    vidNum = f(fields[0])
    
    toPrint = vidNum + "\t"
    for field in fields[1:9]:
        toPrint += field
        toPrint += "\t"
    toPrint=toPrint[:-1]
    outFile2.write(toPrint+"\n")
    
    for relatedVid in fields[9:]:
        relatedNum = f(relatedVid)
        outFile.write(vidNum + "\t" + relatedNum + "\n")  

outFile.flush()
outFile2.flush()
outFile.close()
outFile2.close()
