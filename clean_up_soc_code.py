import glob
import shutil

"""
Clean up special characters in the strings
"""
for file in glob.glob('*.txt'):
	with open(file) as f:
		lines = f.readlines()
	with open(file + '.txt', 'w') as g:
		for line in lines:
			line = line.replace('\\u2014', '-')
			line = line.replace('00', 'oo')
			line = line.replace('\\u2018', "'")
			line = line.replace('\\u2019', "'")
			line = line.replace('\\u201c', "'")
			line = line.replace('\\u201d', "'")
			if 'soc_code' in line:
				line = line.replace('oo', '00')
			g.write(line)
	shutil.move(file + '.txt', file)