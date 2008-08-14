#
# color - a color like datatype
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

class color:
	# internal variables to hold color data
	# its defined as a list, so classes based on this can alter it, like vectors use x,y and z
	internal = ['r','g','b']
	def __init__(self, data=0, data1=None, data2=None):
		self.checkValue(data)
		d = str(data)
		exec( 'self.%s = %s' % (self.internal[0], d) )
		exec( 'self.%s = %s' % (self.internal[1], d) )
		exec( 'self.%s = %s' % (self.internal[2], d) )
		if data1!=None:
			self.checkValue(data1)
			self.checkValue(data2)
			exec( 'self.%s = %s' % (self.internal[1], str(data1)) )
			exec( 'self.%s = %s' % (self.internal[2], str(data2)) )
	def checkKey(self, key):
		if key>2 or key<0:
			raise Exception('Color values can only have 3 elements. Element %d not valid' % key )
	def checkValue(self, value):
		if type(value) not in [int,long,float]:
			raise Exception('Data type "%s" not supported' % type(value))
	def createData(self):
		self.data = [
			eval('self.%s'% self.internal[0]),
			eval('self.%s'% self.internal[1]),
			eval('self.%s'% self.internal[2]),
		]
	def __getitem__(self, key):
		self.checkKey(key)
		return eval('self.%s'% self.internal[key])
	def __setitem__(self, key, value):
		self.checkKey(key)
		self.checkValue(value)
		exec('self.%s = %s'% (self.internal[key],str(value)) )
	def __repr__(self):
		self.createData()
		return '%s(%s,%s,%s)' % (self.__class__.__name__, str(self.data[0]), str(self.data[1]), str(self.data[2]))
	def __len__(self):
		return 3
	def __delitem__(self, key):
		pass