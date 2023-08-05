class Table(object):
	table_name: str
	columns: list
	script: str

	def __init__(self, table_name, columns, script):
		self.table_name = table_name
		self.columns = columns
		self.script = script


class Column(object):
	column_name: str
	data_type: str
	nullable: bool
	character_maximum_length: int
	column_type: str
	column_comment: str

	def __init__(self, column_name, data_type, nullable, character_maximum_length, column_type, column_comment):
		self.column_name = column_name
		self.data_type = data_type
		self.nullable = nullable
		self.character_maximum_length = character_maximum_length
		self.column_type = column_type
		self.column_comment = column_comment
		pass
