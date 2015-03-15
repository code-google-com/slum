# Introduction #

SLUM shader templates are written as a python class derivated from one of the following:

**slumSurface**slumVolume
**slumDisplacement**slumLight
**slumColor**slumFloat

SLUM will look for shader templates on all paths specified in the SLUM\_SEARCH\_PATH environment variable, and also, in the shaders folder in the installation folder. (also, in windows, it looks into "Documents/slum/shaders")

# Details #

An slum shader template has a few simple rules:

**every shader MUST have an unique ID to avoid shader clashing. (an automated central system is planned were developers will be able to create a universal unique ID). This unique ID is retrieve by SLUM by calling the ID() method, which returns the ID as an int.** every shader MUST have an parameters() method which defines the UI parameters showed on an client (clients can be any software. Right now, we only have an Maya client)
**shader classes implement renderer specific shader code by creating methods named as the renderer, for example, delight() method is used for 3delight, cgfx() method is used for cgfx GPU render, renderman() is used for renderman, air() for air renderer, etc.** if a shader is used with a unsupported renderer (the shader class doesnt have the renderer method), slum will render with a standard shader.

## a simple diffuse shader example: ##

```
#
# diffuse.slum - a simple diffuse slum surface shader to be used by
#                 developers as a template shader.
#
#    Copyright (C) 2008 - Roberto Hradec
#
# ---------------------------------------------------------------------------
#     This file is part of SLUM.
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

class diffuse(slumSurface):
    def ID(self):
        '''
            a unique ID that identifys the shader inside slum. If you upload
            this template to a online repository, this method will be replaced
            automatically by the repository server, with the next global available ID.
        '''
        return 2

    def parameters(self):
        '''
            This method defines all the parameter for our shader template. Keep in mind that here you define
            the parameters that the user will see, not necessarily the same parameters of the shaders that this template
            defines.
        '''
        Intensity     = parameter( 1.0, 'Intensity', help = 'Diffuse intensity.', max = 10, min = 0 )
        Color         = parameter( color(1), 'Color', help = 'Color for the diffuse.' )

        OutColor         = parameter( color(1), 'outColor', output=True )         # required for 3delight surface shaders
        OutTransparency = parameter( color(0), 'outTransparency', output=True ) # required for 3delight surface shaders

        return  group( [
            OutColor,
            OutTransparency,
            Intensity,
            Color,
        ], name = 'Simple Diffuse' )


    def delight(self, node):
        '''
            delight method is were you define the code for this shader, when rendering in 3delight.
            this is a renderer method. a renderer method should allways return a tupple as:
            ( <list of strings that define the shader parameters>, <list of strings that define the shader code>)
        '''
        # 3deligth shader parameters
        shaderPars = [
            'float Intensity     = %f;'    % node['Intensity'],
            'color Color        = %s;'    % node['Color'],

            'output varying color outColor=0;',
            'output varying color outTransparency=0;'
        ]

        # shader code
        code=['''
                extern normal N;
                extern point P;
                outColor = diffuse(normalize(N)) * Color * Intensity;
            ''']

        # return a tupple
        return (shaderPars, code)

    def cgfx(self, node):
        code=['''
        ''']
        return ("",code)
```