#
# shaderLight - 	the class that defines a slum light shader node in Maya.
#					based on shaderBase and mayas locator node.
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
import maya.OpenMayaRender as OpenMayaRender
import maya.cmds as m
from maya.mel import eval as meval
from shaderBase import *

gl = OpenMayaRender.MHardwareRenderer.theRenderer().glFunctionTable()

class shaderNetwork:
	def __init__(self, nodePlug, resolution=(320,200)):
		self.resolution = resolution
		self.w = resolution[0]
		self.h = resolution[1]
		self.node = nodePlug
		self.refresh = True
		self.texture = None

	def free(self):
		if self.texture:
			gl.glDeleteTextures( 1, self.texture );
		self.refresh=True;

	def needRefresh(self):
		return self.refresh

	def sample(self):
		uCoords 	= OpenMaya.MFloatArray()
		vCoords 	= OpenMaya.MFloatArray()
		filterSizes	= OpenMaya.MFloatArray()
		points		= OpenMaya.MFloatPointArray()
		refPoints	= OpenMaya.MFloatPointArray()
		normals		= OpenMaya.MFloatVectorArray()
		tanUs		= OpenMaya.MFloatVectorArray()
		tanVs		= OpenMaya.MFloatVectorArray()
		colors		= OpenMaya.MFloatVectorArray()
		transps		= OpenMaya.MFloatVectorArray()

		# current camera
		cameraPath  = OpenMaya.M3dView.active3dView().getCamera( )
		cameraMat 	= cameraPath.inclusiveMatrix().matrix

		numSamples=0;
		for x in range(self.w):
			for y in range(self.h):
				uCoords.append( x/float(self.w) )
				vCoords.append( y/float(self.h) )
				numSamples += 1

		# sample network and bake
		OpenMayaRender.MRenderUtil.sampleShadingNetwork(
			node,
			numSamples,
			false, #shadow
			false, #reuse maps
			cameraMat,
			points,
			uCoords,
			vCoords,
			normals,
			refPoints,
			tanUs,
			tanVs,
			filterSizes,
			colors,
			transps
		);

		data = []
		if colors.length()>0:
			numSamples=0
			for x in range(self.w):
				for y in range(self.h):
						data[numSamples*3+0] = colors[numSamples].x * 255
						data[numSamples*3+1] = colors[numSamples].y * 255
						data[numSamples*3+2] = colors[numSamples].z * 255
						numSamples += 1
		return data

	def bind(self):
		if self.refresh:
			self.texture = gl.glGenTextures( 1 )
			gl.glBindTexture( gl.GL_TEXTURE_2D, self.texture )

			gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR )
			gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR )

			gl.glTexImage2D(
				gl.GL_TEXTURE_2D,
				0,
				gl.GL_RGB,
				self.w, self.h,
				0,
				gl.GL_RGB,
				gl.GL_UNSIGNED_BYTE,
				self.sample()
			)
			self.refresh = False

		if self.texture:
			gl.glBindTexture( gl.GL_TEXTURE_2D, self.texture )



class shaderLight( shaderBase, OpenMayaMPx.MPxLocatorNode ):
	def __init__(self):
		shaderBase.__init__(self)
		OpenMayaMPx.MPxLocatorNode.__init__(self)
	@staticmethod
	def nodeCreator():
		return OpenMayaMPx.asMPxPtr( shaderLight() )
