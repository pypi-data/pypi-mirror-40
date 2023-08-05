import re

import pymysql

from db2pojo.model import Table, Column

def get_tables_from_mysql(host, port, db_name, user, password, charset):
	connection = pymysql.connect(host=host, port=port, user=user, password=password, charset=charset)

	try:
		tables = []

		for table_name in __get_table_names(connection, db_name):
			columns = __get_columns(connection, db_name, table_name)
			script = __get_create_table_script(connection, db_name, table_name)
			tables.append(Table(table_name, columns, script))

		return tables

	finally:
		connection.close()

def __get_table_names(conn, db_name):
	table_names = []

	with conn.cursor() as cur:
		sql = 'select `table_name` from information_schema.`tables` where table_schema = %s'
		cur.execute(sql, (db_name))

		results = cur.fetchall()

		for result in results:
			table_names.append(result[0])

	return table_names


def __get_columns(conn, db_name, table_name):
	columns = []

	with conn.cursor() as cur:
		sql = 'select `column_name`, data_type, is_nullable, character_maximum_length, column_type, column_comment from information_schema.`columns` where table_schema = %s and `table_name` = %s'

		cur.execute(sql, (db_name, table_name))

		results = cur.fetchall()

		for result in results:
			column = Column(result[0], result[1], True if result[2] == 'YES' else False, result[3], result[4], result[5])
			columns.append(column)

	return columns

def __get_create_table_script(conn, db_name, table_name):
	with conn.cursor() as cur:
		sql = 'show create table %s.%s' % (db_name, table_name)

		cur.execute(sql)
		result = cur.fetchone()

	return __filter_auto_increment_value(result[1])

def __filter_auto_increment_value(script):
	(front_script, last_line) = script.rsplit('\n', 1)
	last_line = re.sub("\sAUTO_INCREMENT=\d+", '', last_line, count=1)

	return front_script + '\n' + last_line

