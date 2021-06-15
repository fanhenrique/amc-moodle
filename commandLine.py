# auto-multiple-choice prepare Nominative-sheets.tex --mode s --data /home/fanhenrique/MC-Projects/commandLine/data --debug latex.log

#comando que funciona
# --with pdflatex --filter latex --filtered-source /home/fanhenrique/MC-Projects/teste2/DOC-filtered.tex --out-sujet /home/fanhenrique/MC-Projects/teste2/DOC-sujet.pdf --out-corrige /home/fanhenrique/MC-Projects/teste2/DOC-corrige.pdf --out-corrige-indiv /home/fanhenrique/MC-Projects/teste2/DOC-indiv-solution.pdf --out-catalog /home/fanhenrique/MC-Projects/teste2/DOC-catalog.pdf --out-calage /home/fanhenrique/MC-Projects/teste2/DOC-calage.xy --mode s[sc]k --n-copies 1 /home/fanhenrique/MC-Projects/teste2/Nominative-sheets.tex --prefix /home/fanhenrique/MC-Projects/teste2/ --latex-stdout --data /home/fanhenrique/MC-Projects/teste2/data

import os
import shutil

import argparse
import logging

DEFAULT_NCOPIES = 1
DEFAULT_STUDENTS = 'list.csv'
DEFAULT_LATEX = '/Nominative-sheets.tex'

DEFAULT_LOG_LEVEL = logging.INFO
TIME_FORMAT = '%Y-%m-%d,%H:%M:%S'

def main():

	parser = argparse.ArgumentParser(description='Command Line AMC')

	parser.add_argument('--corrige', help='Corrige as provas', action='store_false')
	parser.add_argument('--project', '-p', help='Diretório do projeto', required=True, type=str)
	parser.add_argument('--answers', '-a', help='Arquivos pdf com as respostas para corrigir', type=str)
	parser.add_argument('--file', '-f', help='Arquivo latex para criar as provas', default=DEFAULT_LATEX, type=str)
	parser.add_argument('--course', '-c', help='Curso', type=str)
	parser.add_argument('--students', '-s', help='lista dos alunos', default=DEFAULT_STUDENTS, type=str)
	parser.add_argument('--ncopies', '-n', help='Quantidade de provas', default=DEFAULT_NCOPIES, type=int)
	
	help_msg = "Logging level (INFO=%d DEBUG=%d)" % (logging.INFO, logging.DEBUG)
	parser.add_argument("--log", "-l", help=help_msg, default=DEFAULT_LOG_LEVEL, type=int)

	args = parser.parse_args()

	if args.log == logging.DEBUG:
		logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s', datefmt=TIME_FORMAT, level=args.log)
	else:
		logging.basicConfig(format='%(asctime)s.%(msecs)03d %(message)s', datefmt=TIME_FORMAT, level=args.log)

	pathProject = '/home/vagrant/MC-Projects/' + args.project

	if(args.corrige):

		logging.info('Created project directory')

		os.makedirs(pathProject)
		os.makedirs(pathProject+'/cr')
		os.makedirs(pathProject+'/cr/corrections')
		os.makedirs(pathProject+'/cr/corrections/jpg')
		os.makedirs(pathProject+'/cr/corrections/pdf')
		os.makedirs(pathProject+'/cr/zooms')
		os.makedirs(pathProject+'/cr/diagnostic')
		os.makedirs(pathProject+'/data')
		os.makedirs(pathProject+'/scans')
		os.makedirs(pathProject+'/exports')
		
		# Descompacta modelos  
		os.system('tar -xvzf /home/vagrant/amc-testbed/models/Nominative-sheets.tgz -C ' + pathProject)
		logging.info('Unzipped model')

		# Busca alunos no banco de dados
		cmd = 'python3 queryStudents.py -c \'' + args.course + '\' -p' + pathProject
		logging.info('Command: ' + cmd)
		os.system(cmd)

		if(args.file != DEFAULT_LATEX):
			shutil.copy2(os.getcwd() + '/' + args.file, pathProject + '/' + DEFAULT_LATEX)
		latexFile = pathProject + '/' + DEFAULT_LATEX
		logging.info('Copied ' + args.file + 'to project')
		
		prepare = ('auto-multiple-choice prepare '+
	           '--with pdflatex '+
	           '--filter latex '+
	           '--filtered-source ' + pathProject + '/DOC-filtered.tex '+
	           '--out-sujet ' + pathProject + '/DOC-sujet.pdf '+
	           '--out-corrige ' + pathProject + '/DOC-corrige.pdf '+
	           '--out-corrige-indiv ' + pathProject + '/DOC-indiv-solution.pdf '+
	           '--out-catalog ' + pathProject + '/DOC-catalog.pdf '+	
	           '--out-calage ' + pathProject + '/DOC-calage.xy '+
	           '--mode s[sc]k '+
	           '--n-copies '+ str(args.ncopies) +' '+
	           latexFile + ' '+
	           '--prefix ' + pathProject + ' '+
	           '--latex-stdout '+
	           '--data ' + pathProject + '/data '+
	           '--debug ' + pathProject + '/file.log')

		os.system(prepare)

		meptex = ('auto-multiple-choice meptex '+
		  		'--src ' + pathProject + '/DOC-calage.xy '+ 
		  		'--progression-id MEP '+
		  		'--progression 1 '+
		  		'--data ' + pathProject + '/data '+  
		  		'--debug ' + pathProject + ' file.log')

		os.system(meptex)

	else:

		answersFile = pathProject + '/answers'

		with open(answersFile, 'w') as file:
			file.write(args.answers)

		readPdfForm = ('auto-multiple-choice read-pdfform '+
					'--progression-id analyse '+
					'--list ' + answersFile + ' '
					'--debug ' + pathProject + ' file.log '+
					'--no-multiple '+
					'--data ' + pathProject + '/data ')

		os.system(readPdfForm)


		getimages = ('auto-multiple-choice getimages '+
					'--progression-id analyse ' +
					'--list ' + answersFile + ' ' +
					'--debug ' + pathProject + ' file.log '+
					'--vector-density 250 ' +
					'--copy-to ' + pathProject + '/scans/ ' +
					'--orientation portrait')

		os.system(getimages)
		      

		analyse = ('auto-multiple-choice analyse '+
				'--debug ' + pathProject + ' file.log '+	
				'--no-multiple '+	
				'--tol-marque 0.2,0.2 '+
				'--prop 0.8 '+	
				'--bw-threshold 0.6 '+
				'--progression-id analyse '+
				'--progression 1 '+
				'--n-procs "0" '+
				'--data ' + pathProject + '/data '+
				'--projet ' + pathProject + ' '+
				'--cr ' + pathProject + '/cr '+
				'--liste-fichiers ' + answersFile + ' '
				'--no-ignore-red '+
				'--try-three')

		os.system(analyse)



		prepare2 = ('auto-multiple-choice prepare '+
				'--out-corrige-indiv ' + pathProject + '/DOC-indiv-solution.pdf '+
				'--n-copies '+ str(args.ncopies) +' '+
				'--with pdflatex '+
				'--filter latex '+
				'--filtered-source ' + pathProject + '/DOC-filtered.tex '+
				'--debug ' + pathProject + '/file.log '+
				'--progression-id bareme '+
				'--progression 1 '+
				'--data ' + pathProject + '/data '+  
				'--mode bk '+
				pathProject + args.file)

		os.system(prepare2)


		note = ('auto-multiple-choice note '+
			'--debug ' + pathProject + ' file.log '+
			'--data ' + pathProject + '/data '+
			'--seuil 0.15 '+
			'--seuil-up 1 '+
			'--grain 0.5 '+
			'--arrondi inf '+
			'--notemax 20 '+
			'--plafond '+
			'--notenull "0" '+
			'--notemin "" '+
			'--postcorrect-student "" '+
			'--postcorrect-copy "" '+
			'--no-postcorrect-set-multiple '+
			'--progression-id notation '+
			'--progression 1')

		os.system(note)
		           


if __name__ == '__main__':
	main()