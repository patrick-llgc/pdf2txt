import glob
import json
import shutil

for file in glob.glob('*.txt'):
	with open(file) as f:
		info = json.load(f)
		nfields = sum(1 for string in info.values() if len(string)>0)
		if nfields < 3:
			# incomplete title, go above and correct for it
			print(file)
			with open('../' + file) as g:
				flag = 0
				page_ctr = 0
				for line in g:
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
						else:
							pass
					elif flag == 1 and info['soc_code']:
						# SOC code
						info['soc_code'] = line.strip().split(' ')[1]
						info['soc_code'] = info['soc_code'].replace('\\u2014', '-')
						info['soc_code'] = info['soc_code'].replace('oo', '00')
						# print('soc_code is {}'.format(info['soc_code']))
						flag = 0 # reset flag
					elif flag == 2 and info['job_title'] :
						# Job title
						info['job_title'] = line.strip()
						# print('job title is {}'.format(info['job_title']))
						flag = 0
					else:
						pass
			# print(info)
			with open(file + '.json', 'w') as outfile:
				json.dump(info, outfile, sort_keys=True,
			                  indent=4, separators=(',', ': '))
			shutil.move(file + '.json', file)