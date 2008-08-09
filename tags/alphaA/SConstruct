
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

	installDir = 'slumInstall'

	env = Environment()
	env.Execute( Mkdir(installDir) )

	install = []
	for each in recursiveFiles('python'):
		install.append(
			env.Install(os.path.join(installDir, 'python', os.path.dirname(each.replace('python'+os.sep,''))), each)
		)

	for each in recursiveFiles('shader'):
		install.append(
			env.Install(os.path.join(installDir, 'shader', os.path.dirname(each.replace('shader'+os.sep,''))), each)
		)

	install.append( env.Install(installDir, 'README') )

	env.Alias( 'install', install)