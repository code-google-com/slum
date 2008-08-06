#
# shaderBase - 	defines a base class for slum maya nodes. Also defines a class
#				AETemplate responsable for the node UI.
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

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as m
from maya.mel import eval as meval
from nodeFactory import *
import slumMaya
import slum
import textwrap


class AETemplate:
	def __init__(self, nodeType):
		'''
			This class initialize an AETemplate for a given nodetype dinamycally.
			When the class is created, it sources a piece of mel code that register a
			global proc AEnodetypeTemplate for the given nodetype.
			This base global proc just calls the static method template of this class, where
			the code for the template really is, in python.
			Hopefully, in future versions of maya we will be able to use python procs directly.
		'''
		mel =  '''
			global proc AE%sTemplate(string $nodeName)
			{
				python ("import slumMaya\\nslumMaya.AETemplate.template('"+$nodeName+"')");
			}
		''' % nodeType
		meval( mel )

	@staticmethod
	def template(nodeName):
		'''
			The base template code.
			Basically, it sets up a scroll layout, adds an extra attributes layout and
			suppress all attributes found in the node.
			The real important one is the add of a callCustom template that calls the
			static method customUI of this class, at runtime.
			Unfortunately, we need to rely on a small portion of mel code to trigger the call for
			our customUI method, since a callCustom only calls mel global procs.
			Hopefully, in future versions of maya we will be able to use python procs directly.
		'''
		node = slumMaya.slumNode(nodeName)

		m.editorTemplate( beginScrollLayout=True )

		# supress everything
		for each in node.keys():
			m.editorTemplate( suppress=each )

		# we need to register another global proc, as editorTemplate python command only calls
		# mel procs (if theres a way to make it call a python function, we need to find out!)
		attrUICustom = 'attrUICustom_%s' % m.nodeType(nodeName)
		mel =  '''
			global proc %s(string $node)
			{
				python ("import slumMaya\\nslumMaya.AETemplate.customUI('"+$node+"')");
			}
			''' % (attrUICustom)
		meval( mel )
		m.editorTemplate( attrUICustom, attrUICustom, '', callCustom=True )

		# add extra controls
		m.editorTemplate( addExtraControls=True )
		m.editorTemplate( endScrollLayout=True )

	@staticmethod
	def _deleteLayoutIfExists(layoutName, type):
		'''
			checks for the existence of a layout with the given layoutName, of type "type"
			and deletes it, if it exists.
		'''
		parent = m.setParent(query=True)
		children = m.layout( parent, q=True, ca=True, )
		if children!=None:
			for child in children:
				if m.objectTypeUI( child, isType=type ) and child==layoutName:
					m.deleteUI( layoutName, layout=True );

	@staticmethod
	def customUI(nodeName):
		nodeName = nodeName.strip('.')
		slumNode = slumMaya.slumNode(nodeName)

		AETemplate.genericHeader(slumNode)
		AETemplate.parameters(slumNode)

	@staticmethod
	def genericHeader(slumNode):
		layoutName = "genericHeaderID_%s" % m.nodeType(slumNode.node)
		AETemplate._deleteLayoutIfExists( layoutName, 'columnLayout' )
		m.columnLayout( layoutName, visible=True, adjustableColumn=True )

		menu = m.optionMenuGrp(layoutName, label='renderer' )

		for each in slumNode.slum._renderers():
			m.menuItem( label = each )
		m.optionMenuGrp( menu, edit=True )

		m.setParent('..')

	@staticmethod
	def parameters(slumNode):
		'''
			This is the method that creates the UI for our attributes.
			The UI is based in the data returned from the parameters method of
			the slum class associated with the node.
		'''

		# this garantees the layout will be rebuild properly everytime
		# the attribute editor is open/selected for a node.
		layoutName = "layoutID_%s" % m.nodeType(slumNode.node)
		AETemplate._deleteLayoutIfExists( layoutName, 'columnLayout' )
		m.columnLayout( layoutName, visible=True, adjustableColumn=True )

		# a recursive function to create our UI. perfect for hierarquical parameters
		def recursiveAddAttrUI( parameter ):
			if parameter.__class__.__name__ == 'group':
				m.frameLayout( label = parameter.name, collapse = not parameter.opened )
				m.columnLayout( visible=True, adjustableColumn=True )

				for each in parameter.value:
					recursiveAddAttrUI( each )

				m.setParent('..')
				m.setParent('..')

			elif parameter.__class__.__name__ == 'button' or parameter.ui.__class__.__name__ == 'button':
				m.button( l = parameter.name, c = parameter.callback )
			elif parameter.__class__.__name__ == 'parameter':
				if not parameter.output:
					attribute = "%s.%s" % (slumNode.node, parameter.name)
					help = textwrap.fill(parameter.help,100)
					type = parameter.value.__class__.__name__
					value = parameter.value

					# custom UI
					if parameter.ui.__class__.__name__ == 'popup':
						popup=parameter.ui.values
						menu = m.optionMenuGrp( label=parameter.name )
						defaulValue=popup.keys()[0]
						for each in popup.keys():
							m.menuItem( label = each, data = popup[each] )
							if popup[each]==value:
								defaulValue = each
						m.optionMenuGrp( menu, edit=True, value=defaulValue, annotation=help )
						m.connectControl( menu, attribute, index=2)

					elif parameter.ui.__class__.__name__ == 'checkbox':
						checkbox = m.checkBoxGrp( numberOfCheckBoxes=1, label=parameter.name, annotation=help  )
						m.connectControl( checkbox, attribute, index=2)

					# normal parameters
					elif  type in ['float','int']:
						value=value
						min=parameter.min
						max=parameter.max
						m.attrFieldSliderGrp(
							sliderMinValue=parameter.min,
							sliderMaxValue=parameter.max,
							fmn=-100000000, fmx=10000000,
							attribute=attribute,
							label=parameter.name,
							annotation=help
						)

					elif type == 'str':
						ui=m.textFieldGrp( label=parameter.name, annotation=help )
						m.connectControl( ui, attribute, index=2)

					elif type == 'color':
						m.attrColorSliderGrp( attribute=attribute, label=parameter.name, annotation=help )

					else: # vectors/normals
						nameUI = '__%sUI' % parameter.name
						m.floatFieldGrp( nameUI, l=parameter.name, numberOfFields=3, annotation=help )
						m.connectControl( nameUI, '%sX' % attribute, index=2 )
						m.connectControl( nameUI, '%sY' % attribute, index=3 )
						m.connectControl( nameUI, '%sZ' % attribute, index=4 )

		recursiveAddAttrUI( slumNode.slum.parameters() )



class shaderBase:
	slum = None
	def __init__(self, slumFile=None):
		'''
			This is the base class used by slum custom nodes.
		'''
		pass
	def compute(self, plug, block):
		pass
	# plugin creation method (returns the class object)
	@staticmethod
	def nodeCreator():
		return OpenMayaMPx.asMPxPtr( shaderBase() )

	# plugin initializaton method (do nothing, as slumInitializer is the real deal, called after the node already exists)
	@staticmethod
	def nodeInitializer():
		# we do nothing here because we want to initialize it dinamically later, when the node already exists
		pass

	# this is the real initialization function... this is called after the node exists in maya.
	# so we can use this to dinamicaly add the shader attributes. Also, this can be called to refresh the node if the class
	# code changes.
	@staticmethod
	def slumInitializer(object, data):
		self = OpenMaya.MFnDependencyNode(object)
		node = slumMaya.slumNode(self.name())

		# dinamically source AETemplate for this node
		AETemplate( self.typeName() )

		# add the code to the slum attribute. After this is done, every call to slumNode will automatically
		# evaluate the slumClass
		classCache = slum.collectSlumClasses()
		nodeTypeName = self.typeName().strip('slum_')
		classe = filter( lambda x: x == nodeTypeName, classCache.allClasses.keys() )[0]
		node['slum'] = classCache.allClasses[classe]
		node.evalSlumClass()

		def recursiveAddAttr( parameter ):
			if parameter.__class__.__name__ == 'group':
				for each in parameter.value:
					recursiveAddAttr( each )
			elif parameter.__class__.__name__ == 'parameter':
				node[parameter.name] = parameter.value
				node.setInternal( parameter.name, True ) # add set/get callback
				node.setReadable( parameter.name, True )
				node.setStorable( parameter.name, True )
				if not parameter.output:
					node.setWritable( parameter.name, True )
				else:
					node.setWritable( parameter.name, False )

		recursiveAddAttr( node.slum.parameters() )

		# 3delight shader attributes - 3delight uses these to pickup shader parameters and code (like rsl code node)
		node['shadingParameters'] = ""
		node.setHidden('shadingParameters', True)
		node.setInternal('shadingParameters', True)

		node['shadingCode'] = ""
		node.setHidden('shadingCode', True)
		node.setInternal('shadingCode', True)

	# callback when changing parameters in the node
	def setInternalValueInContext ( self, plug, dataHandle,  ctx ):
		# false forces maya to set the value of the attribute as it should whitout a callback. False is default!
		return False

	# callback when reading parameters from the node
	def getInternalValueInContext ( self, plug, dataHandle,  ctx ):
		# false forces maya to get teh value of the attribute as it should whitout a callback. False is default!
		ret = False
		node = slumMaya.slumNode( self.name() )
		plugName = plug.name().split('.')[1]

		# 3delight
		dlParameters = ['shadingParameters', 'shadingCode']
		if plugName in dlParameters:
			delightShader = node.slum.delight( node )
			dataHandle.setString( '\n'.join( delightShader[ dlParameters.index(plugName) ] ) )
			ret = True

		# end of callback! False tells maya to return the attribute value. True returns dataHandle value!
		return ret
