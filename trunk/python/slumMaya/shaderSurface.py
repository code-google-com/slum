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
	#mayaBaseClass = OpenMayaMPx.MPxHardwareShader
	mayaBaseClass = OpenMayaMPx.MPxHwShaderNode
except:
	mayaBaseClass = OpenMayaMPx.MPxNode

#class shaderSurface( mayaBaseClass  ):
class shaderSurface( mayaBaseClass, shaderBase.shaderBase ):
    def __init__(self):
        ##OpenMayaMPx.MPxNode.__init__(self)
        mayaBaseClass.__init__(self)
        shaderBase.shaderBase.__init__(self)

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( shaderSurface() )

    def render(self, geo):
        pass
        return True
    def bind(  self, MDrawRequest, M3dView ):
        pass
    def unbind(  self, MDrawRequest, M3dView ):
        pass
    
    def geometry( self, MDrawRequest, M3dView, prim, writable, indexCount, indexArray,
                    vertexCount, vertexIDs, vertexArray, normalCount, normalArrays,
                    colorCount, colorArrays, texCoordCount, texCoordArrays ):
                    
        print MDrawRequest, M3dView, prim, writable, indexCount, indexArray, vertexCount, vertexIDs, vertexArray, normalCount, normalArrays,colorCount, colorArrays, texCoordCount, texCoordArrays

        import maya.OpenMayaRender as omr

        glRenderer = omr.MHardwareRenderer.theRenderer()
        gl = glRenderer.glFunctionTable()

        if prim != omr.MGL_TRIANGLES and prim != omr.MGL_TRIANGLE_STRIP:
            return False

        gl.glPushAttrib ( omr.MGL_ENABLE_BIT )
        gl.glDisable ( omr.MGL_LIGHTING )
        gl.glDisable ( omr.MGL_TEXTURE_1D )
        gl.glDisable ( omr.MGL_TEXTURE_2D )
        # Setup cube map generation

        gl.glEnable ( omr.MGL_TEXTURE_CUBE_MAP_ARB )
        #gl.glBindTexture ( omr.MGL_TEXTURE_CUBE_MAP_ARB, phong_map_id )
        gl.glEnable ( omr.MGL_TEXTURE_GEN_S )
        gl.glEnable ( omr.MGL_TEXTURE_GEN_T )
        gl.glEnable ( omr.MGL_TEXTURE_GEN_R )
        gl.glTexGeni ( omr.MGL_S, omr.MGL_TEXTURE_GEN_MODE, omr.MGL_NORMAL_MAP_ARB )
        gl.glTexGeni ( omr.MGL_T, omr.MGL_TEXTURE_GEN_MODE, omr.MGL_NORMAL_MAP_ARB )
        gl.glTexGeni ( omr.MGL_R, omr.MGL_TEXTURE_GEN_MODE, omr.MGL_NORMAL_MAP_ARB )
        gl.glTexParameteri(omr.MGL_TEXTURE_CUBE_MAP_ARB, omr.MGL_TEXTURE_WRAP_S, omr.MGL_CLAMP)
        gl.glTexParameteri(omr.MGL_TEXTURE_CUBE_MAP_ARB, omr.MGL_TEXTURE_WRAP_T, omr.MGL_CLAMP)
        gl.glTexParameteri(omr.MGL_TEXTURE_CUBE_MAP_ARB, omr.MGL_TEXTURE_MAG_FILTER, omr.MGL_LINEAR)
        gl.glTexParameteri(omr.MGL_TEXTURE_CUBE_MAP_ARB, omr.MGL_TEXTURE_MIN_FILTER, omr.MGL_LINEAR)
        gl.glTexEnvi ( omr.MGL_TEXTURE_ENV, omr.MGL_TEXTURE_ENV_MODE, omr.MGL_REPLACE )
        # Could modify the texture matrix here to do light tracking...

        gl.glMatrixMode ( omr.MGL_TEXTURE )
        gl.glPushMatrix ()
        gl.glLoadIdentity ()
        gl.glMatrixMode ( omr.MGL_MODELVIEW )

        # Draw the surface.
        gl.glPushClientAttrib ( omr.MGL_CLIENT_VERTEX_ARRAY_BIT )
        gl.glEnableClientState( omr.MGL_VERTEX_ARRAY )
        gl.glVertexPointer ( 3, omr.MGL_FLOAT, 0, vertexArray )
        #gl.glEnableClientState( omr.MGL_NORMAL_ARRAY )
        #gl.glNormalPointer ( omr.MGL_FLOAT, 0, normalArrays )
        gl.glDrawElements ( prim, indexCount, omr.MGL_UNSIGNED_INT, indexArray )
        
        # The client attribute is already being popped. You
        gl.glPopClientAttrib()
        gl.glMatrixMode ( omr.MGL_TEXTURE )
        gl.glPopMatrix ()
        gl.glMatrixMode ( omr.MGL_MODELVIEW )
        gl.glDisable ( omr.MGL_TEXTURE_CUBE_MAP_ARB )
        gl.glDisable ( omr.MGL_TEXTURE_GEN_S )
        gl.glDisable ( omr.MGL_TEXTURE_GEN_T )
        gl.glDisable ( omr.MGL_TEXTURE_GEN_R )
        gl.glPopAttrib()

        return True




    def renderSwatchImage ( self, image ):
        w=0
        h=0
        #print dir(image)
        image.getSize( w, h )
        print '---->',w,h
        '''
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
        '''
        return True
