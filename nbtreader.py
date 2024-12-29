import struct, gzip


tag_types = {1: 'b', 2: 'h', 3: 'i', 4: 'q', 5: 'f', 6: 'd'}
types_sizes = {'b': 1, 'h': 2, 'i': 4, 'l': 4, 'q': 8, 'f':4, 'd': 8}


class NBTReader:
	def __init__(self):
		self.file = None

	def read(self, file_path):
		with open(file_path, 'rb') as file:
			signature = file.read(2)
		op = open
		if signature == b'\x1f\x8b':
			op = gzip.open
		with op(file_path, 'rb') as file:
			self.file = file
			return self.read_tag()
		

	def read_tag(self):
		tag_type = self.read_type('b')
		if tag_type == 0:
			return None
		name = self.read_payload(8) #string
		value = self.read_payload(tag_type)
		#print(name, value)
		return {name: value}

	def read_payload(self, tag_type):
		if tag_type <= 6:
			return self.read_type(tag_types[tag_type])
		elif tag_type == 7: #byte array
			return list(self.file.read(self.read_type('i')))
		elif tag_type == 8: #string
			return self.file.read(self.read_type('h')).decode('utf-8')
		elif tag_type == 9: #list
			list_tag_type, lenght = self.read_type('b'), self.read_type('i')
			return [self.read_payload(list_tag_type) for _ in range(lenght)]
		elif tag_type == 10: #compound
			compound = {}
			while True:
				tag = self.read_tag()
				if tag is None:
					break
				compound.update(tag)
			return compound
		elif tag_type == 11: #int array
			return [self.read_type('i') for _ in range(self.read_type('i'))]
		elif tag_type == 12: #long array
			return [self.read_type('q') for _ in range(self.read_type('i'))]
		else:
			raise ValueError(f'Unknown tag type: {tag_type}')


	def read_type(self, tag):
		return struct.unpack(f'>{tag}', self.file.read(types_sizes[tag]))[0]


def properties_to_state(properties):
	result = {}
	for key in ('half', 'type', 'waterlogged', 'shape', 'facing', 'open'):
		if key in properties:
			result[key] = properties[key]
	return result


def to_predicate(data, offset=[0, 0, 0]):
	pallete = data['palette']
	blocks = data['blocks']
	result = {'condition': 'minecraft:all_of', 'terms': []}
	for block in blocks:
		condition = {'condition': "minecraft:location_check"}
		offsets = {"offsetX": block['pos'][0] - offset[0], "offsetY": block['pos'][1] - offset[1], "offsetZ": block['pos'][2] - offset[2]}
		for direction in offsets:
			if offsets[direction] != 0:
				condition[direction] = offsets[direction]
		props = pallete[block['state']]
		predicate = {'block': {'blocks': props['Name']}}
		if 'Properties' in props:
			state = properties_to_state(props['Properties'])
			if len(state) > 0:
				predicate['block']['state'] = state
		condition['predicate'] = predicate
		result['terms'].append(condition)
	return result


def read_data_from_nbt_file(path):
	reader = NBTReader()
	return reader.read(path)['']
