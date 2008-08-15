import os, glob

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

# generate docs
install.append( env.Command( "docsHtml", "python", 'epydoc -o doc --html %s' % os.path.join('$SOURCE','*') ) )
install.append( env.Command( "docsPdf", "python", 'epydoc -o doc --pdf %s' % os.path.join('$SOURCE','*') ) )

env.Clean( install, 'tmp' )
env.Clean( install, 'doc' )
env.Clean( install, installDir )

env.Alias( 'install', install)
