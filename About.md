![http://slum.googlecode.com/svn/trunk/logo/slumNodes00.jpg](http://slum.googlecode.com/svn/trunk/logo/slumNodes00.jpg)![http://slum.googlecode.com/svn/trunk/logo/slumNodes01.jpg](http://slum.googlecode.com/svn/trunk/logo/slumNodes01.jpg)

# About Slum #

SLUM is a project designed to be a central hub for development of render shaders for computer graphics in general.

Basically, SLUM gives you the capability of design one shader that contains language components for more than one render software, like GLSL, Renderman, 3Delight, Air, etc.

SLUM is also capable of gather/release shaders from special online repositories, opening new possibilities for developers to share their work with artists all around.

Just to give a quick idea of how SLUM is organized, we can say that its basically done in 2 main components:

  1. Unified Manager component, which deals with the logic and evaluation of the shaders templates and translation of shader networks. This component is one for all implementations of slum in different 3D Packages.
  1. The client component, which interfaces the Unified Manager with different 3D packages, like Maya, 3Delight for Maya, Blender, Mayaman, Renderman Studio, etc.

So, basically, SLUM is the Unified Manager component, and it rely on client components to interface it with the 3D packages in the market.

The client component will be organize in such a way that will make easy for someone develop a new implementation. For example, the main Maya client component can be used as a base to develop the 3Delight for Maya Client or the Mayaman client.

As the main Maya client component have support for GLSL/CGfx shader code, the 3delight for Maya will inherit this feature, so one can develop a new 3delight shader using a slum template, add some GLSL code to it and automatically have a realtime feedback of the shader in the viewport.

SLUM is all developed in Python, as today python is being chosen by all major 3D Packages as the default script language. This make the Client implementation way easier and straight forward.

All SLUM templates are also in Python. A shader will consist of a class derivate from a slum base class, which contains methods to define all the code for all renderers that shader supports. The code is returned as text to SLUM, which then is responsible of deal with it to release the shader in the appropriated format. Having the shader template defined as python code opens a lot of new possibilities to the developer, making it possible to develop dynamically generated shading code.

To start with, SLUM will be available for download with the Unified Manager component, the Maya client and the 3Delight for maya client. (as soon as I got it up and running)