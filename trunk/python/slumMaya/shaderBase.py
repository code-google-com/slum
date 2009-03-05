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
import os, md5, textwrap, sys

class AETemplate:
	'''
		This class initialize an AETemplate for a given nodetype dinamycally.
		Basically this avoid the need of having an AEnodetypTemplate.mel file.
		When the class is created, it sources a piece of mel code that register a
		global proc AEnodetypeTemplate for the given nodetype.
		This global proc just calls the static method template of this class, where
		the code for the template really is, in python.
		Hopefully, in future versions of maya we will be able to use python directly for AETemplates.
	'''
	def __init__(self, nodeType):
		mel =  '''
			global proc AE%sTemplate(string $nodeName)
			{
				python ("import slumMaya\\nslumMaya.AETemplate.template('"+$nodeName+"')");
			}
		''' % nodeType
		meval( mel )
		self.nodeType = nodeType

	@staticmethod
	def _deleteLayoutIfExists(layoutName, type):
		'''
			checks for the existence of a layout with the given layoutName, of type "type"
			and deletes it, if it exists.
			Used to delete the framelayout of our template.
		'''
		parent = m.setParent(query=True)
		children = m.layout( parent, q=True, ca=True, )
		if children!=None:
			for child in children:
				if m.objectTypeUI( child, isType=type ) and child==layoutName:
					m.deleteUI( layoutName, layout=True );

	@staticmethod
	def template(nodeName):
		'''
			This is the method called by the dinamic AETemplate mel.
			Basically, it sets up a scroll layout, adds an extra attributes layout and
			suppress all attributes found in the node.
			The real important piece of code is the callCustom template that calls the
			static method customUI of this class, at runtime.
			Unfortunately, AGAIN we need to rely on a small portion of mel code to trigger the call for
			our customUI method, since a callCustom only calls mel global procs.
		'''
		node = slumMaya.slumNode(nodeName)

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

		attrUICustomHeader = 'attrUICustomHeader_%s' % m.nodeType(nodeName)
		mel =  '''
			global proc %s(string $node)
			{
				python ("import slumMaya\\nslumMaya.AETemplate.customUIHeader('"+$node+"')");
			}
			''' % (attrUICustomHeader)
		meval( mel )

		m.editorTemplate( attrUICustomHeader, attrUICustomHeader, '', callCustom=True )
		m.editorTemplate( beginScrollLayout=True )
		m.editorTemplate( attrUICustom, attrUICustom, '', callCustom=True )

		# add extra controls
		m.editorTemplate( addExtraControls=True )
		m.editorTemplate( endScrollLayout=True )

	@staticmethod
	def customUI(nodeName):
		'''
			This method is called at runtime, and its responsible to create the
			ui for every type of node we have. It calls genericHeader and parameters
			methods to initialize the generic header all slum shaders have, and the
			parameters for each node type, based on the returned data from the parameter
			of a slum class shader.
		'''
		nodeName = nodeName.strip('.')
		slumNode = slumMaya.slumNode(nodeName)

		AETemplate.parameters(slumNode)

	@staticmethod
	def customUIHeader(nodeName):
		'''
			this method creates generic UI that is the same for every slum shader node.
		'''
		nodeName = nodeName.strip('.')
		slumNode = slumMaya.slumNode(nodeName)

		layoutName = "customUIHeaderID_%s" % m.nodeType(slumNode.node)
		updateButtonName = "genericHeaderUpdateButtonID_%s" % m.nodeType(slumNode.node)

		AETemplate._deleteLayoutIfExists( layoutName, 'columnLayout' )
		m.columnLayout( layoutName, manage=True, adjustableColumn=True )

		# begin first line
		# ----------------------------------------------------------------------------
		m.rowLayout( numberOfColumns=1, columnWidth1=800,
					columnAttach1 = 'right',  columnOffset1=0)
		m.iconTextButton( style='iconOnly', w=800, h=40, align='left',
		#m.image( w=800,h=40, enable=True,
				 image = os.path.join(slumMaya.__path__[0],'images','slum4maya.xpm') )
		m.setParent('..')

		m.rowLayout( numberOfColumns=4, adj=4, columnWidth4=(20, 20, 100,1),
					columnAttach4 = ('left','left','left','left'),  columnOffset4=(0,0,0,0))

		#m.text( label = ' ' )

		# if node is updated compared to template source
		light = 'green'
		help = "Green light - node is up-to-date with original slum template. No need to update."
		if slumNode['slum']['edited']:
			light = 'yellow'
			help = "Yellow light - node has being edited inside maya. If you update, you'll lose all edited code. Don't update!"
		elif not slumNode.updated:
			light = 'red'
			help = "Red light - node is NOT up-to-date with original slum template. Click the red light to bring it to the latest version!"
		xpm = [
			os.path.join(slumMaya.__path__[0],'images','%s.xpm' % light),
			os.path.join(slumMaya.__path__[0],'images','%sSelected.xpm' % light),
		]
		# update button
		def updateCode(*args):
			if slumNode['slum']['edited']:
				raise "If you update, you'll loose all the edit in this node."
			m.iconTextButton( updateButtonName, e=True, image=xpm[1] )
			shaderBase.slumInitializer( slumNode.MObject(), refreshNodeOnly=True )
			m.iconTextButton( updateButtonName, e=True, image=xpm[0] )
			m.select(cl=True)
			m.select(slumNode.node)
			slumNode['slum']['edited'] = False
		m.iconTextButton( updateButtonName, style='iconOnly', w=20, h=20, image=xpm[0],  selectionImage=xpm[1], command=updateCode, annotation = help )

		# edit button
		xpmEdit = [
				os.path.join(slumMaya.__path__[0],'images','edit.xpm'),
				os.path.join(slumMaya.__path__[0],'images','editSelected.xpm'),
			]
		def editCode(*args):
			slumNode['slum']['edited'] = True
			m.select(cl=True)
			m.select(slumNode.node)
		m.iconTextButton( style='iconOnly', w=20, h=20, image=xpmEdit[0],  selectionImage=xpmEdit[1], command=editCode, annotation = "Edit slum template code stored in this node. After editing, Update light will become yellow, signing it has being edit inside maya." )


		# add popmenu for the renderer
		menu = m.optionMenuGrp(label='preview', cw2 = (60,80))

		# loop trough slum template supported shaders.
		previewRenderers = []
		for each in slumNode.slum._renderers():
			# check if the slum template have support for the renderer.
			# if so, add it to the listbox
			if each in dir(slumNode.slum):
				m.menuItem( label = each )
				previewRenderers.append(each)


		# we should check the selected renderer here. for now, default to the first one in the list
		m.optionMenuGrp( menu, e=True, value=previewRenderers[0] )
		menuOption = m.optionMenuGrp( menu, q=True, value=True )

		m.setParent('..')
		# ----------------------------------------------------------------------------
		# end first line


		# run swatchUI method of the current selected renderer
		rendererObject = slumMaya.renderers[slumMaya.renderers.index(eval('slumMaya.%s' % menuOption))]
		if hasattr(rendererObject,'swatchUI'):
			rendererObject.swatchUI(slumNode)

		m.setParent('..')



	@staticmethod
	def parameters(slumNode):
		'''
			This is the method that creates the UI for our attributes.
			The UI is based in the data returned from the parameters method of
			the slum class associated with the node.
		'''
		
		# overrides template clientRefresh method to allow callbacks in the template to
		# trigger a UI refresh in Maya
		def refresh():
			AETemplate.customUIHeader(slumNode.node)
		slumNode.slum.clientRefresh = refresh

		# this garantees the layout will be rebuild properly everytime
		# the attribute editor is open/selected for a node.
		layoutName = "layoutID_%s" % m.nodeType(slumNode.node)
		AETemplate._deleteLayoutIfExists( layoutName, 'columnLayout' )
		m.columnLayout( layoutName, visible=True, adjustableColumn=True )

		# a recursive function to create our UI. perfect for hierarquical parameters
		def recursiveAddAttrUI( parameter ):
			if not parameter.hidden:
				if   parameter.__class__.__name__ == 'group' :
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
							keyz = popup.keys()
							keyz.sort()
							defaulValue=keyz[0]
							for each in keyz:
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
	
		recursiveAddAttrUI( slumNode.slum.parameters( ) )


class shaderBase(OpenMayaMPx.MPxNode):
	'''
		This is the base class used by slum shader nodes. Every node is initialized
		based on a class that derivates from this one.
		For surface shaders for example, we use the shaderSurface class, which is derivate from
		this class and MPxHardwareShader.
		For light shaders, we use shaderLight class, which is derivate from this one and MPxLocatorNode
	'''
	slum = None
	
	def __init__(self):
		''' placeholder. not used at the moment '''
		#OpenMayaMPx.MPxNode.__init__(self)
		pass

	def compute(self, plug, dataBlock):
		'''
			this method is called by maya when rendering in software mode or viewport texture mode.
			we need to come up with a way to have a maya software code inside a slum template that can be
			executed here. The way maya software shaders are written is pretty complex, compared to
			rsl and others, so my plan is to create some python classes that would simplify the maya
			software shader development, bringing it more close to rsl...
		'''
		#sys.stderr.write( "\ncompute %s\n" % plug.name() )
		pass

	@staticmethod
	def nodeCreator():
		'''
			plugin creation method (returns the class object). this is needed to register a new node in maya.
		'''
		return OpenMayaMPx.asMPxPtr( shaderBase() )


	@staticmethod
	def nodeInitializer():
		'''
			plugin initializaton method. this is needed to register a new node in maya.
			usually, this method would handle all the initialization of parameters for the node.
			Instead, we initialize the node in another method that is called AFTER the node
			already exists in maya.
			This make the whole process much simple, and if we need to update a node from a new version
			of a slum template, we just call the same method again.
		'''
		pass

	@staticmethod
	def slumInitializer(object, data=None, forceRefresh=False, refreshNodeOnly=False):
		'''
			this is the real initialization function... this is called after the node exists in maya.
			so we can use this to dinamicaly add the shader attributes.
			Also, this same method can be called to update the node if the class code changes.
		'''
		self = OpenMaya.MFnDependencyNode(object)
		node = slumMaya.slumNode(self.name())

		# dinamically source AETemplate for this node
		AETemplate( self.typeName() )

		# add the code to the slum attribute. After this is done, every call to slumNode will automatically
		# evaluate the slumClass
		classCache = slum.collectSlumClasses( refresh=forceRefresh )

		nodeTypeName = self.typeName().replace('slum_','')
		if not refreshNodeOnly:
			# find slumclass name, get the data from classCache and store in the slum key of the node (string parameter)
			node['slum'] = classCache.allClasses[nodeTypeName]
		else:
			path = classCache.allClasses[nodeTypeName]['path']
			node['slum'] = classCache.readSlumFile( path )[nodeTypeName]

		# re-initialize now that the slum key is in place
		node = slumMaya.slumNode(self.name())

		def recursiveAddAttr( parameter ):
			pars={'input':[], 'output':[]}
			if parameter.__class__.__name__ == 'group':
				for each in parameter.value:
					tmp = recursiveAddAttr( each )
					pars['input'].extend( tmp['input'] )
					pars['output'].extend( tmp['output'] )
			elif parameter.__class__.__name__ == 'parameter':
				node[parameter.name] = parameter.value
				node.setInternal( parameter.name, True ) # add set/get callback
				node.setReadable( parameter.name, True )
				node.setStorable( parameter.name, True )
				if not parameter.output:
					node.setWritable( parameter.name, True )
					pars['input'].append(parameter.name)
				else:
					node.setWritable( parameter.name, False )
					pars['output'].append(parameter.name)
			return pars

		# use pars to set attributeAffects !!!!
		pars = recursiveAddAttr( node.slum.parameters() )


		# loop trough registered renderers and call slumInitializer method
		# if the renderer object have it
		for each in slumMaya.renderers:
			if hasattr(each,'slumInitializer'):
				each.slumInitializer(node)

	def setDependentsDirty ( self, plugBeingDirtied, affectedPlugs ):
		sys.stderr.write('...%s...\n' %  plugBeingDirtied.name() )
		#node = slumMaya.slumNode( self.name() )
		return True

	def setInternalValueInContext ( self, plug, dataHandle,  ctx ):
		'''
			callback when user changes parameters in the node.
			Returning false forces maya to set the value of the attribute as it would whitout a callback.
			returning true means that this function set the value and maya dont need to do a thing.
			False is default!
		'''
		# loop trough registered renderers and call setInternalValueInContext
		# method if the renderer object have it
		for each in slumMaya.renderers:
			if hasattr(each,'setInternalValueInContext'):
				each.setInternalValueInContext(
					plug.name().split('.')[1],
					slumMaya.slumNode( self.name() ),
					dataHandle
				)

		return False

	def getInternalValueInContext ( self, plug, dataHandle,  ctx ):
		'''
			callback when reading parameters from the node.
			returning false forces maya to get teh value of the attribute as it would whitout a callback.
			returning true forces maya to avoid getting the value itself, and will return whatever
			this method put inside dataHandle.
			False is default!
		'''
		ret = False
		node = slumMaya.slumNode( self.name() )
		plugName = plug.name().split('.')[1]

		# loop trough registered renderers and call getInternalValueInContext
		# method if the renderer object have it
		for each in slumMaya.renderers:
			if hasattr(each,'getInternalValueInContext'):
				ret = ret or each.getInternalValueInContext(plugName, node, dataHandle)

		return ret

	def renderSwatchImage ( self, image ):
		pass