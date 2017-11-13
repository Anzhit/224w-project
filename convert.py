import sys
import hashlib
inputPath = sys.argv[1]
edgesPath = sys.argv[2]
attribsPath = sys.argv[3]

inFile = open(inputPath, 'r')
lines = inFile.readlines()

mapping = dict()
num = 0
s = set()
def f(x, first=False):
	global s
	y = str(abs(int(hashlib.sha256(x).hexdigest(),16)) % (10 ** 9))
	if first:
		s |= set([y])
	return y
    # global num
    # if x in mapping.keys():
    #     return mapping[x]
    # num+=1
    # mapping[x]=str(num)
    # return str(num)

outFile = open(edgesPath, 'w')
outFile2 = open(attribsPath, 'w')

outString = ""
outString2 = ""

it = 0.0
for line in lines:
    it += 1
    if it%100==0:
    	pass
    	# print it/len(lines)
    line = line[:-2]
    fields = line.split('\t')
    related = fields[9:]
    vidNum = f(fields[0], True)
    
    toPrint = vidNum
    for field in fields[:9]:
        toPrint += "\t"
        toPrint += field

    outString2+=toPrint+"\n"
    for relatedVid in fields[9:]:
        relatedNum = f(relatedVid)
        outString += vidNum + "\t" + relatedNum + "\n"
outFile.write(outString)
outFile.flush()
outFile2.write(outString2)
outFile2.flush()
outFile.close()
outFile2.close()
print len(s)==len(lines)