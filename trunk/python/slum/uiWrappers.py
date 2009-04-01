#
# uiWrappers.py - classes to define slum template parameters and UI formating
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

class parameter:
	def __init__(self, value, name, help='No Help available', max=1, min=0, output=False, ui=None, callback=None, hidden=False):
		self.name	 	= name
		self.help	 	= help
		self.max	 	= max
		self.min	 	= min
		self.ui 		= ui
		self.output		= output
		self.value  	= value
		self.callback 	= callback
		self.hidden 	= hidden

class group:
	def __init__(self, value, name, help='No Help available', opened=True, hidden=False):
		self.name 	= name
		self.help 	= help
		self.opened = opened
		self.value  = value
		self.hidden = hidden

class uiBase:
	def __init__(self, hidden=False ):
		self.hidden = hidden

class ui:
	class  popup( uiBase ):
		def __init__(self, values = {'yes':True, 'no':False}, hidden=False ):
			uiBase.__init__(self, hidden)
			self.values = values
	class checkbox( uiBase ):
		def __init__(self, hidden=False):
			uiBase.__init__(self, hidden)
			pass
	class button( uiBase ):
		def __init__(self,callback, name='', hidden=False):
			uiBase.__init__(self, hidden)
			self.name		= name
			self.callback	= callback
