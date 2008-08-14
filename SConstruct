
try:
	import builds
	_builds=False
except:
	_builds=False

import os, glob




if _builds:
	# maya python module
	scripts = builds.mayaPythonPlugin(
				ARGUMENTS,
				version='0.0.1',
				mayaVersion='2008',
				src=builds.globRecursive('python/*'),
			)

	scripts.finalize()

else:
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

	def rmDir(path):
		files=[]
		if os.path.isfile(path):
			os.remove(path)
		elif os.path.isdir(path):
			for each in glob.glob(os.path.join(path,'*')):
				rmDir(each)
			os.rmdir(path)
		else:
			pass
		return files

	installDir = 'slumInstall'

	rmDir(installDir)
	rmDir("%s.zip" % installDir)

	env = Environment()

	install = []

	install.append(	env.Execute( Mkdir(installDir) ) )

	for each in recursiveFiles('python'):
		install.append(
			env.Install(os.path.join(installDir, 'python', os.path.dirname(each.replace('python'+os.sep,''))), each)
		)

	for each in recursiveFiles('shader'):
		install.append(
			env.Install(os.path.join(installDir, 'shader', os.path.dirname(each.replace('shader'+os.sep,''))), each)
		)

	install.append( env.Install(installDir, 'README') )

	install.append( env.Command( "%s.zip" % installDir, installDir, "zip -r $TARGET $SOURCE" ) )
	install.append( env.Command( "doc/slumDevDoc.pdf", "python", "epydoc -o /tmp $SOURCE/* ; cp /tmp/api.pdf $TARGET" ) )

	env.Alias( 'install', install)