import rotate, nbtreader
import json, sys


if __name__ == "__main__":
	args = sys.argv
	path = args[1]
	offsets = [0, 0, 0]
	if len(args) >= 5:
		offsets = [int(args[2]), int(args[3]), int(args[4])]
	print(json.dumps(rotate.rotate_predicate(nbtreader.to_predicate(nbtreader.read_data_from_nbt_file(path), offsets)), indent=4))
