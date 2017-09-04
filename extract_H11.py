import glob
import shutil
import os
import json

"""
Extract job duties information from H11 field, in addition to attachment
"""


inputdir = r'/Users/megatron/Downloads/9089 Forms/3.json_output/no_job_duties'
origdir = r'/Users/megatron/Downloads/9089 Forms/0.original_pdf'
outputdir = r'/Users/megatron/Downloads/9089 Forms/H11'

for file in glob.glob(os.path.join(inputdir, '*.txt')):
	basename = os.path.basename(file)
	basename = os.path.splitext(basename)[0]
	pdffile = basename + '.pdf'
	pdffile = os.path.join(origdir, pdffile)

	
	basename = os.path.join(outputdir, basename)
	outputtxt = basename + '.txt'
	pngfile = basename + '-03.png'

	print("INFO: Convert pdf[2] to png files")
	print("INFO: png file '{}'-03.png".format(basename))
	os.system("convert -density 300 -alpha off '{}'[2] -resize 80% '{}'".format(pdffile, pngfile)) 
	os.system("tesseract '{}' stdout >> '{}'".format(pngfile, outputtxt))
	os.system("echo =======================ENDOFPAGE======================= >> '{}'".format(outputtxt))


# extract info from txt and dump into json file
for txtfile in glob.glob("{}/*.txt".format(outputdir)):
	print(txtfile)
	info = {'job_duties': ''}
	print("INFO: Processing text file {}".format(txtfile))
	with open(txtfile) as f:
		flag = 0
		page_ctr = 0
		job_duties = ''
		for line in f:
			if len(line.strip()) == 0:
				# skip empty line
				continue
			if 'ENDOFPAGE' in line:
				page_ctr += 1
				if page_ctr < 2:
					continue
				else:
					break
			if flag == 0:
				# no need to extract info yet
				if "Job duties" in line and "submitting by mail" in line:
					flag = 3
					continue
				else:
					pass
			elif flag == 3:
				# job duties
				if "normal for the occupation" in line:
					flag = 0
					continue
				job_duties += line

		# clean up and contatenate job duties to string
		job_duties = job_duties.split('\n')#[1:]
		job_duties = [line for line in job_duties if line.strip()]
		job_duties = ' '.join(job_duties)
		# job_duties = job_duties.replace('\\u2014', '-')
		# job_duties = job_duties.replace('00', 'oo')
		# job_duties = job_duties.replace('\\u2018', "'")
		# job_duties = job_duties.replace('\\u2019', "'")
		# job_duties = job_duties.replace('\\u201c', "'")
		# job_duties = job_duties.replace('\\u201d', "'")
		info['job_duties'] = job_duties
		# print('job duties is {}'.format(info['job_duties'] ))
		
		# dump job info to json file
		# print(info)
		with open('{}'.format(txtfile + '.json.txt'), 'w') as outfile:
			json.dump(info, outfile, sort_keys=True,
		                  indent=4, separators=(',', ': '))













	