# functions to help build stl files
import numpy as np
import struct 
from bitstring import BitArray

class STLFacet:
	"""a single polygon facet that knows how to encode itself when asked"""

	def __init__(self, pt1, pt2, pt3):
		# Calculate the normal for this facet

		self.p1 = np.array([pt1[0], pt1[1], pt1[2]])
		self.p2 = np.array([pt2[0], pt2[1], pt2[2]])
		self.p3 = np.array([pt3[0], pt3[1], pt3[2]])

		# These two vectors are in the plane
		v1 = self.p3 - self.p1
		v2 = self.p2 - self.p1

		# the cross product is a vector normal to the plane
		cp = np.cross(v1, v2)
		self.normal_a, self.normal_b, self.normal_c = cp


	def get_text_encoding(self):
		list_out = []
		# TODO further refactor to bring strings up to standard usage
		# normal, a, b, c)
		list_out.append("facet normal " + "%E" % self.normal_a + " " + "%E" % self.normal_b + " " + "%E" % self.normal_c + "\n"))
		list_out.append("\touter loop\n")
		# first corner points 0,1,2
		list_out.append("\t\tvertex " + "%E" % self.p1[0] + " " + "%E" % self.p1[1] + " " + "%E" % self.p1[2] + "\n")
		# second corner points 0,1,2
		list_out.append("\t\tvertex " + "%E" % self.p2[0] + " " + "%E" % self.p2[1] + " " + "%E" % self.p2[2] + "\n")
		# third corner points 0,1,2
		list_out.append("\t\tvertex " + "%E" % self.p3[0] + " " + "%E" % self.p3[1] + " " + "%E" % self.p3[2] + "\n")
		list_out.append("\tendloop\n")
		list_out.append("endfacet\n")
		return list_out

	def get_binary_encoding(self):
		# have to figure best way to return this next
		return None


class STLFile:
	"""Using the 'resource manager' pattern, this class provides the standard methods
		for use in a 'with' statement. As such, it opens the STL output file, and
		keeps the file open until the calling scope exits.
	"""

	def __init__(self, filepath, filetype, num_facets, solid_name=None):
		"""Initialize all resource parameters"""
		self.file_path = filepath
		self.file_type = filetype
		self.num_facets = num_facets
		self.solid_name = solid_name if solid_name else ""
		self.file_obj = None

	def __enter__(self):
		"""invoked by the 'with' statement, returns file-object for writing"""
		if self.file_type == 'txt':
			self.file_obj = open(self.file_path, 'w')
			self.file_obj.write(f'solid {self.solid_name}\n')
		elif self.file_path == 'bin':
			self.file_obj = open(self.file_path, 'wb')

			# TODO create this programmatically
			# create and write an 80 character header - any characters will do
			header = bytearray("STL Builder output          3         4         5         6         7         80",'utf8')
			self.file_obj.write(header)

			# write a 4-byte little-endian unsigned integer indicating the number of facets
			self.file_obj.write(self.num_facets.to_bytes(4, byteorder="little", signed=False))
		else:
			raise Exception(f'unknown file type {self.file_type}')

		return self.file_obj

	def __exit__(self, type, value, traceback):
		"""invoked when 'with' statement goes out of scope, properly terminates file."""
		if self.file_type == 'txt':
			stl_file.write(f'endsolid {self.solid_name}\n )

		if self.file_obj:
			self.file_obj.close()

	def append_facet(self, facet: STLFacet):
		"""Use this to write a facet to this STL resource"""
		if self.file_type == 'txt':
			lines_list = facet.get_text_encoding()
			for line in lines_list:
				self.file_obj.write(line)
		elif self.file_type == 'bin':
			data_list = facet.get_binary_encoding()
			for datum in data_list:
				self.file_obj.write(datum)
		else:
			raise Exception(f'unknown file_type {self.file_type}')



# TODO get rid of these functions once the rest of the app is converted
def Initialize_stl_file(filepath, filetype, num_facets, solid_name = ""):
	'''Write the front end of the stl file that goes before the facet data'''
	if filetype == "txt":
		with open(filepath, "w") as stl_file:
			stl_file.write("solid "+solid_name +"\n")
		return
	elif filetype == "bin":
		with open(filepath, "wb") as stl_file:
			#First, create and write an 80 character header - any characters will do
			#header = int(0).to_bytes(80,byteorder="little",signed=False)
			header = bytearray("STL Builder output          3         4         5         6         7         80",'utf8')
			stl_file.write(header)
			#Second, write a 4 byte little endian unsigned integer indicating the numebr of facets

			stl_file.write(num_facets.to_bytes(4,byteorder="little",signed=False))
			pass
		
		return

def Finalize_stl_file(triangle_count, filepath, filetype, solid_name = "" ):
	'''Write the end of the stl file that goes after the facet data'''
	if filetype  == "txt":
		with open(filepath, "w") as stl_file:
			stl_file.write("endsolid \n" + solid_name )
	elif filetype == "bin":
		#no ending stuff for a binary file 
		return



# TODO question - whether this should be a nested class in STLBuilder or standalone.
# if its not a nested class, we should simply allow it to write to the file
# otherwise we may want to add supporting methods to the builder to allow it to know how
# to write a facet. that would be a cleaner interface and properly hide things
# but i think the facet needs to know what to generate - just not how to write to a file

class STL_Facet():
	def __init__(self, pt1, pt2, pt3):
		#Calculate the normal for this facet
		
		self.p1 = np.array([pt1[0], pt1[1],pt1[2]])
		self.p2 = np.array([pt2[0], pt2[1],pt2[2]])
		self.p3 = np.array([pt3[0], pt3[1],pt3[2]])

		# These two vectors are in the plane
		v1 = self.p3 - self.p1
		v2 = self.p2 - self.p1

		# the cross product is a vector normal to the plane
		cp = np.cross(v1, v2)
		self.normal_a, self.normal_b, self.normal_c = cp


	def Append_facet_to_file(self, filepath, filetype):
		if filetype == "txt":
			with open(filepath, "a+") as stl_file:
				stl_file.write("facet normal "+ "%E"%self.normal_a + " " + "%E"%self.normal_b + " " +  "%E"%self.normal_c +"\n") # normal, a, b, c
				stl_file.write("\touter loop\n")
				stl_file.write("\t\tvertex " + "%E"%self.p1[0] + " " + "%E"%self.p1[1] + " " +  "%E"%self.p1[2] +"\n") # first corner points 0,1,2
				stl_file.write("\t\tvertex " + "%E"%self.p2[0] + " " + "%E"%self.p2[1] + " " +  "%E"%self.p2[2] +"\n") # second corner points 0,1,2
				stl_file.write("\t\tvertex " + "%E"%self.p3[0] + " " + "%E"%self.p3[1] + " " +  "%E"%self.p3[2] +"\n") # third corner points 0,1,2
				stl_file.write("\tendloop\n")
				stl_file.write("endfacet\n")
				
				
		elif filetype == "bin":
			with open(filepath, "ab") as stl_file:
				# I used the info here to figure out how to write these IEEE 32bit floating point numbers
				# from https://www.linuxquestions.org/questions/programming-9/write-a-file-fo-data-array-with-float-values-in-a-binary-format-in-python-937020/
				
				#Write the normal and each of the vertexes in IEEE floating point numbers
				stl_file.write(struct.pack('<%df' % 3, *[self.normal_a, self.normal_b, self.normal_c]))
				
				# Now write each of the three points in IEEE floating point numbers
				stl_file.write(struct.pack('<%df' % 3, *[self.p1[0], self.p1[1],self.p1[2]]))
				stl_file.write(struct.pack('<%df' % 3, *[self.p2[0], self.p2[1],self.p2[2]]))
				stl_file.write(struct.pack('<%df' % 3, *[self.p3[0], self.p3[1],self.p3[2]]))
				
				#Next, write 8 bytes as an attribute thing. Copies these (int 115 and int 73  from a file generated by Fusion 360. 
				stl_file.write(int(115).to_bytes(1,byteorder="little",signed=False))
				stl_file.write(int(78).to_bytes(1,byteorder="little",signed=False))

		else: print( "wtf? filetype not found" , filetype)
