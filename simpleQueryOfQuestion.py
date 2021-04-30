import mysql.connector

cnx = mysql.connector.connect(host='127.0.0.1', user='amcmoodle', database='moodle', password='amcmoodle')
cursor = cnx.cursor()

cursor.execute("select id, name, questiontext from mdl_question;")


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