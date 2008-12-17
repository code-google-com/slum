#
# shaderSurface - 	the class that defines a slum surface shader node in Maya.
#					based on shaderBase and mayas hardware shader node.
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
import shaderBase

try:
	mayaBaseClass = OpenMayaMPx.MPxHardwareShader
	#mayaBaseClass = OpenMayaMPx.MPxHwShaderNode 
except:
	mayaBaseClass = OpenMayaMPx.MPxNode

class shaderSurface( mayaBaseClass  ):
#class shaderSurface( shaderBase.shaderBase, mayaBaseClass ):
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
	def slumInitializer():
		'''
			plugin initializaton method. this is needed to register a new node in maya.
			usually, this method would handle all the initialization of parameters for the node.
			Instead, we initialize the node in another method that is called AFTER the node
			already exists in maya.
			This make the whole process much simple, and if we need to update a node from a new version
			of a slum template, we just call the same method again.
		'''
		pass
	def __init__(self):
		##OpenMayaMPx.MPxNode.__init__(self)
		mayaBaseClass.__init__(self)
		#shaderBase.shaderBase.__init__(self)
		pass
	@staticmethod
	def nodeCreator():
		x =shaderSurface()
		return OpenMayaMPx.asMPxPtr( x )

	def render(self, geo):
		pass
		return True
	def bind(  MDrawRequest, M3dView ):
		pass
	def unbind(  MDrawRequest, M3dView ):
		pass
	def geometry( MDrawRequest, M3dView, prim, writable, indexCount, indexArray,
					vertexCount, vertexIDs, vertexArray, normalCount, normalArrays,
					colorCount, colorArrays, texCoordCount, texCoordArrays ):
		pass



	def renderSwatchImage ( self, image ):
		w=0
		h=0
		image.getSize( w, h );
		print '---->',w,h
		
		swatch = OpenMaya.MImage();
		if swatch.readFromFile ( '/tmp/xx.tif' ):
			swatch.resize (w, h, false);
			image.setPixels(swatch.pixels(),w,h);
		else:
			swatch.create(w,h,3)
			pixels = swatch.pixels()
			count = 0
			for y in range(h):
				for x in range(w):
					pixels[y*w+x] = count
					count += 1
					if count>255:
						count=0
			image.setPixels(swatch.pixels(),w,h);

		dlimage.release();

		return True
