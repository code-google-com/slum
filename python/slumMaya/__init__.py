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


searchPath = ['SLUM_SEARCH_PATH', 'MAYA_SCRIPT_PATH', 'PYTHONPATH', '____DYNAMIC_SLUM_SEARCH_PATH']

from nodeFactory import *
from shaderBase import *
from classNode import *
from slumNode import *
#import customGLView

renderers=[]
from delight import *

def updateCode( nodeName = None ):
    '''
        Update the code in all slum node shaders in the current maya scene.
        It first checks if a node needs to be updated and only does
        for the ones who need!
    '''
    import slumMaya, os
    import maya.cmds as m
    if not nodeName:
        nodeName = filter(lambda x: 'slum' in x.lower(), m.listNodeTypes('shader'))
    if type(nodeName) != type([]):
        nodeName = [nodeName]
    for each in nodeName:
        for n in m.ls(type=each):
            slumNode = slumMaya.slumMaya.slumNode(n)
            if not slumNode.updated():
                print 'code updated in node: %s' % n
                slumMaya.shaderBase.slumInitializer( slumNode.MObject(), refreshNodeOnly=True )
                slumNode['slum']['edited'] = False

