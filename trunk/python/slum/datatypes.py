#
# datatypes.py - all slum custom datatypes
#
#    Copyright (C) 2008 - Roberto Hradec
#
# ---------------------------------------------------------------------------
#	 This file is part of SLUM.
#
#    SLUM is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    SLUM is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with SLUM.  If not, see <http://www.gnu.org/licenses/>.
# ---------------------------------------------------------------------------

import math

class color:
	''' slum datatype to hold color data.
	The "internal" variable is a list that defines all the possible keys for this datatype. For color,
	they are [r,g,b], but they can be overriden by derivated classes, like vector, which defines it as
	x,y,z.
	This datatype is defined to simplify a shader implementation, specially when defining slum
	shader parameters.'''

	internal = ['r','g','b']
	def __init__(self, data=0, *args):
		self.checkValue(data)
		for each in self.internal:
			self.__dict__[each] = data
		nargs = len(args)
		if nargs:
			if nargs==len(self.internal)-1:
				internalIndex=1
				for each in args:
					self.checkValue(each)
					self.__dict__[self.internal[internalIndex]] = each
					internalIndex += 1
			else:
				raise Exception('dataype requires 1 or %d parameters in initialization. Received only %d parameters.' % (len(self.internal),nargs+1))
	def checkKey(self, key):
		if key>len(self.internal) or key<0:
			raise Exception('Color values can only have 3 elements. Element %d not valid' % key )
	def checkValue(self, value):
		if type(value) not in [int,long,float]:
			raise Exception('Data type "%s" not supported' % type(value))
	def __getitem__(self, key):
		self.checkKey(key)
		return self.__dict__[self.internal[key]]
	def __setitem__(self, key, value):
		self.checkKey(key)
		self.checkValue(value)
		self.__dict__[self.internal[key]] = value
	def __repr__(self):
		data = []
		for each in self.internal:
			data.append("%s" % str(self.__dict__[each]))
		return '%s(%s)' % (self.__class__.__name__,','.join(data))
	def __len__(self):
		return 3
	def __delitem__(self, key):
		pass

class vector(color):
	'''
		slum datatype to hold vector data.
		its derivated from color, overriding the internal to x,y,z.
		also, theres 2 added method to manipulate vectors: lenght and normalize
	'''
	internal = ['x','y','z']
	def length(self):
		return math.sqrt(
			(self.__dict__[self.internal[0]] * self.__dict__[self.internal[0]]) +
			(self.__dict__[self.internal[1]] * self.__dict__[self.internal[1]]) +
			(self.__dict__[self.internal[2]] * self.__dict__[self.internal[2]])
		)
	def normalize(self):
		len = self.length()
		return vector(
			self.__dict__[self.internal[0]]/len,
			self.__dict__[self.internal[1]]/len,
			self.__dict__[self.internal[2]]/len
		)

class normal(vector):
	'''
		slum datatype to hold normal data.
		its exactly like vector. Its defined just as a placeholder for people used to rsl. (like me :D)
	'''
	pass

class point(vector):
	'''
		slum datatype to hold point data.
		its exactly like vector. Its defined just as a placeholder for people used to rsl. (like me :D)
	'''
	pass