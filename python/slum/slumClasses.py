#
# slumClasses - shader base classes for slumTemplates
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



class slum:
	@staticmethod
	def type():
		return None
	def ID(self):
		return None
	def __init__(self):
		pass
	def upload(self):
		''' upload template to online repository '''
		pass
	def parameters(self):
		''' return parameters to be exposed in the client '''
		pass
	def icon(self):
		''' return string with MPX icon '''
		return ''

	# renderers code (returns tupple where 0-parameters and 1-code)
	def delight(self, parameters):
		''' returns the shader parameters and code of the delight renderer '''
		return ('','')
	def renderman(self, parameters):
		''' returns the shader parameters and code of the renderman renderer '''
		return ('','')
	def air(self, parameters):
		''' returns the shader parameters and code of the air renderer '''
		return ('','')
	def cgfx(self, parameters):
		''' returns the shader parameters and code of the cgfx renderer '''
		return ('','')
	def glsl(self, parameters):
		''' returns the shader parameters and code of the glsl renderer '''
		return ('','')

	# support methods - theses methods are basically to support clients.
	# they are not suposed to be replaced in a .slum file (not virtual)
	def _renderers(self):
		''' returns supported renderers. This is used by clients so they can add support on UI for then
			basically, the names here reflect the same names of the methods for each renderer.
			so, if you add a new renderer, you must make sure to add the method with the same name for it.
			also, the support for this new renderer need to be added in the client.'''
		return [
			'delight',
			'renderman',
			'air',
			'cgfx',
			'glsl',
		]
	def _dictParameters(self):
		def recursivePopulateDict( parameter ):
			temp = {}
			if parameter.__class__.__name__ == 'group':
				for each in parameter.value:
					temp.update( recursivePopulateDict( each ) )
			elif parameter.__class__.__name__ == 'parameter':
				temp[parameter.name] = parameter
			return temp

		return recursivePopulateDict( self.parameters() )



class slumSurface(slum):
	@staticmethod
	def type():
		return 'surface'

class slumVolume(slum):
	@staticmethod
	def type():
		return 'volume'

class slumDisplacement(slum):
	@staticmethod
	def type():
		return 'displacement'

class slumLight(slum):
	@staticmethod
	def type():
		return 'light'

class slumColor(slum):
	@staticmethod
	def type():
		return 'color'

class slumFloat(slum):
	@staticmethod
	def type():
		return 'float'
