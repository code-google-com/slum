#
# delight - 	delight renderer class tha defines how slum will interact with 3delight
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

import os
import slumMaya
import slum
import maya.cmds as m
from maya.mel import eval as meval
from maya.utils import executeInMainThreadWithResult


class delight:
    '''
            this class defines all the static methods that shaderBase calls to correct implement
            the 3delight support in slum nodes.
            this class need to be registered in slumMaya.renderers, so shaderBase can know about it.
            to register a new renderer class, just do :
                    slumMaya.renderers.append(class name)
    '''
    def __init__(self, node):
            '''
                    initialize the delight class to be used in idle events, for example,
                    to render swatch using the _renderPreview method.
            '''
            self.node = node
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
            node.setStorable('shadingParameters', False) # fixes crashing when saving

            node['shadingCode'] = ""
            node.setHidden('shadingCode', True)
            node.setInternal('shadingCode', True)
            node.setStorable('shadingCode', False) # fixes crashing when saving

    @staticmethod
    def setInternalValueInContext(plugName, node, dataHandle):
            '''
                    This method is called by shaderBase when setting parameters of a slum node.
                    you can use this to automatically call the swatch method to render a swatch
                    when an attribute is changed.
            '''
            ret = False
            #renderSwatch = delight(node)
            #maya.cmds.scriptJob( runOnce=True, idleEvent=renderSwatch._renderPreview)
            #def dd():
            #	print 'xxx'
            #maya.cmds.scriptJob( runOnce=True, idleEvent=dd)
            return ret

    @staticmethod
    def getInternalValueInContext(plug, dataHandle):
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
            name, plugName = plug.name().split('.')
            if plugName in dlParameters:
                    node = slumMaya.slumNode( name )
                    delightShader = node.slum.delight( node )
                    zcode = delightShader[ dlParameters.index(plugName) ]

                    # generate rsl code for ui parameters
                    # defined in parameters() method of the slum class
                    # and assign the values fro the node to then.
                    if dlParameters.index(plugName)==0:
                        pars = node.slum.dictParameters
                        for each in pars.keys():
                            line = ''
                            if pars[each].primvar:
                                line += 'shader_input varying'
                            if pars[each].output:
                                if 'shader_input' in line:
                                    line = line.split('input')[0]
                                line += 'output varying'

                            value = node[each] #pars[each].value
                            t = pars[each].value.__class__.__name__
                            if t in ['int', 'float']:
                                line = '%s float %s = %s;' % ( line, each, str(value) )
                            elif t == ['str']:
                                line = '%s string %s = %s;' % ( line, each, value )
                            else:
                                line = '%s %s %s = %s;' % ( line, t, each, str(value).replace('slum.datatypes.','') )
                            zcode.append(line)


                    code = '\n'.join( zcode ).replace('\t',' ')
                    dataHandle.setString( code )
                    ret = True
            return ret

    @staticmethod
    def swatchUI(node):
            '''
                    this method is called by slum node AETemplate to display a swatch images.
                    it should contain all the code to display swatch images inside slum node
                    AETemplate. Whith this method, its very easy to create diferent types of swatch
                    preview layouts, depending on the renderer.
            '''
            '''
            m.scrollLayout(h=150)
            m.gridLayout(cellWidthHeight=(128,150), nr=1)

            for each in range(3):
                    m.image(w=128,h=128, enable=True, i='/tmp/xx.tif')

            m.setParent('..')
            m.setParent('..')
            '''
            m.rowLayout( numberOfColumns=3, adj=3, columnWidth3=((400-128)/2,128,1) )
            m.text( label = ' ' )
            m.image( delight._imageControlName(node), w=120,h=128, enable=True,
                            image = os.path.join(slumMaya.__path__[0],'images','previewImage.tif') )
            m.setParent('..')
            m.image( delight._imageControlName(node), e=True, w=128)

    @staticmethod
    def _imageControlName(node):
            return "__delightPreviewImageID_%s" % node.node

    def _translateShader(self, compile=True):
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
                    meval( 'buildShader("%s", {"%s"}, "%s", "","%s","%s", 1)' % (
                            os.path.basename(sdl),
                            shadingGroup,
                            type,
                            os.path.dirname(sdl),
                            os.path.dirname(sdl)
                    ))
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

    def _renderPreview(self):
            '''
                    this method is called by slum node AETemplate to render a swatch image.
                    everytime an attribute is changed, shaderBase class will call this method
                    to render a new swatch for the node.
            '''
            sdl = self._translateShader()

            m.RiBegin(of=outputRib)
            meval('RiOption -id false  	 -n "rib" -p "format" "string" "ascii" ')
            meval('RiOption -n "render"  -p "bucketorder" "string" "spiral"  ' )
            meval('RiOption -n "limits"  -p "bucketsize" "integer[2]" "16 16" ' )

            m.RiPixelSamples( s=(3, 3) )
            m.RiShadingRate( s=shadingRate )
            m.RiDisplay( n = imagefile, t = display, m = "rgb")
            m.RiFormat( r=resolution, pa=1 )
            m.RiProjection( p=45 )
            m.RiTranslate( 0, 0, 4)

            m.RiWorldBegin()

            m.RiTransformBegin()
            m.RiArchiveRecord( m = "verbatim", t = "Translate 4 4 -4\n" )
            meval('RiLightSource -n "pointlight" -p "intensity" "float" "1" ;' )
            m.RiTransformEnd()

            m.RiTransformBegin()
            m.RiArchiveRecord( m = "verbatim", t = "Translate -4 4 -4\n" )
            meval('RiLightSource -n "pointlight" -p "intensity" "float" "0.5" ;' )
            m.RiTransformEnd()

            m.RiTransformBegin()
            m.RiArchiveRecord( m = "verbatim", t = "Translate 0 -4 -4\n" )
            meval('RiLightSource -n "pointlight" -p "intensity" "float" "0.25" ;' )
            m.RiTransformEnd()

            # turn raytrace on
            meval('RiAttribute -n "visibility" -p "trace" "integer" 1 -p "photon" "integer" 1 -p "transmission" "string " "opaque" ;')

            if type == 'surface':
                    m.RiSurface( n = sdl+'.sdl' )
            elif type == 'displacement':
                    meval('RiAttribute -n "displacementbound" -p "sphere" "float" 2 -p "coordinatesystem" "string" "shader";')
                    m.RiDisplacement( n = sdl+'.sdl' )
                    m.RiSurface( n = "plastic" )

            m.RiArchiveRecord( m = "verbatim", t = eval(model) )

            m.RiArchiveRecord( m = "verbatim", t = "Translate 0 0 0 \n" )
            m.RiArchiveRecord( m = "verbatim", t = groundRIB )

            m.RiWorldEnd()
            m.RiEnd()



slumMaya.renderers.append(delight)
