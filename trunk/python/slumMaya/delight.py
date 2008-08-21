
import slumMaya
import slum
import maya.cmds as m
from maya.mel import eval as meval


class delight:
	'''
		this class defines all the static methods that shaderBase calls to correct implement
		the 3delight support in slum nodes.
		this class need to be registered in slumMaya.renderers, so shaderBase can know about it.
		to register a new renderer class, just do :
			slumMaya.renderers.append(class name)
	'''
	@staticmethod
	def slumInitializer(node):
		'''
			This method is called by shaderBase when initializing parameters for a slum node.
			slum is implemented in 3delight for maya as a rsl code node.
			shadingParameters and shadingCode are the attributes that 3dfm looks for in an rsl code node.
			we also set the attributes as "setInternal=True", which triggers maya to call our
			getInternalValueInContext method everytime someone tries to read this parameters.
			So, the only thing we do is hook some code into getInternalValueInContext to gather
			parameters and code from the slum class and return to maya, dynamically.
		'''
		node['shadingParameters'] = ""
		node.setHidden('shadingParameters', True)
		node.setInternal('shadingParameters', True)

		node['shadingCode'] = ""
		node.setHidden('shadingCode', True)
		node.setInternal('shadingCode', True)

	@staticmethod
	def setInternalValueInContext(plugName, node, dataHandle):
		'''
			This method is called by shaderBase when setting parameters of a slum node.
			you can use this to automatically call the swatch method to render a swatch
			when an attribute is changed.
		'''
		ret = False
		delight.swatch(node)
		return ret

	@staticmethod
	def getInternalValueInContext(plugName, node, dataHandle):
		'''
			This method is called by shaderBase when querying parameters of a slum node.
			slum is implemented in 3delight for maya as renderman shader code nodes. It
			have a shadingParameters and shadingCode attributes that 3delight for maya
			will query to get the rsl shader parameters and code for a shader.
			This method grabs the parameters and code from the slum class and return to
			3delight for maya dinamically.
		'''
		ret = False
		dlParameters = ['shadingParameters', 'shadingCode']
		if plugName in dlParameters:
			delightShader = node.slum.delight( node )
			zcode = delightShader[ dlParameters.index(plugName) ]
			# ====================================================================================================
			# hack to allow slum to work with 3delight 7.0.0 version
			# must remove after new public is available
			if plugName == 'shadingParameters':
				zcode = []
				for line in delightShader[ dlParameters.index(plugName) ]:
					zcode.append(line.split('=')[0]) # just use text before the '=' character, if any
			# ====================================================================================================
			code = '\n'.join( zcode ).replace('\t',' ')
			dataHandle.setString( code )
			ret = True
		return ret

	@staticmethod
	def _translateShader(node, compile=True):
		delete	= []
		type 	= 'surface'
		sdl 	= '/tmp/%s_preview' % node
		nodeSG 	= m.listConnections( node, t='shadingEngine' )
		if nodeSG:
			shadingGroup = nodeSG[0]
		else:
			shadingGroup = m.createNode('shadingEngine', name='%s_slumPreview' % node, ss=True)
			m.connectAttr( '%s.outColor' % node, '%s.surfaceShader' % shadingGroup,  f=True)
			delete.append(shadingGroup)

		if compile:
			m.delightNodeWatch( f=True )
			try:
				meval( 'buildShader("%s", {"%s"}, "%s", "","%s","%s", 1)' % (
					os.path.basename(sdl),
					shadingGroup,
					type,
					os.path.dirname(sdl),
					os.path.dirname(sdl)
				))
			except:
				m.confirmDialog( title='slum', message='Error compiling shader %s.\nCheck script editor for more details.' % shadingGroup )
		else:
			sdl=meval( 'DL_translateMayaToSl("%s", {"%s"}, "%s")' % (
				os.path.basename(sdl),
				shadingGroup,
				type
			))

		m.delightNodeWatch( f=True )
		for each in delete:
			m.delete(each)
		return sdl

	@staticmethod
	def swatchUI(node):
		'''
			this method is called by slum node AETemplate to display a swatch images.
			it should contain all the code to display swatch images inside slum node
			AETemplate. Whith this method, its very easy to create diferent types of swatch
			preview layouts, depending on the renderer.
		'''
		m.scrollLayout(h=135)
		m.gridLayout(cellWidthHeight=(128,128), nr=1)

		for each in range(3):
			m.image(w=128,h=128, enable=True, i='/tmp/xx.tif')

		m.setParent('..')
		m.setParent('..')

	@staticmethod
	def swatch(node):
		'''
			this method is called by slum node AETemplate to render a swatch image.
			everytime an attribute is changed, shaderBase class will call this method
			to render a new swatch for the node.
		'''

		pass



slumMaya.renderers.append(delight)
