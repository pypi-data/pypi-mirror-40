# ipbook

*Allows you to save IP addresses so that they are accessible in the command line*

## Installation

```
git clone https://github.com/bypie5/ipbook.git
cd ipbook
pip install .
```

## Usage

### Add a Record

```
ipbook add [ip] [name]

ex: ipbook add 127.0.0.1 localhost
```

*NOTE: You cannot add entries with duplicate names*

___

### Show All Records

```
ipbook list
```
```
sample output:
1) localhost: 127.0.0.1

```

___

### Delete a Record

```
ipbook remove [name]

ex: ipbook remove localhost
```

___
