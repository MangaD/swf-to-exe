import struct

projectorData = None
swfData = None
footer = bytearray(b'\x56\x34\x12\xFA')

def swf2exe_win(in_file, out_file, projector):
	with open(projector, "rb") as proj:
		projectorData = proj.read()

	with open(in_file, "rb") as swf:
		swfData = swf.read()

	with open(out_file, "wb") as out:
		out.write(projectorData)
		out.write(swfData)
		out.write(footer)
		out.write(struct.pack("i", len(swfData)))

# ATTENTION: Linux x64 projector needs to be patched first!
# Check out: https://github.com/shockpkg/swf-projector
def swf2exe_lin(in_file, out_file, projector, is64):
	with open(projector, "rb") as proj:
		projectorData = proj.read()
		#projectorData = projectorData.replace(b'Adobe Flash Player ', b'New Title\0') # Change window title

	with open(in_file, "rb") as swf:
		swfData = swf.read()

	with open(out_file, "wb") as out:
		out.write(projectorData)
		if not is64:
			out.write(struct.pack("i", len(swfData)))
			out.write(footer)
		else:
			out.write(struct.pack("<q", len(swfData))) # q=8 bytes, i=4 bytes, < little endian, > big endian
			out.write(footer + b'\xFF\xFF\xFF\xFF') # 64-bit version uses 8 bytes now (probably using size_t)
		out.write(swfData)