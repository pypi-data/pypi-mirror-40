#!/usr/bin/env python

import argparse
import codecs
import os

from db2pojo import __version__
from db2pojo.mysql import get_tables_from_mysql
from db2pojo.pojo import convert_pojo

def main():
	parser = argparse.ArgumentParser(description='Generates pojo class file from an existing mysql database.\n If it runs without the required options, it run interactive mode.')

	parser.add_argument('--mysql-host', type=str, required=True, help='mysql host name')
	parser.add_argument('--mysql-port', default=3306, type=int, help='mysql port. default 3306')
	parser.add_argument('--mysql-user', type=str, required=True, help='mysql user name')
	parser.add_argument('--mysql-password', type=str, required=True, help='mysql password')
	parser.add_argument('--mysql-charset', default='utf8', type=str, help='mysql connection charset. default utf8')
	parser.add_argument('--db-name', type=str, required=True, help='db name to generate pojo class')
	parser.add_argument('--table-names', nargs='+', default=None, type=str, help='specific table names to generate pojo class. default all tables')

	parser.add_argument('--pojo', type=str, nargs=2, metavar=('OUTPUT_DIR', 'PACKAGE_NAME'), help='pojo generation options')
	parser.add_argument('--ddl', type=str, metavar='OUTPUT_DIR', help='ddl for create table generation option')
	parser.add_argument('--dry', action="store_true", help='it will not create files will only print to console.')

	parser.add_argument('-v', '--version', default=False, action='version', version='db2pojo version ({})'.format(__version__),  help='Print the current version')

	args = parser.parse_args()

	tables = get_tables_from_mysql(args.mysql_host, args.mysql_port, args.db_name, args.mysql_user, args.mysql_password, args.mysql_charset)

	specific_tables = set(args.table_names) if args.table_names else None

	if specific_tables:
		filtered_tables = [table for table in tables if table.table_name in specific_tables]
	else:
		filtered_tables = tables

	if args.pojo:
		generate_pojo(filtered_tables, args.pojo[0], args.pojo[1], args.dry)

	if args.ddl:
		generate_ddl(filtered_tables, args.ddl, args.dry)

	pass

def generate_pojo(tables, output_dir, package_name, dry_run):
	for table in tables:
		pojo = convert_pojo(table)
		pojo.package_name = package_name

		code = pojo.generate_code()

		if dry_run:
			title = "==== Generate ({} -> {}) ====".format(table.table_name, pojo.class_name + '.java')
			print(title)
			print (code)
			print('-' * len(title), "\n\n")
		else:
			file_path = os.path.join(output_dir, pojo.class_name + '.java')

			with codecs.open(file_path, "w", 'utf-8') as f:
				f.write(code)

			print ("{} -> {}".format(table.table_name, file_path))


def generate_ddl(tables, output_dir, dry_run):
	for table in tables:

		if dry_run:
			title = "==== Generate ({} Script) ====".format(table.table_name)
			print (title)
			print(table.script)
			print ('-' * len(title), "\n\n")
		else:

			file_path = os.path.join(output_dir, table.table_name + '.sql')

			with codecs.open(file_path, "w", 'utf-8') as f:
				f.write(table.script)

			print ("{} -> {}".format(table.table_name, file_path))


if __name__ == "__main__":
	main()
