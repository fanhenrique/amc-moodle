import argparse
import logging

import mysql.connector


DEFAULT_LOG_LEVEL = logging.INFO
TIME_FORMAT = '%Y-%m-%d,%H:%M:%S'


def main():

	parser = argparse.ArgumentParser(description='Query students')

	parser.add_argument('--project', '-p', help='Diretório do projeto', required=True, type=str)
	parser.add_argument('--course', '-c', help='Curso', required=True, type=str)
	
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
	logging.info('Search for course students')


	cmd = '''
	SELECT mdl_user_enrolments.enrolid, 
	mdl_user_enrolments.userid, 
	mdl_enrol.courseid, 
	mdl_course.shortname, 
	mdl_user.username, 
	mdl_user.firstname, 
	mdl_user.lastname, 
	mdl_user.email 
	FROM 
	mdl_user_enrolments, 
	mdl_enrol, 
	mdl_course, 
	mdl_user 
	WHERE 
	mdl_enrol.id=mdl_user_enrolments.enrolid AND 
	mdl_user_enrolments.userid=mdl_user.id AND 
	mdl_enrol.courseid=mdl_course.id AND 
	mdl_course.shortname=\''''+args.course+'''\';
	'''
	cursor.execute(cmd)


	logging.info('mysql: ' + cmd)


	# Cria arquivo com a lista dos alunos
	with open(args.project + '/list.csv', 'w') as file:
		
		file.write('name,forename,id\n')
		
		for(enrolid, userid, courseid , courseName, userName, firstName, lastName, email) in cursor:
			# print(enrolid, userid, courseid, courseName, userName, firstName, lastName, email)
			file.write(firstName + ',' + lastName + ',' + str(userid) + '\n')

	logging.info('File created list.csv\n')
	

	



if __name__ == '__main__':
	main()