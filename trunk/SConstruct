import os, glob, sys

version = 'slumAlphaK'

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

env = Environment(PATH=os.environ['PATH'])
if  'test' not in sys.argv and 'release' not in sys.argv and 'doc' not in sys.argv and	'ftp' not in sys.argv and '-c' not in sys.argv:
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

	env.Alias( 'release',
			#env.Install(installDir, 'README.txt')
			env.Command(
				os.path.join(installDir,"README.txt"),
				"README.txt",
				'cat $SOURCE | sed "s/@SLUM@/%s/g" > $TARGET' % version
			)
		)
	zip = env.Command( "%s.zip" % installDir, installDir, "zip -r $TARGET $SOURCE" )
	env.Alias( 'release', zip )

	# windows installer
	znis = {}
	try:
		znis['darwin'] = os.popen('which nsis 2>/dev/null').readlines()[0].strip()
	except: pass
	if os.environ.has_key('PROGRAMFILES(X86)'):
		znis['cygwin'] = os.path.join(os.environ['PROGRAMFILES(X86)'], 'NSIS', 'makensis.exe')

	wininstall = None
	if sys.platform in znis.keys():
		nsisCompiler = znis[sys.platform]
		if os.path.exists(nsisCompiler):
			os.system("cat installers/windows.nsi | sed 's/@SLUM@/%s/g' > windows.nsi" % version)
			os.system("cat installers/license.txt | sed 's/@SLUM@/%s/g' > license.txt" % version)
			wininstall = env.Command( "%s_Windows.exe" % installDir, zip, '"%s" windows.nsi' % nsisCompiler )
			env.Alias( 'release', wininstall  )
			env.Clean( wininstall, 'license.txt' )
			env.Clean( wininstall, 'windows.nsi' )
			env.Clean( zip, "%s.exe" % installDir )

	env.Clean( zip, 'tmp' )
	env.Clean( zip, 'doc' )
	env.Clean( zip, installDir )
	env.Clean( zip, "%s.zip" % installDir )

	# upload Release
	# zip package
	env.Alias('release',
		env.Command(
			"%s.released" % zip[0],
			zip[0],
			"../../devtools/uploadRelease $SOURCE slum 'multiplatform package' 'Featured,Type-Package,OpSys-All' && touch $TARGET"
		)
	)
	# windows installer
	env.Alias('release',
		env.Command(
			"%s.released" % wininstall[0],
			wininstall[0],
			"../../devtools/uploadRelease $SOURCE slum 'windows installer' 'Featured,Type-Installer,OpSys-Windows' && touch $TARGET"
		)
	)

	# send release email to discussion group



	# generate docs
	#html = env.Command( "docsHtml", "python", 'echo $PATH:/usr/bin/env epydoc' )
	html = env.Command( "docsHtml", "python", 'bash -i -l -c "epydoc -q -o doc --html %s"' % os.path.join('$SOURCE','*') )
	pdf  = env.Command( "docsPdf", 	"python", 'bash -i -l -c "epydoc -q -o doc --pdf  %s"' % os.path.join('$SOURCE','*') )
	env.Alias( 'doc', html )
	env.Alias( 'doc', pdf  )

	# ftp docs
	if not os.system('syncFTP.py > .tmp'):
		ftp  = env.Command( "ftp", 		html, 'mkdir -p doc ; cd doc ; ~/tools/scripts/syncFTP.py /htdocs/slum/doc' )
		env.Alias( 'ftp', ftp  )


	# testing
	testSlumImport = env.Command(
		".test",
		"python/slum/__init__.py",
		'export PYTHONPATH=./python ; export SLUM_SEARCH_PATH=./shader ; echo "import slum" | python -'
	)
	env.Alias( 'test', testSlumImport )
