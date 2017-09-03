import glob
import os
import subprocess
import json


decryption_flag = True
convertion_flag = False
decrypted_folder = "decrypted"
converted_folder = "converted"


if not os.path.isdir(decrypted_folder):
	os.mkdir(decrypted_folder)
if not os.path.isdir(converted_folder):
	os.mkdir(converted_folder)

# ocr
for file in glob.glob('originals/*.pdf'):
	print("INFO: Processing input file {}".format(file))
	converted_file = os.path.join(converted_folder, file + '.txt')
	print(converted_file)
	# decrypt
	if decryption_flag:
		decrypted_file = os.path.join(decrypted_folder, file + '.pdf')
		print("INFO: decrypted file is {}".format(decrypted_file))
		os.system("qpdf --password='' --decrypt '{}' '{}'".format(file, decrypted_file))
		inputfile = decrypted_file
	else:
		inputfile = file

	# use pdf2txt directly
	if convertion_flag:
		os.system("pdf2txt.py -o '{}' '{}'".format(converted_file, inputfile)) # bypass decryption	

	# get page numbers
	cmd = "pdfinfo '{}' | grep Pages| cut -d':' -f2".format(file)
	npages =subprocess.check_output(cmd, shell=True)
	npages = int(npages)
	print('{} has {} pages'.format(file, npages))

	# # pdf2png and ocr
	basename = os.path.basename(file)
	basename = os.path.splitext(basename)[0] # no extension
	outputtxt = basename + '.txt'
	print("INFO: Convert pdf[1] to png files")
	os.system("convert -density 300 -alpha off '{}'[1] -resize 80% '{}'-02.png".format(file, basename)) 
	os.system("tesseract '{}'-02.png stdout >> '{}'".format(basename, outputtxt))
	os.system("echo =======================ENDOFPAGE======================= >> '{}'".format(outputtxt))

	if (npages >= 11):
		# some files has fewer than 11 pages and does not have job details
		print("INFO: Convert pdf[10] to png files")
		os.system("convert -density 300 -alpha off '{}'[10] -resize 80% '{}'-11.png".format(file, basename)) 
		os.system("tesseract '{}'-11.png stdout >> '{}'".format(basename, outputtxt))
	os.system("echo =======================ENDOFPAGE======================= >> '{}'".format(outputtxt))


# extract info from txt and dump into json file
for txtfile in glob.glob("2.ocr_txt/*.txt"):
	info = {'soc_code': '', 
			'job_title': '',
			'job_duties': ''}
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
				if "SOC" in line:
					# print('line is {}'.format(line))	
					flag = 1
					continue
				elif "Job title" in line or "Joblitle" in line or "Jobtitle" in line:
					flag = 2
					continue
				elif "Addendum" in line:
					flag = 3
					continue
				else:
					pass
			if flag == 1 and not info['soc_code']:
				# SOC code
				soc_code = line.strip().split(' ')[1]
				print(soc_code)
				soc_code = soc_code.replace('\\u2014', '-')
				print(soc_code)
				soc_code = soc_code.replace('oo', '00')		
				print(soc_code)
				info['soc_code'] = soc_code
				# print('soc_code is {}'.format(info['soc_code']))
				flag = 0 # reset flag
			elif flag == 2 and not info['job_title']:
				# Job title
				info['job_title'] = line.strip()
				# print('job title is {}'.format(info['job_title']))
				flag = 0
			elif flag == 3:
				# job duties
				if "ETA Form" in line:
					flag = 0
					continue
				job_duties += line

		# clean up and contatenate job duties to string
		job_duties = job_duties.split('\n')[1:]
		job_duties = [line for line in job_duties if line.strip()]
		job_duties = ' '.join(job_duties)
		job_duties = job_duties.replace('\\u2014', '-')
		job_duties = job_duties.replace('00', 'oo')
		job_duties = job_duties.replace('\\u2018', "'")
		job_duties = job_duties.replace('\\u2019', "'")
		job_duties = job_duties.replace('\\u201c', "'")
		job_duties = job_duties.replace('\\u201d', "'")
		info['job_duties'] = job_duties
		# print('job duties is {}'.format(info['job_duties'] ))
		
		# dump job info to json file
		# print(info)
		with open('json3/{}'.format(os.path.basename(txtfile)), 'w') as outfile:
			json.dump(info, outfile, sort_keys=True,
		                  indent=4, separators=(',', ': '))













	