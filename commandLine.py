# auto-multiple-choice prepare Nominative-sheets.tex --mode s --data /home/fanhenrique/MC-Projects/commandLine/data --debug file.log

#comando que funciona
# --with pdflatex --filter latex --filtered-source /home/fanhenrique/MC-Projects/teste2/DOC-filtered.tex --out-sujet /home/fanhenrique/MC-Projects/teste2/DOC-sujet.pdf --out-corrige /home/fanhenrique/MC-Projects/teste2/DOC-corrige.pdf --out-corrige-indiv /home/fanhenrique/MC-Projects/teste2/DOC-indiv-solution.pdf --out-catalog /home/fanhenrique/MC-Projects/teste2/DOC-catalog.pdf --out-calage /home/fanhenrique/MC-Projects/teste2/DOC-calage.xy --mode s[sc]k --n-copies 1 /home/fanhenrique/MC-Projects/teste2/Nominative-sheets.tex --prefix /home/fanhenrique/MC-Projects/teste2/ --latex-stdout --data /home/fanhenrique/MC-Projects/teste2/data

import os
import shutil

import argparse
import logging

DEFAULT_NCOPIES = 1
DEFAULT_STUDENTS = 'list.csv'
DEFAULT_FILE = '/Nominative-sheets.tex'

DEFAULT_LOG_LEVEL = logging.INFO
TIME_FORMAT = '%Y-%m-%d,%H:%M:%S'

def main():

	parser = argparse.ArgumentParser(description='Command Line AMC')

	parser.add_argument('--project', '-p', help='Diretorio do projeto', required=True, type=str)
	parser.add_argument('--file', '-f', help='Arquivo latex para criar as provas', default=DEFAULT_FILE, type=str)
	parser.add_argument('--students', '-s', help='lista dos alunos', default=DEFAULT_STUDENTS, type=str)
	parser.add_argument('--ncopies', '-n', help='Quantidade de provas', default=DEFAULT_NCOPIES, type=int)
	
	help_msg = "Logging level (INFO=%d DEBUG=%d)" % (logging.INFO, logging.DEBUG)
	parser.add_argument("--log", "-l", help=help_msg, default=DEFAULT_LOG_LEVEL, type=int)

	args = parser.parse_args()

	if args.log == logging.DEBUG:
		logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s', datefmt=TIME_FORMAT, level=args.log)
	else:
		logging.basicConfig(format='%(asctime)s.%(msecs)03d %(message)s', datefmt=TIME_FORMAT, level=args.log)


	path = '/home/vagrant/MC-Projects/' + args.project

	os.makedirs(path)
	os.makedirs(path+'/cr')
	os.makedirs(path+'/cr/corrections')
	os.makedirs(path+'/cr/corrections/jpg')
	os.makedirs(path+'/cr/corrections/pdf')
	os.makedirs(path+'/cr/zooms')
	os.makedirs(path+'/cr/diagnostic')
	os.makedirs(path+'/data')
	os.makedirs(path+'/scans')
	os.makedirs(path+'/exports')

	os.system('tar -xvzf /home/vagrant/amc-testbed/models/Nominative-sheets.tgz -C ' + path)

	if(args.file != DEFAULT_FILE):
		shutil.copy2(os.getcwd() + '/' + args.file, path)
	
	file = path + '/' + args.file
	
	print(file)

	os.system('auto-multiple-choice prepare '+
               '--with pdflatex '+
               '--filter latex '+
               '--filtered-source ' + path + '/DOC-filtered.tex '+
               '--out-sujet ' + path + '/DOC-sujet.pdf '+
               '--out-corrige ' + path + '/DOC-corrige.pdf '+
               '--out-corrige-indiv ' + path + '/DOC-indiv-solution.pdf '+
               '--out-catalog ' + path + '/DOC-catalog.pdf '+	
               '--out-calage ' + path + '/DOC-calage.xy '+
               '--mode s[sc]k '+
               '--n-copies '+ str(args.ncopies) +' '+
               file + ' '+
               '--prefix ' + path + ' '+
               '--latex-stdout '+
               '--data ' + path + '/data '+  
	           '--debug ' + path + '/file.log')


if __name__ == '__main__':
	main()