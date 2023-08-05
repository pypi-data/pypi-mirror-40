
def underscore_to_camelcase(underscore_str):
	first, *others = underscore_str.lower().split('_')
	return ''.join([first.lower(), *map(str.title, others)])

def underscore_to_pascalcase(underscore_str):
	first, *others = underscore_str.lower().split('_')
	return ''.join([str.title(first), *map(str.title, others)])
