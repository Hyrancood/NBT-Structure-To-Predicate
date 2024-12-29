# NBT to JSON Predicate Converter
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/Hyrancood/NBT-Structure-To-Predicate/blob/main/README.md)
[![ru](https://img.shields.io/badge/lang-ru-blue.svg)](https://github.com/Hyrancood/NBT-Structure-To-Predicate/blob/main/README-RU.md)

## Description
This project provides tools to read NBT (Named Binary Tag) files, convert them into Minecraft JSON predicates. The system supports working with uncompressed and compressed (GZip) NBT files.
*Project is tested on Minecraft 1.21.X nbt files, but as far as I know they haven't changed much since 1.13+*

## Functionality
- **Reading NBT files:** `NBTReader` class for parsing structured NBT data.
- **Convert to JSON predicate:** Function to convert NBT data to Minecraft compatible JSON format (predicate).
- **Predicate rotation:** A module to rotate predicate data by 90 degrees.

## Usage
The project is prepared to be used 'out of the box' for the case “I need to convert a structure to a predicate independent of building direction”.

### Reading NBT file and converting to JSON predicate
The `from_nbt_to_predicate.py` script converts the NBT file into a JSON predicate that checks if the structure is built correctly.
**Important!** The output predicates are sensitive to the following block states: `half`, `type`, `waterlogged`, `shape`, `facing`, `open`.

**Usage example:**
```bash
python from_nbt_to_predicate.py <path to NBT-file> <center X> <center Y> <center Z>
```
- `<path to NBT-file>` - path to NBT file.
- `<center X>`, `<center Y>`, `<center Z>` - optional `center of construction` (default is `[0, 0, 0]`). When the predicate is checked, the structure is checked from the center block.
This way the script will output the predicate to the console. If you want to write the predicate to a file, you can use '>', example:
```bash
python from_nbt_to_predicate.py example.nbt 0 1 0 > predicate.json
```

### JSON predicate rotation
You can also use the rotate module separately to make your predicate insensitive to building direction (*The direction of the blocks also rotates with the building!*).
The `rotate.py` script rotates predicates 90 degrees (3 times), creating a set of predicates for all possible orientations.

**Usage example:**
```bash
python rotate.py <input JSON file> <output JSON file> [-t]
```
- `<input JSON file>` is the path to the source JSON file (predicate).
- `<output JSON file>` - path to save the result.
- `-t` - (optional) is used for predicates of the form: `{"condition": "minecraft:all_of/any_of", "terms": [...]}`. If your predicate is a simple list of predicates, then the `-t` flag should not be set.

### Code example
You can also use these modules in python if the 'standard' method of use doesn't suit you:
#### Convert NBT to JSON
```python
import nbtreader, json

data = nbtreader.read_data_from_nbt_file("example.nbt")
json_predicate = nbtreader.to_predicate(data, offset=[0, 0, 0]) # This would create a one-direction-sensitive predicate
print(json.dumps(json_predicate, indent=4))
```

#### Predicate rotation
```python
import rotate

with open("predicate.json") as file:
    predicate = json.load(file)

rotated_predicate = rotate.rotate_predicate(predicate) # rotate the predicate once by 90 degrees and return a new one
print(rotated_predicate)
```

## Project structure
- `nbtreader.py`: Module for reading and parsing NBT files, converting them into Minecraft predicates.
- `rotate.py`: Module for rotating predicates.
- `from_nbt_to_predicate.py`: Main script for converting NBT to JSON predicate with the ability to specify the center of the structure against which the predicate will be checked.

## Dependencies
The project uses only the standard Python library and does not require any third-party packages.

## License
This project is distributed under the MIT license. See the `LICENSE` file for details.

