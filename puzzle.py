#Japer Dan Colin maybe Akis n Kunde
def LoadFromFile(filepath):
	state = []
	f = open(filepath, "r")
	for i in f:
		state.append(i.strip().split("\t"))
	dimensions = state.pop(0)[0]
	print(state)
	print(dimensions)


LoadFromFile("Untitled.txt")
