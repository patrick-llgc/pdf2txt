import glob
import shutil
import os
import json

"""
Combine information from attachment and H11 field for files that 
does not have job dueties in attachment
"""


inputdir = r'/Users/megatron/Downloads/9089 Forms/3.json_output/no_job_duties'
origdir = r'/Users/megatron/Downloads/9089 Forms/0.original_pdf'
outputdir = r'/Users/megatron/Downloads/9089 Forms/H11/json'

for file in glob.glob(os.path.join(inputdir, '*.txt')):
	basename = os.path.basename(file)
	basename = os.path.splitext(basename)[0]
	print('basename is {}'.format(basename))

	input1 = os.path.join(outputdir, basename + '.txt.json.txt')
	input2 = os.path.join(inputdir, basename + '.txt')
	with open(input1) as f:
		print("INFO: Processing text file {}".format(input1))
		info = json.load(f)
	with open(input2) as g:
		print("INFO: Processing text file {}".format(input2))
		info2 = json.load(g)
	# print(info)
	# print(info2)
	if (sum(1 for string in info.values() if len(string)>0) == 1 and 
		sum(1 for string in info2.values() if len(string)>0) == 2):
		info2['job_duties'] = info['job_duties']

		outputfile = os.path.join(outputdir, basename + '.txt')
		with open(outputfile, 'w') as outfile:
			json.dump(info2, outfile, sort_keys=True,
		                  indent=4, separators=(',', ': '))
	