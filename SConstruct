import os, glob, sys

version = 'slumAlphaH'

def recursiveFiles(path):
	files=[]
	for each in glob.glob(os.path.join(path,'*')):
		if os.path.isfile(each):
			files.append(each)
		elif os.path.isdir(each):
			files.extend(recursiveFiles(each))
		else:
			pass
	return files

def rmDir(path, mask=''):
	files=[]
	if os.path.isfile(path):
		if mask in path:
			try: os.remove(path)
			except: pass
	elif os.path.isdir(path):
		for each in glob.glob(os.path.join(path,'*')):
			rmDir(each,mask)
		try: os.rmdir(path)
		except: pass
	else:
		pass
	return files

installDir = version
#for each in glob.glob('./*.zip'):
#		print each
#		rmDir("%s.zip" % each)
#rmDir(installDir)
rmDir("python", mask='.pyc')

env = Environment()
if  'release' not in sys.argv and 'doc' not in sys.argv and	'ftp' not in sys.argv and '-c' not in sys.argv:
		print '''

	you must specify what you want scons to do. (add -c to clean folder)

		release - builds a release package
		doc	- builds all documentation
		ftp - ftp's the generated documentation to ftp


		'''
else:


	# release - make a package release
	for each in recursiveFiles('python'):
		env.Alias( 'release',
			env.Install(os.path.join(installDir, 'python', os.path.dirname(each.replace('python'+os.sep,''))), each)
		)

	for each in recursiveFiles('shader'):
		env.Alias( 'release',
			env.Install(os.path.join(installDir, 'shader', os.path.dirname(each.replace('shader'+os.sep,''))), each)
		)

	env.Alias( 'release', env.Install(installDir, 'README.txt') )
	zip = env.Command( "%s.zip" % installDir, installDir, "zip -r $TARGET $SOURCE" )
	env.Alias( 'release', zip )
	
	# windows installer
	nsisCompiler = os.path.join(os.environ['PROGRAMFILES(X86)'], 'NSIS', 'makensis.exe')
	if os.path.exists(nsisCompiler):
		os.system("cat installer/windows.nsi | sed 's/@SLUM@/%s/g' > windows.nsi" % version)
		os.system("cat installer/license.txt | sed 's/@SLUM@/%s/g' > license.txt" % version)
		wininstall = env.Command( "%s.exe" % installDir, zip, '"%s" windows.nsi' % nsisCompiler )
		env.Alias( 'release', wininstall  )
		env.Clean( wininstall, 'license.txt' )
		env.Clean( wininstall, 'windows.nsi' )
		env.Clean( zip, "%s.exe" % installDir )

	env.Clean( zip, 'tmp' )
	env.Clean( zip, 'doc' )
	env.Clean( zip, installDir )
	env.Clean( zip, "%s.zip" % installDir )

	# generate docs
	html = env.Command( "docsHtml", "python", 'epydoc -q -o doc --html %s' % os.path.join('$SOURCE','*') )
	pdf  = env.Command( "docsPdf", 	"python", 'epydoc -q -o doc --pdf  %s' % os.path.join('$SOURCE','*') )
	env.Alias( 'doc', html )
	env.Alias( 'doc', pdf  )

	# ftp docs
	if not os.system('syncFTP.py > .tmp'):
		ftp  = env.Command( "ftp", 		"python", 'mkdir -p doc ; cd doc ; ~/tools/scripts/syncFTP.py /htdocs/slum/doc' )
		env.Alias( 'ftp', ftp  )
