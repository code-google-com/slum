#
# customGLView.py - a custom GL Viewport that doesnt draw any geometry.
#					Basically its a way	for slum to have a gl canvas
#					in maya UI to draw whatever we want.
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



import sys
import math
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaRender as OpenMayaRender

glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()

kPluginCmdName = "customGLView"

kInitFlag = "-in"
kInitFlagLong = "-init"

kResultsFlag = "-r"
kResultsFlagLong = "-results"

kClearFlag = "-cl"
kClearFlagLong = "-clear"

kToleranceFlag = "-tol"
kToleranceFlagLong = "-tolerance"

class customGLView(OpenMayaMPx.MPx3dModelView):
	def __init__(self):
		OpenMayaMPx.MPx3dModelView.__init__(self)

		self.fOldCamera = OpenMaya.MDagPath()
		self.fCameraList = OpenMaya.MDagPathArray()
		self.fCurrentPass = 0
		self.fDrawManips = True
		self.fOldDisplayStyle = OpenMayaUI.M3dView.kWireFrame
		self.fLightTest = False
		self.fListList = OpenMaya.MDagPathArray()
		self.tol = 10.0

		self.setMultipleDrawEnable(True)

	def multipleDrawPassCount(self):
		return self.fCameraList.length() + 1

	def setCameraList(self, cameraList):
		setMultipleDrawEnable(True)
		self.fCameraList.clear()

		for i in range(cameraList.length()):
			self.fCameraList.append(cameraList[i])

		self.refresh()

	def removeAllCameras(self):
		self.fCameraList.clear()
		self.refresh()

	def getCameraHUDName(self):
		cameraPath = OpenMaya.MDagPath()
		self.getCamera(cameraPath)

		cameraPath.pop()

		hudName = "spNarrowPolyViewer: " + cameraPath.partialPathName()
		return hudName

	def setIsolateSelect(self, list):
		self.setViewSelected(True)
		return self.setObjectsToView(list)

	def setIsolateSelectOff(self):
		return self.setViewSelected(False)

	def preMultipleDraw(self):
		self.fCurrentPass = 0
		self.fDrawManips = False

		self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayEverything, False)

		self.setDrawAdornments(False)
		self.setDisplayHUD(False)
		self.setDisplayAxis(False)
		self.setDisplayAxisAtOrigin(False)
		self.setDisplayCameraAnnotation(False)
		self.setViewSelected(True)

		self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayGrid, True)

		'''

		dagPath = OpenMaya.MDagPath()
		try:
			oldCamera = OpenMaya.MDagPath()
			self.getCamera(oldCamera)

			self.fOldCamera = oldCamera

			#if self.isColorIndexMode():
			#	self.setColorIndexMode(False)

			displayHUD(False)

			sList = OpenMaya.MSelectionList()
			OpenMaya.MGlobal.getActiveSelectionList(sList)

			sList.getDagPath(0, dagPath)
		except:
			# sys.stderr.write("ERROR: spNarrowPolyViewer.preMultipleDraw b\n")
			pass

		try:
			itMeshPolygon = OpenMaya.MItMeshPolygon(dagPath, OpenMaya.cvar.MObject_kNullObj)

			if None == itMeshPolygon:
				return;

			self.beginGL()
			while not itMeshPolygon.isDone():
				points = OpenMaya.MPointArray()
				itMeshPolygon.getPoints(points, OpenMaya.MSpace.kWorld)
				length = points.length()

				if length == 3:
					for i in range(length):
						p = points[i]
						p1 = points[(i+1)%length]
						p2 = points[(i+2)%length]

						v1 = OpenMaya.MVector(p1 - p)
						v2 = OpenMaya.MVector(p2 - p)

						angle = v1.angle(v2) * 180.0 / math.pi

						if math.fabs(angle - self.tol) < 0.0001 or angle < self.tol:
							glFT.glBegin( OpenMayaRender.MGL_POLYGON )
							glFT.glVertex3f(points[0].x, points[0].y, points[0].z)
							glFT.glVertex3f(points[1].x, points[1].y, points[1].z)
							glFT.glVertex3f(points[2].x, points[2].y, points[2].z)

							glFT.glNormal3f(points[0].x, points[0].y, points[0].z)
							glFT.glNormal3f(points[1].x, points[1].y, points[1].z)
							glFT.glNormal3f(points[2].x, points[2].y, points[2].z)

							glFT.glTexCoord3f(points[0].x, points[0].y, points[0].z)
							glFT.glTexCoord3f(points[1].x, points[1].y, points[1].z)
							glFT.glTexCoord3f(points[2].x, points[2].y, points[2].z)
							glFT.glEnd()

				itMeshPolygon.next()
			self.endGL()
		except:
			#sys.stderr.write("ERROR: spNarrowPolyViewer.preMultipleDraw c\n")
			pass
		'''

	def postMultipleDraw(self):
		try:
			#self.setCamera(self.fOldCamera)
			self.fDrawManips = False
			#self.updateViewingParameters()
		except:
			sys.stderr.write("ERROR: spNarrowPolyViewer.postMultipleDraw\n")
			raise

	def preMultipleDrawPass(self, index):
		self.fCurrentPass = index
		'''
		try:
			self.setDrawAdornments(False)
			self.setDisplayHUD(False)
			self.setDisplayAxis(False)
			self.setDisplayAxisAtOrigin(False)
			self.setDisplayCameraAnnotation(False)
			self.setViewSelected(True)

			dagPath = OpenMaya.MDagPath()

			if self.fCurrentPass == 0:
				self.getCamera(dagPath)
			else:
				nCameras = self.fCameraList.length()
				if self.fCurrentPass <= nCameras:
					dagPath = self.fCameraList[self.fCurrentPass-1]
				else:
					sys.stderr.write("ERROR: ...too many passes specified\n")
					return

			self.setCameraInDraw(dagPath)

			self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayEverything, False)

			if dagPath == self.fOldCamera:
				self.fDrawManips = False
				self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayGrid, True)

				self.setFogEnabled(False)

				self.setBackgroundFogEnabled(False)

				self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayLights, False)
				self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayCameras, False)
				self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayIkHandles, False)
				self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayDimensions, False)
				self.setObjectDisplay(OpenMayaUI.M3dView.kDisplaySelectHandles, False)

				textPos = OpenMaya.MPoint(0.0, 0.0, 0.0)
				str = "Main View"
				self.drawText(str, textPos, OpenMayaUI.M3dView.kLeft)
			else:
				self.fDrawManips = False
				self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayGrid, True)

				self.setFogEnabled(False)

				self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayLights, False)
				self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayCameras, False)
				self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayIkHandles, False)
				self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayDimensions, False)
				self.setObjectDisplay(OpenMayaUI.M3dView.kDisplaySelectHandles, False)
		except:
			sys.stderr.write("ERROR: spNarrowPolyViewer.preMultipleDrawPass\n")
			raise

		# note do not have light test in here

		# self.setLightingMode(OpenMayaUI.kLightDefault)

		if ((self.fCurrentPass % 2) == 0):
			self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayNurbsSurfaces, True );
			self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayNurbsCurves, True );

		#self.updateViewingParameters()
		'''

	def postMultipleDrawPass(self, index):
		self.setObjectDisplay(OpenMayaUI.M3dView.kDisplayEverything, False)

	def okForMultipleDraw(self, dagPath):
		if not self.fDrawManips and dagPath.hasFn(OpenMaya.MFn.kManipulator3D):
			return False
		return True

	def multipleDrawPassCount(self):
		return self.fCameraList.length() + 1

	def viewType(self):
		return kPluginCmdName;




class customGLViewCmd(OpenMayaMPx.MPxModelEditorCommand):
	def __init__(self):
		OpenMayaMPx.MPxModelEditorCommand.__init__(self)
		self.fCameraList = OpenMaya.MDagPathArray()

	def appendSyntax(self):
		try:
			theSyntax = self._syntax()
			theSyntax.addFlag(kInitFlag, kInitFlagLong)
			theSyntax.addFlag(kResultsFlag, kResultsFlagLong)
			theSyntax.addFlag(kClearFlag, kClearFlagLong)
			theSyntax.addFlag(kToleranceFlag, kToleranceFlagLong, OpenMaya.MSyntax.kDouble)

		except:
			sys.stderr.write( "ERROR: creating syntax for model editor command: %s" % kPluginCmdName )

	def doEditFlags(self):
		try:
			user3dModelView = self.modelView()

			if user3dModelView.viewType() == kPluginCmdName:
				argData = self._parser()

				if argData.isFlagSet(kInitFlag):
					self.initTests(user3dModelView)
				elif argData.isFlagSet(kResultsFlag):
					self.testResults(user3dModelView)
				elif argData.isFlagSet(kClearFlag):
					self.clearResults(user3dModelView)
				elif argData.isFlagSet(kToleranceFlag):
					tol = argData.flagArgumentDouble(kToleranceFlag, 0)
					user3dModelView.tol = tol
					user3dModelView.refresh(True, True)
				else:
					return OpenMaya.kUnknownParameter
		except:
			sys.stderr.write( "ERROR: in doEditFlags for model editor command: %s" % kPluginCmdName )

	def initTests(self, view):
		clearResults(self, view)

		# Add every camera into the scene.  Don't change the main camera,
		# it is OK that it gets reused.
		#
		cameraPath = OpenMaya.MDagPath()
		dagIterator = OpenMaya.MItDag(OpenMaya.MItDag.kDepthFirst, OpenMaya.MFn.kCamera)

		while not dagIterator.isDone():
			try:
				dagIterator.getPath(cameraPath)
				camera = OpenMaya.MFnCamera(cameraPath)
			except:
				continue

			OpenMaya.MGlobal.displayInfo(camera.fullPathName())
			self.fCameraList.append(cameraPath)

			dagIterator.next()

		try:
			view.setCameraList(self.fCameraList)
		except:
			OpenMaya.MGlobal.displayError("Could not set list of cameras\n")
			raise

		view.refresh()

	def testResults(self, view):
		print "fCameraLIst.length() = %d " % (self.fCameraList.length(), )
		length = self.fCameraList.length()

	def clearResults(self, view):
		view.removeAllCameras()
		self.fCameraList.clear()



def cmdCreator():
	return OpenMayaMPx.asMPxPtr( customGLViewCmd() )

def viewerCreator():
	return OpenMayaMPx.asMPxPtr( customGLView() )

# initialize the script plug-in
def initializePlugin(mpluginObj):
    mplugin = OpenMayaMPx.MFnPlugin(mpluginObj)
    mplugin.registerModelEditorCommand( kPluginCmdName, cmdCreator, viewerCreator)


# uninitialize the script plug-in
def uninitializePlugin(mpluginObj):
    mplugin = OpenMayaMPx.MFnPlugin(mpluginObj)
    mplugin.deregisterModelEditorCommand( kPluginCmdName )
    

def test(customCamera=False):
	import maya
	import slumMaya


	window	= maya.cmds.window()
	form 	= maya.cmds.formLayout()
	editor	= maya.cmds.customGLView()

	maya.cmds.formLayout(form,edit=True,attachForm=(editor, "top", 		0))
	maya.cmds.formLayout(form,edit=True,attachForm=(editor, "bottom", 	0))
	maya.cmds.formLayout(form,edit=True,attachForm=(editor, "right", 	0))
	maya.cmds.formLayout(form,edit=True,attachForm=(editor, "left", 	0))

	if customCamera:
		camera = maya.cmds.camera(centerOfInterest=2.450351, position=(1.535314,1.135712,1.535314), rotation=(-27.612504,45,0), worldUp=(-0.1290301,0.3488592,-0.1290301))
		maya.cmds.customGLView(editor,edit=True,camera=camera[0])
		maya.cmds.currentTime(10.0,edit=True)
		maya.cmds.customGLView(editor,edit=True,i=True)
		maya.cmds.refresh()
		maya.cmds.customGLView(editor,edit=True,r=True)

	maya.cmds.showWindow(window)
