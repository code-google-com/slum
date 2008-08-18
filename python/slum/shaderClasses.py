#
# shaderClasses.py - shader base classes for slumTemplates
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
	''' This is the base shader class. Usually, its not used directly when developing shaders.
	this class have all the methods that a shader can define, including renderers shader code methods
	and specific client methods.'''
	@staticmethod
	def type():
		''' slum shader type. This method is overriden by other classes to define the slum class type '''
		return None
	def ID(self):
		''' slum shader template ID. Every shader must have an unique ID. '''
		return None
	def __init__(self):
		''' placeholder. No use for this method yet '''
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
		'''returns a tupple where: 0 = 3delight shader parameters and 1 = 3delight shader code'''
		return ('','')
	def renderman(self, parameters):
		'''returns a tupple where: 0 = renderman shader parameters and 1 = renderman shader code'''
		return ('','')
	def air(self, parameters):
		'''returns a tupple where: 0 =  air shader parameters and 1 =  air shader code'''
		return ('','')
	def cgfx(self, parameters):
		'''returns a tupple where: 0 = cgfx shader parameters and 1 = cgfx shader code'''
		return ('','')
	def glsl(self, parameters):
		'''returns a tupple where: 0 = glsl shader parameters and 1 = glsl shader code'''
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
	''' this class is used in a slum template when defining surface shaders.
	this class is basically a normal slum class, with the override of the type method.
	This classes are being defined here to make a slum template easier to read, with just the
	methods that are really needed on it.'''
	@staticmethod
	def type():
		return 'surface'

class slumVolume(slum):
	''' this class is used in a slum template when defining volume shaders '''
	@staticmethod
	def type():
		return 'volume'

class slumDisplacement(slum):
	''' this class is used in a slum template when defining displacement shaders '''
	@staticmethod
	def type():
		return 'displacement'

class slumLight(slum):
	''' this class is used in a slum template when defining light shaders '''
	@staticmethod
	def type():
		return 'light'

class slumColor(slum):
	''' this class is used in a slum template when defining color utility shaders '''
	@staticmethod
	def type():
		return 'color'

class slumFloat(slum):
	''' this class is used in a slum template when defining float utility shaders '''
	@staticmethod
	def type():
		return 'float'
