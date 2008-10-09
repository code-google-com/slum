#
# slumNode -  classNode that evaluates the slum class stored in a node and
#			  makes its object available as self.slum
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
# ------------------------------------------------------------


from classNode import *
import slum

class slumNode(classNode):
	'''
		derivated from classNode, this class adds the advantage of evaluating an slum attribute automaticaly, if
		one is present in a node.
		Instead of returning the string value of the slum attribute, it returns the evaluated class object
		from the code in the string attribute.
	'''
	def __init__(self, node, data=None):
		classNode.__init__(self, node, data)
		self.evalSlumClass()
	def evalSlumClass(self):
		if classNode.has_key(self, 'slum'):
			classe = classNode.__getitem__(self,'slum')
			if classe:
				self.slum = slum.evalSlumClass(classe['code'], classe['name'])
				self.updated = slum.checkMD5(classe['md5'], classe['path'])

	