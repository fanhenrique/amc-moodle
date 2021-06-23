import argparse
import logging

import mysql.connector


DEFAULT_LOG_LEVEL = logging.INFO
TIME_FORMAT = '%Y-%m-%d,%H:%M:%S'


def main():

	parser = argparse.ArgumentParser(description='Query quiz')

	parser.add_argument('--project', '-p', help='Diretório do projeto', required=True, type=str)
	parser.add_argument('--course', '-c', help='Curso', required=True, type=str)
	parser.add_argument('--quiz', '-q', help='Quesionário', required=True, type=str)
	
	help_msg = "Logging level (INFO=%d DEBUG=%d)" % (logging.INFO, logging.DEBUG)
	parser.add_argument("--log", "-l", help=help_msg, default=DEFAULT_LOG_LEVEL, type=int)

	args = parser.parse_args()

	if args.log == logging.DEBUG:
		logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s', datefmt=TIME_FORMAT, level=args.log)
	else:
		logging.basicConfig(format='%(asctime)s.%(msecs)03d %(message)s', datefmt=TIME_FORMAT, level=args.log)


	#Conexão banco de dados
	cnx = mysql.connector.connect(host='127.0.0.1', user='amcmoodle', database='moodle', password='amcmoodle')
	cursor = cnx.cursor()


	logging.info('Connected to the databese')
	logging.info('Search for course quiz')


	cmd = '''
	SELECT mdl_quiz.name, mdl_course.shortname
	FROM 
	mdl_course,
	mdl_quiz
	WHERE
	mdl_quiz.course=mdl_course.id AND
	mdl_quiz.name=\''''+args.quiz+'''\' AND
	mdl_course.shortname=\''''+args.course+'''\';
	'''


	# cursor.execute("select id, name, questiontext from mdl_question;")
	cursor.execute()

	for (id, name, questiontext) in cursor:
		questiontext = questiontext.split('>', 1)
		questiontext = questiontext[1].split('<', 1)
		questiontext = questiontext[0]
		# print('{} | {} | {} | {}'.format(id, name, questiontext))


	file = open("questionario_teste.txt", "w")

	file.write('# AMC-TXT source file\nTitle: My first AMC questionnaire\n\nPresentation: Please answer the following questions\nthe best you can.\n\n')

	file.write('* '+name+' - '+questiontext+'\n')

	cursor.execute('select answer, fraction from mdl_question_answers where question = '+ str(id) +';')

	for (answer, fraction) in cursor:
		answer = answer.split('>', 1)
		answer = answer[1].split('<', 1)
		answer = answer[0]
		# print('{}'.format(answer))
		if fraction == 0.0:
			file.write('- '+answer+'\n')
		else:
			file.write('+ '+answer+'\n')

	print(file.name+' arquivo criado')

	file.close()
	cursor.close()
	cursor.close()


	# cursor.execute('SELECT id, shortname FROM mdl_course WHERE shortname=\''+args.course+'\';')
	# for id, shortname in cursor:
	# 	id_course = id
	# print(id_course)


	# cursor.execute('SELECT id, course, name FROM mdl_quiz WHERE course=\''+str(id_course)+'\' AND name=\''+args.quiz+'\';')
	# for id, course, name in cursor:
	# 	id_quiz = id


if __name__ == '__main__':
	main()