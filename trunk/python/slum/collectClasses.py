#
# collectClasses.py - 	collect classes defined inside .slum files and return as
# 						a dictionary
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


import os, glob, traceback, sys, copy
import md5 as __md5
from  safeEval import safe_eval


from shaderClasses import *

class __templates:
    def __getitem__(self, key):
        return eval( 'self.%s' % key )

templates = __templates()

# initialization methods
def refresh():
    '''
            high level function
            force a refresh of all templates from disk/online
    '''
    init(refresh=True)

def init(refresh=False):
    '''
        high level function
        loads all templates from disk/online
    '''
    classes = collectSlumClasses()
    if refresh:
        classes.refresh(force=refresh)
    allTemplates = classes.allClasses
    cmd = []
    for each in allTemplates.keys():
        cmd.append( "templates.%s = __template('%s', allTemplates)" % (each, each) )
    exec( ';'.join(cmd) )


# internal methods.
def __template(name, classes=None):
    '''
        high level function
        returns a class obj for the givem template name.
        The returned object will be the class defined in the template, properly evaluated for runtime/syntax errors.
    '''
    if not classes:
        classes = collectSlumClasses().allClasses
    if not _test(classes[name]):
        return None
    c = evalSlumClass(classes[name]['code'], name)
    c.name = name
    c.md5 = classes[name]['md5']
    c.path = classes[name]['path']
    return c

def _test(classe):
    '''
        low level class (shouldn't be directly used - refer to high level functions/classes)
        test methods in a template for runtime/syntax errors.

        todo: 	only delight() method being test. Need to implement a
                        loop that tests all methods in the given class.
    '''
    ret = True
    c = evalSlumClass(classe['code'], classe['name'])
    #for each in c._renderers():
    try:
        tmp=c.delight(c._dictParameters(value=True))
    except:
        sys.stderr.write( "Runtime error in %s delight method.\n%s" % (classe['path'], traceback.format_exc()) )
        ret = False
    return ret


def _readSlumFile(path):
    '''
        low level class (shouldn't be directly used - refer to high level functions/classes)
        reads a template from a file and returns it as a list (one line per record)
    '''
    slumCode = open(path).readlines()
    # fix txt if writen in windows
    for n in range(len(slumCode)):
        slumCode[n] = slumCode[n].replace('\r','')
    return slumCode


# a low level method to evaluate a new template from a code string
def evalSlumClass(code, classeName):
    '''
        low level class (shouldn't be directly used - refer to high level functions/classes)
        execute "code" string, and returns the class object for "classeName"
    '''

    ret = None
    newCode  = 'import traceback\n'
    newCode += 'from slum import *\n'
    #newCode += 'from slum.shaderClasses import *\n'
    #newCode += 'from slum.uiWrappers import *\n'
    #newCode += 'from slum.datatypes import *\n'
    newCode += 'try:\n\t'
    newCode += code.replace('\n','\n\t')
    newCode += '\nexcept:\n'
    newCode += '\traise Exception("Syntax error in slum template: \\n%s" % traceback.format_exc() )\n\n'
    newCode += 'temp = %s()\n' % classeName
    newCode += 'temp._dictParameters(value=True)'
    #print newCode
    #print 'bummmm', classeName
    env = {}
    try:
        exec newCode in env
    except:
        tmp = classeName
#        lineNumber = 1
#        for each in newCode.split('\n'):
#            tmp += "%4d: %s\n" % (lineNumber, each)
#            lineNumber  += 1
        sys.stderr.write(  "Error in slum class '%s':\n%s\n%s%s\n" % (tmp, '='*80, traceback.format_exc(), '='*80) )
    #print 'bummmm2'
    if env.has_key('temp'):
        ret = copy.copy(env['temp'])

        #ret = safe_eval('%s()' % classeName, fail_on_error = True)

    return ret

# md5 help methods
def getMD5(code):
    '''
        low level class (shouldn't be directly used - refer to high level functions/classes)
        calculates md5 for the given code
    '''
    return __md5.md5( code ).digest()

def checkMD5(md5data, name):
    '''
        low level class (shouldn't be directly used - refer to high level functions/classes)
        check if the md5 matchs the md5 of the source file.
    '''
    classes = collectSlumClasses().allClasses
    return md5data == getMD5( ''.join( _readSlumFile(classes[name]['path']) ) )


# the class that looks for all templates
class collectSlumClasses:
    '''
        low level class (shouldn't be directly used - refer to high level functions/classes)
        class responsible for deal with slum files and classes
        initializing a new class object will trigger the search of *.slum files in the local search path and online repositories.
        a cache system is in place to avoid un-necessary re-caching by clients.
        clients dont need to care about it. just re-create the class and the new object will pick up the data from the cache
        automatically, unless refresh parameter is True.
    '''
    def __init__(self, searchPath = None, onlineRepositories = None):
        '''
            gathers slum classes from local disk/network and online repositories

            this class stores the gathered classes and search paths as global variables, so
            if the class is re-created, it will retain the data from a previous object. (a sort of cache)

            this is very useful when using this class in clients, so a call for the class in a initialization context
            will store the data, and the data can be quickly retrieve later in a diferent context, even whitout the original
            search paths.

            also, a call to refresh method
            will refresh the class caches using the cached search paths. This way,
            the search paths only need to be defined in the initialization context. As the class caches are global, even
            the refresh method can be called from a totally separated context.

            This cache mechanism frees the client from the tedious and error prone tasks of store all this data so it can
            be accessed in diferent contexts. It also speeds up the whole proccess, avoiding multiple un-necessary
            disk/network accesses.
        '''

        searchPathCache	= ['SLUM_SEARCH_PATH']
        onlineRepositoriesCache = ['http://slum.hradec.com/repository']

        if os.environ.has_key('___SLUM_GLOBAL_ONLINE_SEARCH_PATH'):
            onlineRepositoriesCache = eval( os.environ['___SLUM_GLOBAL_ONLINE_SEARCH_PATH'] )

        if os.environ.has_key('___SLUM_GLOBAL_SEARCH_PATH'):
            searchPathCache = eval( os.environ['___SLUM_GLOBAL_SEARCH_PATH'] )

        # it paths specified, update caches
        if searchPath:
                searchPathCache	= searchPath
                os.environ['___SLUM_GLOBAL_SEARCH_PATH'] = str(searchPathCache)

        if onlineRepositories:
                onlineRepositoriesCache = onlineRepositories
                os.environ['___SLUM_GLOBAL_ONLINE_SEARCH_PATH'] = str(onlineRepositoriesCache)

        # store in the class for later use by methods
        self.searchPath         = searchPathCache
        self.onlineRepositories	= onlineRepositoriesCache

        # makes sure searchpaths are lists
        if type(self.searchPath) == str:
                self.searchPath = [self.searchPath]
        if type(self.onlineRepositories) == str:
                self.onlineRepositories = [self.onlineRepositories]

        self.refresh()

    def clearCache(self):
        '''cache classes if global caches are empty or if forced to recache.'''
        global localClasses
        global onlineClasses
        try:
            del localClasses
            del onlineClasses
        except:
            pass

    def refresh(self, force=False):
        '''cache classes if global caches are empty or if forced to recache.'''
        global localClasses
        global onlineClasses

        try: # check if variables are defined or not
            firstInit = False
            localClasses
            onlineClasses
            if force or (not localClasses and not onlineClasses):
                    raise
        except:
            firstInit = True

        localClasses, onlineClasses = self.__refresh(firstInit)

        # store then separeted for now...
        self.localClasses  	= localClasses
        self.onlineClasses 	= onlineClasses

        # combine then
        self.allClasses = self.localClasses
        self.allClasses.update( self.onlineClasses )

    def __refresh(self, firstInit=False):
            ''' main refresh code, called from self.refresh()'''
            global localClasses
            global onlineClasses

            def p(m):
                if firstInit:
                    sys.stdout.write(m)

            def printClasses(classes):
                idz = []
                countIDz = {}
                for classe in classes.keys():
                    id = classes[classe]['ID']
                    idz.append('slum:	found ID %4d Class %s' % ( id,classe))
                    if not countIDz.has_key(id):
                        countIDz[id] = []
                    countIDz[id].append(classe)

                idz.sort()
                clash = None
                for each in idz:
                    id = int( each.split('ID ')[1].split(' C')[0] )
                    p( each )
                    if len(countIDz[id])>1:
                        p( "%s> ERROR: ID Clashing - %s\n" % ( "="*(50-len(each)), str(countIDz[id]) ) )
                        clash = True
                    else:
                        p('\n')

                if clash:
                    global localClasses
                    global onlineClasses
                    localClasses = None
                    onlineClasses = None
                    raise Exception("\n\nClash of templates in slum initialization. Fix it!")

            p( 'slum: local caching...\n' )
            localClasses = self.local()
            printClasses(localClasses)
            p( 'slum: online caching\n' )
            onlineClasses = self.online()
            printClasses(onlineClasses )
            p( 'slum: all done.\n' )
            return ( localClasses, onlineClasses )

    def _registerSlumFile(self, slumCode, path):
            '''
                    based on a string with slum code on it, registers all class names in it into a temp db
                    for each name, it adds a "code" key with the source code, so later a client
                    can execute it and retrieve the class object at runtime.

                    this class is a support class for local and online methods!
            '''


            # keep dir() to compare with new dir() after
            # code execution to find the new classes
            # defined inside slum file

            # execute code
            env = {}
            registry = None
            newClasses = None
            exec 'from slum import *' in env
            exec 'from slum.shaderClasses import *' in env
            exec 'from slum.uiWrappers import *' in env
            exec 'from slum.datatypes import *' in env

            registry = env.copy()
            exec '\n'.join(slumCode) in env
            newClasses = env
            #print filter(lambda x: x not in registry.keys(), newClasses.keys()), env

            # compare current dir() with old one and get the new ones
            # loop trough all defined classes inside the current slum file
            # and register then in a dict, if no other with the same name is already registered.
            slumClasses={}
            idz = []
            for classe in filter(lambda x: x not in registry, newClasses):
                    #print 'slum:	found %s' % filter(lambda x: 'class %s' % classe in ' '.join(x.split()), slumCode)[0].strip().strip(':')
                    if not slumClasses.has_key(classe):
                            slumClasses[classe] = {}
                            slumClasses[classe]['code'] = ''.join(slumCode)
                            # we also store the class name so it can be retrieve later in the client,
                            # even if the data is stored in a diferent format than a dict.
                            slumClasses[classe]['name'] = classe
                            slumClasses[classe]['md5']  = getMD5( slumClasses[classe]['code'] )
                            slumClasses[classe]['path'] = path
                            slumClasses[classe]['ID'] 	= evalSlumClass(slumClasses[classe]['code'], classe).ID()

                            # execute code to catch potential runtime errors so clients don't have to
                            if not _test(slumClasses[classe]):
                                    del slumClasses[classe]


            return slumClasses


    def online(self):
            '''
                    same as local, but for online repositories.
                    returns data in the same format as local
            '''
            return {}

    def readSlumFile(self, path):
            return self._registerSlumFile( _readSlumFile(path), path )

    def local(self):
            '''
                    returns a dictionary with all classes found in the searchpath
                    the dictionary is organized as:

                            { 'class name' :
                                    {'code' : 'code for the class'}
                            }
            '''
            # loop trough searchpath an look for all *.slum files
            slumClasses={}
            for searchPath in self.searchPath:
                    if os.environ.has_key(searchPath):
                            env = os.environ[searchPath]
                            for path in env.split(os.path.pathsep):
                                    for each in glob.glob( os.path.join( path, '*.slum' ) ):
                                            slumClasses.update( self.readSlumFile(each) )


            return slumClasses

