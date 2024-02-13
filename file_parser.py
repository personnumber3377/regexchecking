
import re
import sys
import subprocess
import os
import time
from shlex import quote
import random


DEBUG = 1

def debug(string: str) -> None:
	if DEBUG:
		print("[DEBUG] "+str(string))


def find_regex_in_line(line: str): # Returns false if no regex. Returns the regex string if found.
	debug("Line: "+str(line))
	if line.count("/") == 2 and "=~" in line:
		first_slash_ind = line.index("/")
		rest_of_string = line[first_slash_ind+1:]
		rest_of_string = rest_of_string[:rest_of_string.index("/")+1]
		final_regex = "/"+rest_of_string
		if len(final_regex) <= 5:
			return False # False positive
		fh = open("regex_list.txt", "a")
		fh.write(final_regex+"\n")
		fh.close()
		return final_regex


RECHECK_DIR = "/home/cyberhacker/Asioita/regexchecking/recheck/modules/recheck-cli/target/native-image/"

def get_string(string: str) -> str:
	debug("Here is the string in get_string: "+str(string))
	new_string = string[string.index("'")+1:]
	print("new_string == "+str(new_string))
	if "'" in new_string:

		new_string = new_string[:new_string.index("'")]
	else:
		return new_string
	return new_string

#STRING_COUNT = 3

STRING_COUNT = 100000


def parse_repeated(tok) -> str:
	debug("Processing repeated token: "+str(tok))
	assert tok.count("'") == 2
	
	# Now just return the shit.
	oof_string = get_string(tok)

	final_string = oof_string * STRING_COUNT
	return final_string

def parse_repeated_debug(tok) -> str:
	debug("Processing repeated token: "+str(tok))
	assert tok.count("'") == 2
	
	# Now just return the shit.
	oof_string = get_string(tok)

	final_string = oof_string * 10
	return final_string


def exec_str(string: str) -> str: # This evaluates the attack str string.
	tokens = string.split(" + ")
	# This is here to check for ' ' <--- this case
	if tokens.count("'") == 2:
		ind_of_string_start = tokens.index("'")
		if tokens[ind_of_string_start+1] == "'":
			tokens[ind_of_string_start] = "' '"
			tokens.pop(ind_of_string_start+1)
	while "+" in tokens:
		tokens.remove("+")
	# Now evaluate the string.
	out = ""
	for tok in tokens:
		if "repeat" in tok:
			out += parse_repeated(tok)
		else:
			out += get_string(tok)
	debug("Here is the final payload string: "+str(out))
	return out

def exec_str_debug(string: str) -> str: # This evaluates the attack str string.
	tokens = string.split(" + ")
	# This is here to check for ' ' <--- this case
	if tokens.count("'") == 2:
		ind_of_string_start = tokens.index("'")
		if tokens[ind_of_string_start+1] == "'":
			tokens[ind_of_string_start] = "' '"
			tokens.pop(ind_of_string_start+1)
	while "+" in tokens:
		tokens.remove("+")
	# Now evaluate the string.
	out = ""
	for tok in tokens:
		if "repeat" in tok:
			out += parse_repeated_debug(tok)
		else:
			out += get_string(tok)
	debug("Here is the final payload string: "+str(out))
	return out

def rand_str(length: int) -> str:
	alphabet = "abcdefghijklmnopqrstuvxyz"
	return ''.join([random.choice(alphabet) for _ in range(length)])

def parse_payload(contents, regex_str, debug=False, final_order=None, attack_string=None, filename=None) -> str:
	if "Attack string: " not in contents:
		return
	attack_str = contents[contents.index("Attack string: ")+len("Attack string: "):]
	print(attack_str)
	attack_str = attack_str[:attack_str.index("\n")]
	print("Here is the attack_str: "+str(attack_str))
	if "' '" in attack_str:
		return
	payload = exec_str(attack_str)
	if debug:

		debug_thing = exec_str_debug(attack_str)
		fh = open("debug/"+str(rand_str(10)), "w")
		fh.write(debug_thing)
		fh.write("\n\n\n")
		fh.write(regex_str)
		fh.write("\n\n\n")
		fh.write("Here is the order: "+str(final_order))
		fh.write("\n\n\n")
		fh.write(attack_str)
		fh.write("\n\n\n")
		fh.write(filename)
		fh.close()
	# write the string to the file and then pass the regex to this ruby script.
	fh = open("attack_str.txt", "w")
	fh.write(payload)
	fh.close()



ORDERS = ["2nd", "3rd", "4th", "5th", "6th", "7th", "8th"]

def classify_regex(regex_str: str, filename: str) -> None:

	#command_str = "./recheck --attack-limit 1000  --enable-log "/^(a|a)*$/""
	command_str = RECHECK_DIR + "recheck --attack-limit 1000  --enable-log "+str(quote(regex_str))+" > output.txt"
	# Now we run the command and get output.
	#output = subprocess.check_output(command_str.split(" "))
	print("Here is the output from recheck:")
	#print(output)
	os.system(command_str)
	time.sleep(0.2)
	fh = open("output.txt", "r")
	contents = fh.read()
	fh.close()
	if "safe" in contents:
		return
	final_order = None
	debug_mode = False
	for order in ORDERS:
		if order in contents:
			print(str(order)+" found at here: "+str(regex_str)+" at filename "+str(filename))
			if order == "2nd" or order == "3rd" or order == "4th" or order == "5th" or order == "6th" or order == "7th" or order == "8th":
				final_order = order
				debug_mode = True
			break
	#if "4th" in contents:
	#	print("4th!!!! "+str(filename))
	print(contents)


	string = None
	#if debug_mode:
	#	string = contents[contents.index("Attack ")]
	#	string = string[string.index("\n")]

	# Here get the attack payload.
	attack_payload = parse_payload(contents, regex_str, debug=debug_mode, final_order=final_order, attack_string=string, filename=filename)
	# Write the actual regex to regex.txt
	fh = open("regex.txt", "w")
	fh.write(regex_str[1:-1]) # 1 and -1 , because we do not need the "/" characters.
	fh.close()

	redos_command = "ruby shit.rb"

	# Now try running the benchmark. If it times out, then we may have redos.
	debug("Running this command: "+str(redos_command))

	os.system(redos_command)

	return

def sanitize_regex(regex: str) -> str:
	new_regex = regex
	if new_regex[1:3] == "\\A":
		print("poopoo")
		new_regex = "/"+new_regex[3:]
	if new_regex[-3:] == "\\z/":
		new_regex = new_regex[:-3]+"/"
	print("new_regex == "+str(new_regex))
	assert new_regex.count("/") == 2
	assert "\\A" != new_regex[1:3]
	assert "\\z/" != new_regex[-3:]
	return new_regex

def get_regexes(filename: str) -> list:
	# Get's every single regex pattern from a singular file.
	# This is a regex to detect regexes. :D
	#regex_regex = re.compile(r'/((?:(?:[^?+*{}()[\]\\|]+|\\.|\[(?:\^?\\.|\^[^\\]|[^\\^])(?:[^\]\\]+|\\.)*\]|\((?:\?[:=!]|\?<[=!]|\?>)?(?1)??\)|\(\?(?:R|[+-]?\d+)\))(?:(?:[?+*]|\{\d+(?:,\d*)?\})[?+]?)?|\|)*)/')
	fh = open(filename, "r")
	try:
		lines = fh.readlines()
	except:
		print("Paskaaaaaa "+str(filename))
		fh.close()
		return
	fh.close()

	for line in lines:
		# Check for two "/" characters.
		maybe_regex = find_regex_in_line(line)
		debug("Maybe regex: "+str(maybe_regex))
		if maybe_regex:
			assert maybe_regex.count("/") == 2
			debug("Here is a regex which we found: "+str(maybe_regex))
			# Here maybe check for a bad regex????
			maybe_regex = sanitize_regex(maybe_regex) # This is to get rid of the "\A" marker for example which recheck thinks is actually an "A" character. same with "\z"
			classify_regex(maybe_regex, filename)


'''

recheck [--acceleration-mode <mode>] [--attack-limit <integer>] [--attack-timeout <duration>] [--checker <checker>] [--crossover-size <integer>] [--heat-ratio <floating-point>] [--incubation-limit <integer>] [--incubation-timeout <duration>] [--enable-log] [--max-attack-string-size <integer>] [--max-degree <integer>] [--max-gene-string-size <integer>] [--max-generation-size <integer>] [--max-initial-generation-size <integer>] [--max-iteration <integer>] [--max-nfa-size <integer>] [--max-pattern-size <integer>] [--max-recall-string-size <integer>] [--max-repeat-count <integer>] [--max-simple-repeat-count <integer>] [--mutation-size <integer>] [--random-seed <integer>] [--recall-limit <integer>] [--recall-timeout <duration>] [--seeder <seeder>] [--seeding-limit <integer>] [--seeding-timeout <duration>] [--timeout <duration>] <pattern>

recheck --attack-limit 1000 --attack-timeout 10000 --enable-log "a*a"

'''


BLACKLIST_STRINGS = ["test", "rdoc", "bundler", "shit"]

def main() -> int:
	# This file checks each file in the current directory for the redos vulnerability.
	import os
	rootdir = '.'
	debug("len(sys.argv) == "+str(len(sys.argv)))
	if len(sys.argv) == 2: # There is a directory after the script
		rootdir = sys.argv[-1]
	all_regexes = []

	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			#print(os.path.join(subdir, file))

			filename = os.path.join(subdir, file)
			debug("Filename : "+str(filename))
			if any([string in filename for string in BLACKLIST_STRINGS]):
				#debug("Blacklisted filename: "+str(filename))
				continue
			# Get the regexes
			#all_regexes += get_regexes(filename)
			if ".rb" not in filename:
				continue
			debug("Now trying to read this: "+str(filename))
			get_regexes(filename)
	print("Done!")
	return 0

if __name__=="__main__":
	exit(main())
