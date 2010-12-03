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
    def __init__(self, value, name, help='No Help available', max=1, min=0, output=False, input=False, primvar=False, ui=None, callback=None, hidden=False):
        self.name	= name
        self.help	= help
        self.max	= max
        self.min	= min
        self.ui 	= ui
        self.output	= output
        self.primvar	= primvar
        self.value  	= value
        self.callback 	= callback
        self.hidden 	= hidden

#    def __repr__(self):
#        ret=['%s( ' % str(self.__class__)]
#        for each in dir(self):
#            try:
#                if each[0] != '_':
#                    v = eval("self.%s" % each)
#                    if type(v)==type(''):
#                        v = '"%s"' % v
#                    else:
#                        v = str(v)
#                    ret.append( "%s = %s," % ( str(each), v ) )
#            except:
#                pass
#        ret.append(')')
#        return ''.join(ret)

class group:
    def __init__(self, value, name, help='No Help available', opened=True, hidden=False):
        self.name   = name
        self.help   = help
        self.opened = opened
        self.value  = value
        self.hidden = hidden
        #self.children = self.__getAllUI( self.value )
#        self.keys = self.children.keys

#    def __repr__(self):
#         return '%s(%s)' % (self.__class__, self.children)

#    def __getitem__(self, key):
#        return self.children[key]

#    def __setitem__(self, key, value):
#        self.children[key].value = value

#    def __getAllUI(self, uiList=[], children={}):
#        for pars in uiList:
#            if 'group' in pars.__class__.__name__:
#                children.update( self.__getAllUI( pars.value, children) )
#            else:
#                children[pars.name] = pars
#        return children



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
    class file( uiBase ):
        def __init__(self, filetypes=[], defaultFolder=None, hidden=False):
            uiBase.__init__(self, hidden)
            self.filetypes = filetypes
            self.defaultFolder = defaultFolder
    class button( uiBase ):
        def __init__(self,callback, name='', hidden=False):
            uiBase.__init__(self, hidden)
            self.name		= name
            self.callback	= callback
