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
from shaderBase import *

try:
	mayaBaseClass = OpenMayaMPx.MPxHardwareShader
except:
	mayaBaseClass = OpenMayaMPx.MPxNode

class shaderSurface( shaderBase, mayaBaseClass ):
	def __init__(self):
		shaderBase.__init__(self)
		mayaBaseClass.__init__(self)
	@staticmethod
	def nodeCreator():
		return OpenMayaMPx.asMPxPtr( shaderSurface() )

	def render(self, geo):
		pass
		return True

	def renderSwatchImage ( self, image ):
		w=0
		h=0
		image.getSize( w, h );

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
