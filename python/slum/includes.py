#
# includes.py - adds .hslum extension to python import mechanism, allowing
# 				templates to just use import to import .hslum includes
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

import sys,  marshal
VER = sys.hexversion

debug = 0

class DBmodule(type(sys)):
    def __repr__(self):
        return "<DBmodule '%s' originally from '%s'>" % (self.__name__, self.__file__)



class hslumImporter(object):

    def __init__(self, item, *args, **kw):
        print 'init',item, args, kw
        '''
        if item != "*db*":
            raise ImportError
        if debug:
            print "dbimporter: item:", id(self), item, "args:", args, "keywords:", kw
            print "Accepted", item
        '''

    def find_module(self, fullname, path=None):
        print 'find_module',fullname, path
        '''
        if debug:
            print "%x: find_module: %s from %s" % (id(self), fullname, path)
        if fullname not in impdict:
            if debug:
                print "Bailed on", fullname
            return None
        else:
            if debug:
                print "found", fullname, "in db"
            return self
        '''

    def load_module(self, modname):
        print 'load_module'
        if debug:
            print "%x: load_module: %s" % (id(self), modname)

        # return it if already loaded
        if modname in sys.modules:
            return sys.modules[modname]

        # load it
        if False:
            raise ImportError, "DB module %s not found in modules"

        code, package, path = ("","","")
        code = marshal.loads(code)
        module = DBmodule(modname)
        sys.modules[modname] = module
        module.__name__ = modname
        module.__file__ = path # was "db:%s" % modname
        module.__loader__ = self
        if package:
            module.__path__ = ["*db*"]
        exec code in module.__dict__
        if debug:
            print modname, "loaded:", module, "pkg:", package

        return module


def install():
    sys.path_hooks.append(hslumImporter)
    sys.path_importer_cache.clear() # probably not necessary
    sys.path.insert(0, "*db*") # probably not needed with a metea-path hook?


