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


import os, glob


defaultSearchPath = 'SLUM_SEARCH_PATH'
defaultOnlineRepositorie = 'http://slum.hradec.com/repositorie'

def evalSlumClass(code, classeName):
	'''
		execute "code" string, and returns the class object for "classeName"
	'''
	exec 'from slum import *' in globals()
	exec code in globals()
	return eval('%s()' % classeName)

class collectSlumClasses:
	'''
		class responsible for deal with slum files and classes
		initializing a new class object will trigger the search of *.slum files in the local search path and online repositories.
		a cache system is in place to avoid un-necessary re-caching by clients.
		clients dont need to care about it. just re-create the class and the new object will pick up the data from the cache
		automatically, unless refresh parameter is True.
	'''
	def __init__(self, refresh=None, searchPath = None, onlineRepositories = None):
		'''
			gathers slum classes from local disk/network and online repositories

			this class stores the gathered classes and search paths as global variables, so
			if the class is re-created, it will retain the data from a previous object. (a sort of cache)

			this is very useful when using this class in clients, so a call for the class in a initialization context
			will store the data, and the data can be quickly retrieve later in a diferent context, even whitout the original
			search paths.

			also, a call to _refresh method (or creating the class object using the refresh parameter = True)
			will refresh the class caches using the cached search paths. This way,
			the search paths only need to be defined in the initialization context. As the class caches are global, even
			the _refresh method can be called from a totally separated context.

			This cache mechanism frees the client from the tedious and error prone tasks of store all this data so it can
			be accessed in diferent contexts. It also speeds up the whole proccess, avoiding multiple un-necessary
			disk/network accesses.
		'''
		global searchPathCache
		global onlineRepositoriesCache

		# it paths specified, update caches
		if searchPath:
			searchPathCache	= searchPath
		else:
			searchPathCache	= defaultSearchPath

		if onlineRepositories:
			onlineRepositoriesCache = onlineRepositories
		else:
			onlineRepositoriesCache = defaultOnlineRepositorie

		# store in the class for later use by methods
		self.searchPath 		= searchPathCache
		self.onlineRepositories	= onlineRepositoriesCache

		# makes sure searchpaths are lists
		if type(self.searchPath) == str:
			self.searchPath = [self.searchPath]
		if type(self.onlineRepositories) == str:
			self.onlineRepositories = [self.onlineRepositories]

		#cache classes if refresh is set or caches are empty
		global localClasses
		global onlineClasses
		try: # check if variables are defined or not
			localClasses
			onlineClasses
			if refresh:
				raise
		except:
			localClasses, onlineClasses = self._refresh()

		# store then separeted for now...
		self.localClasses  	= localClasses
		self.onlineClasses 	= onlineClasses

		# combine then
		self.allClasses = self.localClasses
		self.allClasses.update( self.onlineClasses )

	def _refresh(self):
		print 'slum: local caching...'
		localClasses = self.local()
		print 'slum: online caching'
		onlineClasses = self.online()
		print 'slum: all done.'
		return ( localClasses, onlineClasses )

	def _registerSlumFile(self, slumCode):
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
		registry = None
		newClasses = None
		exec 'from slum import *' in locals()
		registry = dir()
		exec '\n'.join(slumCode) in locals()
		newClasses = dir()

		# compare current dir() with old one and get the new ones
		# loop trough all defined classes inside the current slum file
		# and register then in a dict, if no other with the same name is already registered.
		slumClasses={}
		for classe in filter(lambda x: x not in registry, newClasses):
			print 'slum:	found %s' % filter(lambda x: 'class %s' % classe in ' '.join(x.split()), slumCode)[0].strip().strip(':')
			if not slumClasses.has_key(classe):
				slumClasses[classe] = {}
				slumClasses[classe]['code'] = ''.join(slumCode)
				# we also store the class name so it can be retrieve later in the client,
				# even if the data is stored in a diferent format than a dict.
				slumClasses[classe]['name'] = classe
		return slumClasses


	def online(self):
		'''
			same as local, but for online repositories.
			returns data in the same format as local
		'''
		return {}

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
						slumClasses.update( self._registerSlumFile( open(each).readlines() ) )

		return slumClasses