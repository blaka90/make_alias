#! /user/bin/env python
import os
import subprocess
import getpass
import argparse
import sys

user = getpass.getuser()
os_sys = sys.platform

parser = argparse.ArgumentParser(description="creates an alias for script to be used anywhere in terminal by keyword")
parser.add_argument("-p", nargs="?", help="specify the full path of script to alias", default="empty")
parser.add_argument("-a", nargs="?", help="specify the alias keyword you want to use", default="empty")
args = parser.parse_args()


# get the path of the script/program the user wants to alias
def get_script():
	if args.p != "empty":
		script_addr = args.p
	else:
		print "Please provide full path of script"
		script_addr = raw_input(">>> ")
	get_name(script_addr)


# get the name of the alias that invokes the script
def get_name(script_addr):
	if args.a != "empty":
		alias_name = args.a
	else:
		print "What would you like to call the alias name?"
		alias_name = raw_input(">>> ")
	script = [script_addr, alias_name]
	make_alias(script)


# check for .bash_profile or create if none exists
def check_bash():
	if "linux" in os_sys:
		os.chdir("/home/" + user + "/")
		for pth in os.listdir("/home/" + user + "/"):
			if pth == ".bash_aliases":
				get_script()
			else:
				continue
		try:
			p = subprocess.Popen(["touch", ".bash_aliases"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output = p.communicate()[0]
			print output
			get_script()
		except Exception as e:
			print "Failed to make new .bash_profile"
			print str(e)
			exit(3)
	elif "darwin" in os_sys:
		os.chdir("/Users/" + user + "/")
		for pth in os.listdir("/Users/" + user + "/"):
			if pth == ".bash_profile":
				get_script()
			else:
				continue
		try:
			p = subprocess.Popen(["touch", ".bash_profile"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output = p.communicate()[0]
			print output
			get_script()
		except Exception as e:
			print "Failed to make new .bash_profile"
			print str(e)
			exit(3)
	else:
		print "Your operating system is not compatible...sorry"
		sys.exit(6)



# check if the alias already exists
def check_alias(alias_cmd):
	if "linux" in os_sys:
		chk_bash = open("/home/" + user  + "/.bash_aliases", "r")
	elif "darwin" in os_sys:
		chk_bash = open("/Users/" + user + "/.bash_profile", "r")
	else:
		print "Your operating system is not compatible...sorry"
		sys.exit(6)

	for line in chk_bash.readlines():
		if line == alias_cmd:
			print "#" * 76
			print " " * 25 + "Alias already exists"
			print "#" * 76
			chk_bash.close()
			exit(0)
		else:
			continue
	chk_bash.close()
	make_bash(alias_cmd)


# make alias name
def make_alias(path_n_name):
	user_path = path_n_name[0]
	aname = path_n_name[1]
	create_alias = "alias " + aname + '="python ' + user_path + '"\n'
	check_alias(create_alias)


# create the alias
def make_bash(alias_command):
	if "linux" in os_sys:
		bash_path = "/home/" + user + "/.bash_aliases"
	elif "darwin" in os_sys:
		bash_path = "/Users/" + user + "/.bash_profile"
	else:
		print "Your operating system is not compatible...sorry"
		sys.exit(6)

	bash_pro = open(bash_path, "a")
	bash_pro.write(alias_command)
	bash_pro.close()
	x = subprocess.Popen(["source", bash_path], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	xput = x.communicate()[0]
	print xput
	print "#" * 76
	print " " * 18 + "Your new alias is now ready to use..."
	print "#" * 76
	exit(0)


# just cause
def main():
	check_bash()

# starts the program
if __name__ == "__main__":
	main()
