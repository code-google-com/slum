#
# vector - a vector like datatype (based on color)
# normal - a normal like datatype (based on vector)
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


from color import *
import math

class vector(color):
	internal = ['x','y','z']
	def length(self):
		self.createData()
		return math.sqrt( (self.data[0] * self.data[0]) + (self.data[1] * self.data[1]) + (self.data[2] * self.data[2]) )
	def normalize(self):
		len = self.length()
		return vector(self.data[0]/len, self.data[1]/len, self.data[2]/len)

class normal(vector):
	pass