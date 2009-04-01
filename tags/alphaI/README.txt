SLUM - Shader Language Unified Manager
author: Hradec (slum@hradec.com)
Version: alpha_D
website: http://code.google.com/p/slum/
support: http://groups.google.com/group/slum-project-development-and-support

before anything, you DON'T need SCons to build and install. SConstruct file is here just to easy the development,
specially when slum starts to get bigger, with more clients, etc.

To install on linux or OSX, you just need to add 2 variables to your environment (or maya.env file):

	Linux and OSX:
		SLUM_PATH			= <path to slum source code folder>
		SLUM_SEARCH_PATH	= $SLUM_PATH/shader
		MAYA_PLUG_IN_PATH	= $SLUM_PATH/python:$MAYA_PLUG_IN_PATH

On Windows its even simpler. Just drop the content of the slum zip file into the folder (assuming you are using maya 2009):

		%HOMEPATH%\My Documents\maya\2009

and add the following lines to the file %HOMEPATH%\My Documents\maya\2009\maya.env
	
		SLUM_PATH			= %HOMEPATH%\My Documents\maya\2009\slumAlphaD
		SLUM_SEARCH_PATH	= %SLUM_PATH%\shader
		MAYA_PLUG_IN_PATH   = %SLUM_PATH%\python
		
if your version of maya is different than 2009, just replace 2009 by the version number you have.

The MAYA_PLUG_IN_PATH tells maya where to find slum plugin, and SLUM_SEARCH_PATH tells slum where to find shader templates.
You can add more paths to the SLUM_SEARCH_PATH environment variable to have slum looking on all those paths.

thats pretty much it...

Keep an eye on our website for new versions:
	http://code.google.com/p/slum/

Don't forget to get in touch trough our forun:
	http://groups.google.com/group/slum-project-development-and-support

and off course, for issues please please please post then at:
	http://code.google.com/p/slum/issues/list

I hope you guys have fun with it and enjoy!

Hradec
