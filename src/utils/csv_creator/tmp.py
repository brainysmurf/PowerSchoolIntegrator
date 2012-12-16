import os 
path = os.path.realpath(__file__)

while not path == '/':
	path = os.path.split(path)[0]
	if not '__init__.py' in os.listdir(path):
		break
	print(os.listdir(path))

print()
print(path)
