#Japer Dan Colin maybe Akis n Kunde
def LoadFromFile(filepath):
	state = []
	f = open(filepath, "r")
	for i in f:
		state.append(i.strip().split("\t"))
	dimensions = state.pop(0)[0]
	print("{} is a {}x{} grid".format(str(filepath),dimensions,dimensions))

	return [dimensions,state]

def DebugPrint(fileToPrint):

	for row in fileToPrint[1]:
		print("{ ", end = '')
		for number in row:
			print(" {}\t".format(number), end = '')
		print("}")

hahahahaahahahaha = LoadFromFile("Test.txt")
DebugPrint(hahahahaahahahaha)
