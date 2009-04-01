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

import maya.OpenMayaMPx as OpenMayaMPx
import slumMaya

pluginName = "slum"
PluginNodeId = 0xC0000
searchPath = ['SLUM_SEARCH_PATH', 'MAYA_SCRIPT_PATH', 'PYTHONPATH']

def initializePlugin(mobject):
	global nodeFactory
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	nodeFactory = slumMaya.nodeFactory(
		mplugin,
		pluginName,
		PluginNodeId,
		searchPath
	)
	nodeFactory.register()

	slumMaya.customGLView.initialize(mplugin)

def uninitializePlugin(mobject):
	global nodeFactory
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	nodeFactory.unregister()

	slumMaya.customGLView.uninitialize(mplugin)
