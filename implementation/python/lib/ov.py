
def _count_backslash(data):
	count = 0
	for i in data[::-1]:
		if i == "\\":
			count += 1
		else:
			break
	return count

def _parse(tokens):

	result = [ [] ]

	for token in tokens:
		if token[0] in ("array","object") and token[1] in ("[","{"):
			result.append([])
		elif token == ("array","]"):
			arr = result.pop()
			result[-1].append(arr)
		elif token == ("object","}"):
			arr = result.pop()
			if len(arr) % 2 != 0:
				return None,{"error":"invalid object definition, key-value count doesn't match"}

			obj = {}
			last_name = None
			for item in arr:
				if last_name:
					obj[last_name] = item
					last_name = None
				else:
					if type(item) != str:
						return None,{"error":"invalid key in object. only strings are accepted as key"}
					last_name = item
			result[-1].append(obj)
		else:
			if token[0] == "number":
				# todo: process number
				value = None
				if '.' in token[1]:
					value = float(token[1])
				elif '0x' in token[1]:
					value = int(token[1],16)
				elif '0b' in token[1]:
					if len(token[1].replace("0","").replace("1","").replace("b","")) > 0:
						return None,{"error":"illegal values in binary number"}
					value = int(token[1],2)
				elif token[1][0] == '0':
					if "8" in token[1] or "9" in token[1]:
						return None,{"error":"illegal values in octal number"}
					value = int(token[1],8)
				else:
					value = int(token[1])

				result[-1].append(value)
			else:
				result[-1].append(token[1])

	if type(result[0][0]) not in (list,dict):
		return None,{"error":"your root data must be array or object"}

	return result[0][0]

def load(data):

	# just hacky way to ensure processed all given data
	data += ' '

	# valid types and yes, type_array and type_object unused
	type_name    = 1
	type_number  = 2
	type_string  = 3
	# type_array    = 4
	# type_object  = 5
	# yeah, we treating comments is type too while finding tokens
	type_comment = 6

	# current type
	current = 0
	# current value
	value   = ""

	# results before parsing ?
	tokens = []

	# iterate every character from data
	for char in data:
		if current != 0:
			if current == type_name:
				if char == "_" or char.isalnum():
					value += char
				else:
					tokens.append(("name",value))
					current, value = 0, ""

			elif current == type_number:
				if char.isdigit() or char == "." or char in "abcdefx":
					if char == "." and "." in value:
						return {"error":"numbers cant contain more than one dot"}
					elif char in ("-","+"):
						return {"error":"multiple/invalid minus/plus written in number"}
					elif char in ("abcdef"):
						if char == "b" and len(value) == 1:
							pass
						elif len(value) > 1 and value[1] == 'x':
							pass
						else:
							return {"error":"unknown {} in number definition".format(char)}

					value += char
				else:
					tokens.append(("number",value))
					current, value = 0, ""

			elif current == type_string:
				if char == "\"":
					if len(value) > 1:
						count_slash = _count_backslash(value)
						escaped = False
						if count_slash > 0:
							value = value[:-count_slash]
							if count_slash % 2 != 0:
								escaped = True
								count_slash -= 1
							value += "\\" * int(count_slash/2)

						if not escaped:
							tokens.append(("string",value[1:]))
							current, value = 0, ""
						else:
							value += char
					else:
						tokens.append(("string",""))
						current, value = 0, ""
				else:
					value += char

			elif current == type_comment:
				if len(value) == 1 and char != "*":
					return {"error":"unknown character found while passing comment. comments must be starts with /* and ends with */"}
				elif char == "/" and len(value) > 3 and value[-1] == "*":
					current, value = 0, ""
				else:
					value += char
		else:
			if char == "_" or char.isalpha():
				current, value = type_name, char
			elif char in ("-","+") or char.isnumeric():
				current, value = type_number, char
			elif char == "\"":
				current, value = type_string, char
			elif char in ("[","]"):
				tokens.append(('array',char))
			elif char in ('{','}'):
				tokens.append(('object',char))
			elif char == "/":
				current, value = type_comment, char

	return _parse(tokens)

def save(data):
	current, temporary = [ data ], []
	finished = False
	while not finished:
		finished = True
		for item in current:
			if type(item) in (float,int):
				temporary.append(str(item))
			elif type(item) in (str,tuple):
				temporary.append(item)
			elif type(item) == list:
				temporary.append(("[",))
				temporary.extend(item)
				temporary.append(("]",))
				finished = False
			elif type(item) == dict:
				temporary.append(("{",))
				items = []
				for k,v in item.items():
					items.append(k)
					items.append(v)
				temporary.extend(items)
				temporary.append(("}",))
				finished = False
			else:
				return None,r"{ error \"invalid data type passed to ov's save method\" }"
		current, temporary = temporary, []

	result = ""
	for item in current:
		if type(item) == tuple:
			result += item[0] + " "
		else:
			if item.replace("_","").isalnum():
				result += item + " "
			elif item.replace("+","").replace("-","").replace(".","").isalnum():
				result += item + " "
			else:
				if "\"" in item:
					slices, value = item.split("\""),""
					for slice in slices:
						# escape backslashes before quote if any
						slashes = _count_backslash(slice)
						if slashes > 0:
							slice = slice[:-slashes]
							slice += "\\"*(slashes*2)
						# add escape after every " symbol
						slice += "\\\""
						value += slice
					# remove trailing "
					value = value[:-2]
					result += "\""+ value + "\" "
				else:
					result += "\""+ item + "\" "

	return result[:-1]
