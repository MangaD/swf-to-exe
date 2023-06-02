#!/usr/bin/python

import sys
import swflib

def printHelp():
	print("Usage:")
	print(sys.argv[0] + " <windows|linux32|linux64> <swf> <out_exe> <projector>")

if __name__ == "__main__":
	if len(sys.argv) < 5:
		printHelp()
	else:
		if sys.argv[1] == "windows":
			swflib.swf2exe_win(sys.argv[2], sys.argv[3], sys.argv[4])
		elif sys.argv[1] == "linux32":
			swflib.swf2exe_lin(sys.argv[2], sys.argv[3], sys.argv[4], False)
		elif sys.argv[1] == "linux64":
			swflib.swf2exe_lin(sys.argv[2], sys.argv[3], sys.argv[4], True)
		else:
			printHelp()

