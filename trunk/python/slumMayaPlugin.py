#
# slumMayaPlugin - 	the plugin loader. Maya calls the initializePlugin and
#					unitializePlugin in this file everytime the plugin
#					is laoded/unloaded
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

import os, sys
import maya.cmds as m
import maya.OpenMayaMPx as OpenMayaMPx
import slumMaya

pluginName = "slum"
PluginNodeId = 0xC0000


global ____nodeFactory

def initializePlugin(mobject):
    global ____nodeFactory
    
    os.environ['____DYNAMIC_SLUM_SEARCH_PATH'] = "%sslum" % m.workspace(rd=1,q=1)
    ____nodeFactory = slumMaya.nodeFactory(
        mobject, 
        pluginName,
        PluginNodeId,
        slumMaya.searchPath
    )
    ____nodeFactory.register()
 
    # scriptjob this function everytime a file is open to warn the user
    # that the workspace is different from before and slum needs to 
    # refresh its nodes to account for templates located in
    # the project "slum" folder.
    def initSlum():
        global ____nodeFactory
        if '%sslum' % m.workspace(rd=1,q=1) != os.environ['____DYNAMIC_SLUM_SEARCH_PATH'] :
            sceneName = m.file(q=1,sn=1)
            if sceneName:
                msg  = [
                    'WARNING:\nWorkspace changed and slumMaya needs to be refresh to look for project specific slum templates.\n',
                    'Hit "Yes" to allow it to refresh (scene "%s" will be reloaded automatically)' % os.path.basename(sceneName),
                    'or "No" if you fell a refresh is not necessary.',
                    "\nIt's stronly recomended that you hit \"Yes\" to fix any eventual missing slum node in the current scene!!\n",
                ]
                result = m.confirmDialog( title='SLUM MAYA PLUGIN WARNING', message='\n'.join(msg), button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            else:
                result = "Yes"

            if result == "Yes":
                m.file( f=1, new=1 )
                m.unloadPlugin( 'slumMayaPlugin.py' )
                os.environ['____DYNAMIC_SLUM_SEARCH_PATH'] = '%sslum' % m.workspace(rd=1,q=1)
                m.loadPlugin( 'slumMayaPlugin.py' )
                def initSlumFinish():
                    if sceneName:
                        m.file( sceneName, f=1, o=1 )
                    print "Slum Maya Plugin refreshed templates suscessfully.",
                m.scriptJob( idleEvent = initSlumFinish, runOnce=True )
                
    m.scriptJob( e = ["PreFileNewOrOpened",initSlum] )
        
    #slumMaya.customGLView.initialize(mplugin)
 
def uninitializePlugin(mobject):
    global ____nodeFactory
    
    try:
        ____nodeFactory.unregister()
        del ____nodeFactory
    except: 
        pass

    # cleanup all slum scriptJobs, if any, in an idleEvent so if 
    # this has being called by one, it will only delete it after it has
    # finish.
    jobsToKill = filter(lambda x: 'Slum' in x,  m.scriptJob( lj=1 ))
    def killJobs():
        for each in jobsToKill:
            m.scriptJob( kill = int(each.split(':')[0]) )
    m.scriptJob( idleEvent = killJobs, runOnce=True )

    #slumMaya.customGLView.uninitialize(mplugin)
