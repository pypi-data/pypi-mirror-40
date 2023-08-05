import os, argparse, json

dir_path, file_name = os.path.split(os.path.abspath(__file__))
data_path = os.path.join(dir_path, 'data/ip_addrs.json')

def loc_fname(ips, fname):
	for i, entry in enumerate(ips):
		if entry["name"] == fname:
			return i
	return -1

def add_ip(args):
	with open(data_path, "r+") as f:
		data = json.load(f)
		if loc_fname(data["ips"], args.fname) == -1:
			f.seek(0)
			data["ips"].append({"ip": args.ip, "name": args.fname})
			json.dump(data, f)
			print("Added " + args.fname)
		else:
			print("Cannot add duplicate name!")

def list_ips(args):
	with open(data_path) as f:
		data = json.load(f)
	
	for i, entry in enumerate(data["ips"]):
		print(str(i+1) + ") " + data["ips"][i]["name"] + ": " + data["ips"][i]["ip"])
	
def delete_ip(args):
	with open(data_path) as f:
		data = json.load(f)
		f.seek(0)
		
	i = loc_fname(data["ips"], args.fname)
	if not i == -1:
		del data["ips"][i]
		with open(data_path, "w+") as o:	
			json.dump(data, o)

		print ("Deleted " + args.fname)
	else:
		print(args.fname + " not in records")

def main():
	parser = argparse.ArgumentParser(description=
		"Save a list of your most commonly used IP addresses")
	subparser = parser.add_subparsers()

	# Add command
	add_parser = subparser.add_parser('add', help="Save new IP")
	add_parser.add_argument('ip', help="IP Address")
	add_parser.add_argument('fname', help="Friendly name for the IP (Quotes)")
	add_parser.set_defaults(func=add_ip)

	# List command
	list_parser = subparser.add_parser('list', help="Show all saved IPs")
	list_parser.set_defaults(func=list_ips)

	# Delete command
	delete_parser = subparser.add_parser('remove', help=
		"Remove IP record by friendly name")
	delete_parser.add_argument('fname', help="Record's friendly name")
	delete_parser.set_defaults(func=delete_ip)


	args = parser.parse_args()
	args.func(args)

if __name__ == '__main__':
	main()
