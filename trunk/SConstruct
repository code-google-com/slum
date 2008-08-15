import os, glob, sys

version = 'slumAlphaD'

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
			os.remove(path)
	elif os.path.isdir(path):
		for each in glob.glob(os.path.join(path,'*')):
			rmDir(each,mask)
		try: os.rmdir(path)
		except: pass
	else:
		pass
	return files

installDir = version

rmDir(installDir)
for each in glob.glob('*.zip'):
	rmDir("%s.zip" % each)
rmDir("python", mask='.pyc')

env = Environment()

if  0: #'release' not in sys.argv and 'doc' not in sys.argv and	'ftp' not in sys.argv and '-c' not in sys.argv:
		print '''

	you must specify what you want scons to do.

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

	env.Alias( 'release', env.Install(installDir, 'README') )
	zip = env.Command( "%s.zip" % installDir, installDir, "zip -r $TARGET $SOURCE" )
	env.Alias( 'release', zip )

	env.Clean( zip, 'tmp' )
	env.Clean( zip, installDir )
	env.Clean( zip, 'doc' )

	# generate docs
	html = env.Command( "docsHtml", "python", 'epydoc -q -o doc --html %s' % os.path.join('$SOURCE','*') )
	pdf  = env.Command( "docsPdf", 	"python", 'epydoc -q -o doc --pdf  %s' % os.path.join('$SOURCE','*') )
	ftp  = env.Command( "ftp", 		"python", 'cd doc;python ~/tools/scripts/syncFTP2.py /htdocs/slum/doc' )

	env.Alias( 'doc', html )
	env.Alias( 'doc', pdf  )
	env.Alias( 'ftp', ftp  )
