import abc

from db2pojo.util import underscore_to_pascalcase, underscore_to_camelcase


def convert_pojo(table):
	property_converter = PojoPropertyConverter.create()

	class_name = table.table_name

	if '_' in class_name:
		class_name = underscore_to_pascalcase(class_name)
	elif class_name == class_name.upper() and len(class_name) > 1:
		class_name = class_name[0] + class_name[1:].lower()

	props = []

	for col in table.columns:
		props.append(property_converter.convert(col))

	return PojoClassStructure(class_name, props)

	pass

class PojoClassStructure(object):
	def __init__(self, class_name, properties):
		self.class_name = class_name
		self.properties = properties
		self.package_name = None
		self.imports = {'import lombok.Data;'}
		self.annotations = ['@Data']
		self.line_separator = '\n'
		self.indent_char = '\t'

	def generate_code(self):
		code = ''

		if self.package_name:
			code += 'package {0};{1}{1}'.format(self.package_name, self.line_separator)

		for prop in self.properties:
			if '.' in prop.type:
				self.imports.add('import ' + prop.type + ';')
				(package, type) = prop.type.rsplit('.', 1)
				prop.type = type


		for im in self.imports:
			code += im + self.line_separator

		if self.imports:
			code += self.line_separator

		for an in self.annotations:
			code += an + self.line_separator

		code += "public class %s {%s" % (self.class_name, self.line_separator)

		for prop in self.properties:
			comment = ' //' + prop.comment if prop.comment else ''

			code += "%s%s %s %s;%s%s" % (self.indent_char, prop.access_modifier, prop.type, prop.name, comment, self.line_separator)

		code += "}%s" % (self.line_separator)

		return code


class PojoPropertyStructure(object):
	def __init__(self, type, name):
		self.access_modifier = 'private'
		self.type = type
		self.name = name
		self.comment = None

	def to_tuple(self):
		return (self.access_modifier, self.type, self.name)


class PojoPropertyConverter(metaclass=abc.ABCMeta):
	def __init__(self):
		self.__next_converter = None

	def set_next_converter(self, converter):
		self.__next_converter = converter

	def convert(self, column):
		name = self._convert_name(column)
		type = self._convert_type(column)

		prop = PojoPropertyStructure(type, name)

		comment = ''

		if column.data_type == 'enum':
			comment = column.column_type

		if column.column_comment:
			comment += ' ' if comment else ''
			comment += column.column_comment.replace('\r', ' ').replace('\n', ' ')

			prop.comment = comment

		return prop
		pass

	def _convert_name(self, column):
		name = column.column_name

		if ('_' in name):
			return underscore_to_camelcase(name)
		elif name == name.upper():
			return name.lower()
		else:
			return name[0].lower() + name[1:] if len(name) >= 2 else name.lower()


	def _convert_type(self, column):
		type = self._convert_type_internal(column)

		if type == None and (self.__next_converter is not None):
			type = self.__next_converter._convert_type(column)

		if type == None:
			raise Exception('not implemented converter for column (%s, %s)' % (column.column_name, column.data_type))

		return type

		pass

	@abc.abstractmethod
	def _convert_type_internal(self, column):
		pass

	@classmethod
	def create(cls):
		converters = [
			StringConverter(),
			ByteArrayConverter(),
			IntegerConverter(),
			DoubleConverter(),
			DateConverter()
		]

		prev_converter = None

		for converter in converters:
			if prev_converter is not None:
				prev_converter.set_next_converter(converter)

			prev_converter = converter

		return converters[0]

	pass


class StringConverter(PojoPropertyConverter):

	def _convert_type_internal(self, column):
		str_types = ('char', 'varchar', 'enum', 'tinytext', 'text', 'mediumtext', 'longtext', 'set')

		data_type = column.data_type.lower()

		if data_type in str_types:
			return 'String'

	pass

class ByteArrayConverter(PojoPropertyConverter):

	def _convert_type_internal(self, column):
		byte_array_types = ('tinyblob', 'blob', 'mediumblob', 'longblob', 'binary')

		data_type = column.data_type.lower()

		if data_type in byte_array_types:
			return 'byte[]'

	pass

class IntegerConverter(PojoPropertyConverter):

	def _convert_type_internal(self, column):
		int_types = ('tinyint', 'smallint', 'mediumint', 'int', 'year')

		data_type = column.data_type.lower()

		if data_type == 'bigint' or \
				(column.data_type == 'int' and 'unsigned' in column.column_type):

			return 'Long' if (column.nullable) else 'long'

		elif data_type in int_types:
			return 'Integer' if (column.nullable) else 'int'

	pass

class DoubleConverter(PojoPropertyConverter):

	def _convert_type_internal(self, column):
		double_types = ('decimal', 'float', 'double', 'bit')

		data_type = column.data_type.lower()

		if data_type in double_types:
			return 'Double' if (column.nullable) else 'double'

	pass

class DateConverter(PojoPropertyConverter):

	def __init__(self):
		super().__init__()
		self.date_and_time_types_to_date = False

	def _convert_type_internal(self, column):
		date_types = ('date', 'datetime', 'timestamp', 'time')

		data_type = column.data_type.lower()

		if self.date_and_time_types_to_date:
			if data_type in date_types:
				return 'java.util.Date'
		else:
			if data_type == 'datetime' or data_type == 'timestamp':
				return 'java.time.LocalDateTime'
			elif data_type == 'date':
				return 'java.time.LocalDate'
			elif data_type == 'time':
				return 'java.time.LocalTime'
	pass
