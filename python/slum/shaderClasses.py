#
# shaderClasses.py - shader base classes for slumTemplates
#
#    Copyright (C) 2008-2009 - Roberto Hradec
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

import sys, traceback

class slum:
    '''This is the base shader class. (not used directly to develop shaders)
    This class have all the support methods that that a template needs.
    Also have all the client support methods.

    renderer code is define as a method, as in the following example:

            def delight(self, parameters):
                    return ('','')

    The method must have the name of one of the renderers defined in
    the _renderers method.

    The method will be called by the clients, which will pass
    the "parameters" attribute to it.

    The parameters attribute is a dictionary that contains all the
    parameters returned by the parameters method, but already evaluated
    by the client. This way the method can evaluate the parameters input
    from the user to build up the shader parameters and code.

    The method should return a tupple, where [0] is the shader
    parameters and [1] is the shader code.
    '''

    @staticmethod
    def ID(self):
            ''' slum shader template ID. This method MUST be overriden when developing a shader template. Every shader must have an unique ID. '''
            return None
    def parameters(self):
            ''' return parameters to be exposed in the client. This method MUST be overriden when developing a shader template. '''
            pass
    def icon(self):
            ''' return string with MPX icon. This can be overriden in the template to define a custom icon. '''
            return ''
    def type():
            ''' slum shader type. This method is overriden by other classes to define the slum class type '''
            return None
    def __init__(self):
            '''
            # execute virtual self.parameters() here just once and cache in self.__pars.
            # replaces self.parameters() by a simple function which returns self.__pars.
              this way we only execute parameters ONCE everytime the class obj is initialized.
            # creates a plain dictionary of the parameters found in self.parameters() method
              for easy access by clients.
            '''
            self.client = 'python'
            self.platform = sys.platform

            # execute virtual self.parameters() here just once and cache it
            # also replaces self.parameters() by a simple function which returns the cache.
            self.__pars = {}
            try:
                self.__pars = self.parameters()
            except:
                tmp = self.__class__.__name__
                raise Exception( "Runtime error in %s.parameters() method:\n%s\n%s%s\n" % (tmp, '='*80, traceback.format_exc(), '='*80) )

            # replace self.parameters by this simple method who returns the cached output of parameters
            # this way we only execute parameters ONCE everytime the class obj is initialized.
            self.originalParameters = self.parameters
            def __cachedParameters():
                return self.__pars
            #self.parameters = __cachedParameters

            # creates a plain dictionary of the parameters found in self.parameters() method
            # for easy access by clients.
            self.dictParameters = self.__dictParameters(value=False)
            self.dictParametersWithValue = self.__dictParameters(value=True)


    def clientRefresh(self):
            ''' placeholder. Clients will override this at runtime to allow template to refresh client UI '''
            pass
    def getClientClass(self):
            ''' returns a client '''
            return None
    def upload(self):
            ''' upload template to online repository. It will be called by the client when the user wants to submit a template to the online repository.'''
            pass


    # support methods - theses methods are basically to support clients.
    # they are not suposed to be replaced in a .slum file (not virtual)
    def _renderers(self):
            ''' Returns supported renderers. This is used by clients so they can add support on UI for then.
                    Basically, the names here reflect the same names of the methods for each renderer.
                    so, if you add a new renderer, you must make sure to add the method with the same name for it.
                    also, the support for this new renderer need to be added in the clients.'''
            return [
                    'delight',
                    'renderman',
                    'air',
                    'cgfx',
                    'glsl',
            ]
    def __dictParameters(self, value=False):
            def recursivePopulateDict( parameter ):
                    temp = {}
                    if parameter.__class__.__name__ == 'group':
                            for each in parameter.value:
                                    temp.update( recursivePopulateDict( each ) )
                    elif parameter.__class__.__name__ == 'parameter':
                            if value:
                                    temp[parameter.name] = parameter.value
                            else:
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
