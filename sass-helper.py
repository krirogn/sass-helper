#!/usr/bin/env python3

## ======= Imports ==================
import sys
import os
import shutil


## ======= Sanity Checks ============
## Check if sass cli is installed
if (not shutil.which("sass")):
	print("The dart-sass cli has to be installed (https://sass-lang.com/install)")
	exit(1)


## ======= Helper functions =========
## Checks if the path is valid and ends with /
def path_check(path: str) -> str:
	if (os.path.isfile(path)):
		print("The path must be to a directory")
		exit(1)

	correct_path = path
	if (not path.endswith("/")):
		correct_path += "/"

	return correct_path

## Returns a list of all files in a directory
def list_files(path: str) -> list[str]:
	return os.listdir(path)


## ======= Functions handlers =======
## Cleans temp files from folder
#  The temp files (.css.map) are generated
#  from the watch process 
def clean(path: str) -> None:
	path = path_check(path)
	print("Cleaning " + path)

	# Get a list of files to be removed
	files = []
	for file in list_files(path):
		if (file.endswith(".css.map")):
			files.append(file)
	
	# Sanity check if there are files
	if (len(files) < 1):
		print("No files to remove")
		exit()

	# Get the full path of files to be removed
	for i in range(len(files)):
		files[i] = path + files[i]

	# Remove files
	for file in files:
		if os.path.exists(file):
			print("File removed: " + file)
			os.remove(file)
		else:
			print("File doesn't exist: " + file)


## Builds all sass/scss files in a directory to css
def build(path: str) -> None:
	path = path_check(path)
	print("Building " + path)

	# Run sass cli
	command = f"sass {path}:{path}"
	print(f"Running: {command}")
	os.system(command)

## Continuously builds all sass/scss files in a directory to css
def watch(path: str) -> None:
	path = path_check(path)
	print("Watching files in " + path)

	# Run sass cli
	command = f"sass --no-source-map --watch {path}:{path}"
	print(f"Running: {command}")
	os.system(command)


## ======= Script arguments ========
##  If there is only one argument
if (len(sys.argv) == 2):
	# Prints the help info
	if sys.argv[1] == "--help" or sys.argv[1] == "-h":
		print("""
		Helper script to handle sass/scss files

		Usage: sass.py [option] <dir/to/sass/files/>

		━━━ Options ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
		-h, --help                     Shows info about how to use the script
		-c, --clean <dir>              Removes all temporary files from the directory
		-b, --build <dir> [-c]         Transpiles sass/scss files in a directory into css
		-w, --watch <dir>              Continuously watches sass/scss files in a directory
		""".replace("\t", "").strip() + "\n" + (" " * 31) + "and transpiles them into css")
		exit()
	# Default handler
	else:
		print("This argument isn't supported or lacks arguments, see -h for documentation")
		exit(1)

		

## If there are three arguments
if (len(sys.argv) >= 3):
	# Clean case
	if sys.argv[1] == "--clean" or sys.argv[1] == "-c":
		clean(sys.argv[2])
		exit()
	# Build case
	elif sys.argv[1] == "--build" or sys.argv[1] == "-b":
		build(sys.argv[2])

		if (len(sys.argv) == 4):
			if (sys.argv[3] == "-c" or sys.argv[3] == "--clean"):
				print()
				clean(sys.argv[2])
		
		exit()
	# Watch case
	elif sys.argv[1] == "--watch" or sys.argv[1] == "-w":
		watch(sys.argv[2])
		exit()
	# Default handler
	else:
		print("This argument isn't supported, see -h for documentation")
		exit(1)