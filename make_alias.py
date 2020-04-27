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


# check for .bash_aliases or create if none exists
def check_for_alias_files():
	has_bash = False
	has_zsh = False
	has_zsh_rc = False
	if "linux" in os_sys:
		os.chdir("/home/" + user + "/")
		for pth in os.listdir("/home/" + user + "/"):
			if pth == ".bash_aliases":
				has_bash = True
			if pth == ".zsh_aliases":
				has_zsh = True
			if pth == ".zshrc":
				has_zsh_rc = True

		if not has_bash:
			try:
				p = subprocess.Popen(["touch", ".bash_aliases"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				output = p.communicate()[0]
				print(output)
			except Exception as e:
				print("Failed to make new .bash_aliases file!")
				print(str(e))
				exit(3)
		if not has_zsh:
			try:
				p = subprocess.Popen(["touch", ".zsh_aliases"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				output = p.communicate()[0]
				print(output)
			except Exception as e:
				print("Failed to make new .zsh_aliases file!")
				print(str(e))
				exit(3)
		if not has_zsh_rc:
			try:
				p = subprocess.Popen(["touch", ".zshrc"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				output = p.communicate()[0]
				print(output)
				with open(".zshrc", "w+") as f:
					f.write(". ~/.zsh_aliases")
					f.close()
			except Exception as e:
				print("Failed to make new .zshrc file!")
				print(str(e))
				exit(3)
	else:
		print("Your operating system is not compatible...sorry")
		sys.exit(6)

	if has_bash and has_zsh:
		get_script()


# get the path of the script/program the user wants to alias
def get_script():
	if args.p != "empty":
		script_addr = args.p
	else:
		print("Please provide full path of script")
		script_addr = input(">>> ")
	get_name(script_addr)


# get the name of the alias that invokes the script
def get_name(script_addr):
	if args.a != "empty":
		alias_name = args.a
	else:
		print("What would you like to call the alias name?")
		alias_name = input(">>> ")
	script = [script_addr, alias_name]
	make_alias(script)


# make alias name
def make_alias(path_n_name):
	user_path = path_n_name[0]
	aname = path_n_name[1]
	if sys.version_info > (3, 0):
		create_alias = "alias " + aname + '="python3 ' + user_path + '"\n'
	else:
		create_alias = "alias " + aname + '="python ' + user_path + '"\n'
	check_alias(create_alias)


# check if the alias already exists
def check_alias(alias_cmd):
	in_bash = False
	in_zsh = False
	if "linux" in os_sys:
		chk_bash = open("/home/" + user + "/.bash_aliases", "r")
		chk_zsh = open("/home/" + user + "/.zsh_aliases", "r")
	else:
		print("Your operating system is not compatible...sorry")
		sys.exit(6)

	for line in chk_bash.readlines():
		if line == alias_cmd:
			print("#" * 76)
			print(" " * 25 + "Alias already exists in .bash_aliases")
			print("#" * 76)
			chk_bash.close()
			in_bash = True
		else:
			continue

	for line in chk_zsh.readlines():
		if line == alias_cmd:
			print("#" * 76)
			print(" " * 25 + "Alias already exists in .zsh_aliases")
			print("#" * 76)
			chk_zsh.close()
			in_zsh = True
		else:
			continue
	if in_zsh or in_bash:
		sys.exit(0)
	chk_bash.close()
	chk_zsh.close()
	make_bash(alias_cmd)


# create the alias
def make_bash(alias_command):
	if "linux" in os_sys:
		bash_path = "/home/" + user + "/.bash_aliases"
		zsh_path = "/home/" + user + "/.zsh_aliases"
	else:
		print("Your operating system is not compatible...sorry")
		sys.exit(6)

	bash_pro = open(bash_path, "a")
	bash_pro.write(alias_command)
	bash_pro.close()
	x = subprocess.Popen(["source", bash_path], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	xput = x.communicate()[0]
	print(xput.decode())

	zsh_pro = open(zsh_path, "a")
	zsh_pro.write(alias_command)
	zsh_pro.close()
	x = subprocess.Popen(["source", zsh_path], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	xput = x.communicate()[0]
	print(xput.decode())

	print("#" * 76)
	print(" " * 18 + "Your new alias is now ready to use...")
	print("#" * 76)
	exit(0)


# just cause
def main():
	check_for_alias_files()


# starts the program
if __name__ == "__main__":
	main()
