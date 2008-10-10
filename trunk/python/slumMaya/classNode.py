#
# classNode - wraps a maya node as if it was a dictionary. Attrs are dictionary keys and
#			  adding a new key will add and attribute in the node.
# 			  this class makes use of color/vector datatype (color.py and vector.py) to create color/vectors attributes
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


import maya, os
import maya.mel as meval
import maya.cmds as m
import maya.OpenMaya as OpenMaya
from slum import * # color and vector datatypes

class classNode(dict):
	'''
		wraps a maya node as if it was a dictionary. Attrs are dictionary keys and
		adding a new key will add and attribute in the node.
		this class makes use of color/vector classes (color.py and vector.py) to create color/vectors attributes
		see slum for more info about color/vector classes

		classNode also have some special methods that wraps some really usefull api methods, like setConnectable and
		setInternal.
		Also, some low level api methos to return an MObject of the node, a MFnDependecyNode object of the node and
		MFnAttribute of the specified key (attribute)
	'''
	def __init__(self, node, data=None):
		self.node = node
		if data != None:
			if type(data) != dict:
				raise Exception("'%s' can only be initialized with a dict" % self.__class__.__name__)
			self.update(data)

	def attr(self, key):
		return "%s.%s" % (self.node, key)

	def addAttr(self, key, item, hidden=False):
		t = eval(item.__class__.__name__)
		# check the item type and create a proper attr in the node to accomodate the data type
		if not m.objExists( self.attr(key) ):
			if t in [int,long]:
				m.addAttr( self.node, ln=key,  at='long', hidden=hidden )
			elif t==float:
				m.addAttr( self.node, ln=key,  at='float', hidden=hidden )
			elif t==bool:
				m.addAttr( self.node, ln=key,  at='bool', hidden=hidden )
			elif t == str:
				m.addAttr( self.node, ln=key,  dt='string', hidden=hidden )
			elif t in [vector, normal, color]:
				isColor = False
				dataTypes={
					vector: ['X','Y','Z'],
					normal: ['NX','NY','NZ'],
					color:  ['R','G','B'],
				}
				children=dataTypes[t]
				maya.cmds.addAttr( self.node, ln=key,  at="float3", usedAsColor=t is color, hidden=False )
				maya.cmds.addAttr( self.node, ln="%s%s" % (key,children[0]), at="float", dv=int(item[0]), keyable=True, parent=key, hidden=False )
				maya.cmds.addAttr( self.node, ln="%s%s" % (key,children[1]), at="float", dv=int(item[1]), keyable=True, parent=key, hidden=False )
				maya.cmds.addAttr( self.node, ln="%s%s" % (key,children[2]), at="float", dv=int(item[2]), keyable=True, parent=key, hidden=False )
			else:
				# if a unknown datatype, create a string attr and store as string
				m.addAttr( self.node, ln=key,  dt='string', hidden=True )

	def setAttr(self, key, item):
		self.addAttr(key, item)
		t = item.__class__.__name__
		if t=='str':
			m.setAttr( self.attr(key), item,  type="string" )
		elif t in ['vector', 'normal', 'color']:
			m.setAttr( self.attr(key), item[0], item[1], item[2], type="double3" )
		elif t in ['dict','_dict','list','tuple']: #handle dict/list/tuple as special string data that will be retrieve as python dict/list/tuple
			m.setAttr( self.attr(key), "%s/%s" % (item.__class__.__name__,str(item)), type="string" )
		else:
			m.setAttr( self.attr(key), item )

	def getAttr(self, key):
		if not m.objExists( self.attr(key) ):
			raise Exception( 'Attribute %s does not exist in node.' % self.attr(key) )
		value = m.getAttr(self.attr(key))
		ret = value
		t = type(ret)
		if t in [str, unicode]:
			ret = str(value)
			# check if its a python dict, list or tuple. if so, return our wrapper to trigger updates automatically
			dataType = ret.split('/')[0]
			if dataType in ['dict','list','tuple']:
				data = eval(ret.replace('%s/' % dataType,''))
				#print '\n\ntttttt:', data, '\n\n'
				ret = self._dict(self, key)
				ret.update(data, callingFromClassNode=True)
				#print '\n\ntttttt:', ret, '\n\n'
		elif t in [list]:
			if m.objExists( "%sX" % self.attr(key) ):
				ret = vector(value[0][0], value[0][1], value[0][2])
			elif m.objExists( "%sNX" % self.attr(key) ):
				ret = normal(value[0][0], value[0][1], value[0][2])
			elif m.objExists( "%sR" % self.attr(key) ):
				ret = color(value[0][0], value[0][1], value[0][2])
			else:
				ret = [value[0][0], value[0][1], value[0][2]]
		return ret

	def __setitem__(self, key, item):
		self.setAttr(key, item)

	def __getitem__(self, key):
		return self.getAttr(key)

	def __repr__(self):
		name = self.__class__.__name__
		list = {}
		for each in self.keys():
			list[each] = self.getAttr(each)
		return "%s('%s',%s)" % (name, self.node, str(list) )
	def __str__(self):
		return self.__repr__()

	def __len__(self):
		return len(m.listAttr(self.node))

	def keys(self):
		excluded = ['message']
		excludedTypes = ['TdataCompound']
		list = []
		for each in m.listAttr(self.node):
			try:
				if each not in excluded and '.' not in each:
					if m.getAttr(self.attr(each), type=True) not in excludedTypes :
						list.append(str(each))
			except:
				pass
		return list

	def has_key(self,f):
		return f in m.listAttr(self.node)

	def update(self,f):
		if type(f) != dict:
			raise Exception('%s.update only accepts dicts' % self.__class__.__name__)
		for each in f:
			self.setAttr(each, f[each])

	def __delitem__(self, key):
		m.deleteAttr(self.attr(key))




	def MObject(self):
		list = OpenMaya.MSelectionList()
		list.add( self.node )
		mobj = OpenMaya.MObject()
		list.getDependNode( 0, mobj )
		return mobj

	def MFnDependencyNode(self):
		return OpenMaya.MFnDependencyNode( self.MObject() )

	def MFnAttribute(self, key):
		return OpenMaya.MFnAttribute( self.MFnDependencyNode().attribute( key ) )

	def _setNeededAttributes(self, key):
		ret=[key]
		if self.__getitem__(key).__class__.__name__ in ['color']:
			ret.extend(['%sR' % key,'%sG' % key,'%sB' % key])
		elif self.__getitem__(key).__class__.__name__ in ['vector','normal']:
			ret.extend(['%sX' % key,'%sY' % key,'%sZ' % key])
		return ret

	def setInternal(self, key, value=True):
		for each in self._setNeededAttributes(key):
			self.MFnAttribute(each).setInternal(value)

	def setReadable(self, key, value=True):
		for each in self._setNeededAttributes(key):
			self.MFnAttribute(each).setReadable(value)

	def setStorable(self, key, value=True):
		for each in self._setNeededAttributes(key):
			self.MFnAttribute(each).setStorable(value)

	def setWritable(self, key, value=True):
		for each in self._setNeededAttributes(key):
			self.MFnAttribute(each).setWritable(value)

	def setHidden(self, key, value=False):
		for each in self._setNeededAttributes(key):
			self.MFnAttribute(each).setHidden(value)

	def setConnectable(self, key, value=True):
		for each in self._setNeededAttributes(key):
			self.MFnAttribute(each).setConnectable(value)

	class _dict(dict):
		'''
		_classNode = classNode that own this data
		key = original key(attr) in the classnode
		index = all the keys that are needed to get to this data from the original classNode attr(list)
		'''
		def ____updateFromClassNode(self):
			if not self.updatingFrom:
				self.updatingFrom = True
				dict.clear(self)
				data = self._classNode.getAttr(self.key)
				data.updatingFrom = True
				index = "['%s']" % ']['.join(self.index)
				if not self.index:
					index=""
				dict.update( self, eval( 'data%s' % index ) )
				data.updatingFrom = False
				self.updatingFrom = False

		def ____updateToClassNode(self):
			if not self.updating:
				self.updating = True
				data = self._classNode.getAttr(self.key)
				data.updatingFrom = True
				index = "['%s']" % ']['.join(self.index)
				if not self.index:
					index=""
				exec( 'data%s=%s' % ( index, dict.__repr__(self) ) )
				self._classNode.setAttr(self.key, data)
				#data.updatingFrom = False
				self.updating = False

		def __init__(self, _classNode, key,  index=[]):
			self.updating = False
			self.updatingFrom = False
			dict.__init__(self)
			self.key = key
			self._classNode = _classNode
			self.index = index
		def __setitem__(self, key, item):
			t = item.__class__.__name__
			if t in ['dict','_dict']:
				dict.__setitem__( self, key, _dict(self.classNode, self.key, self.index+[key]).update(item) )
			else:
				dict.__setitem__(self, key, item)
			self.____updateToClassNode()
		def update(self, data, callingFromClassNode=False):
			if not callingFromClassNode:
				self.____updateFromClassNode()
			dict.update(self, data)
			if not callingFromClassNode:
				self.____updateToClassNode()
		def __delitem__(self, key):
			self.____updateFromClassNode()
			dict.__delitem__(self, key)
			self.____updateToClassNode()
		def __getitem__(self, key):
			self.____updateFromClassNode()
			return dict.__getitem__(self, key)
		def __repr__(self):
			self.____updateFromClassNode()
			return dict.__repr__(self)
		def __len__(self):
			self.____updateFromClassNode()
			return dict.__len__(self)
		def keys(self):
			self.____updateFromClassNode()
			return dict.keys(self)
		def has_key(self,f):
			self.____updateFromClassNode()
			return dict.has_key(self,f)

#need to add API utils to do affectsAttributo, callbacks, etc...
