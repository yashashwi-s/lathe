# The luplot package.
# version 1.5
# Authors: Chetan Shirore and Ajit Kumar
# Email: mathsbeauty@gmail.com

# Introduction
The luaplot package is developed using Lua to plot graphs of real-valued functions of a real variable in LaTeX. It is developed with the  MetaPost system  and luamplib and luacode packages. It provides an easy way for plotting graphs of standard mathematical functions. There is no particular environment in the package for plotting graphs. It also works inside floating environments of LaTeX like tables and figures. The compilation time to plot several graphs in LaTeX using the luaplot package is significantly less with LuaLaTeX engine.

The package is based on the core idea of loading mathematical functions inside Lua and determining plot points using different methods available in Lua. After determining plot points in Lua, two different approaches are used:

	parse plot points to the MetaPost system via luampblib.
 
	parse plot points to the  tikz package.

# License
The luaplot package is released under the LaTeX Project Public License v1.3c or later. 
The complete license text is available at http://www.latex-project.org/lppl.txt. 
It is developed in Lua. 
Lua is available as a certified open-source software. 
Its license is simple and liberal, which is compatible with GPL.

#Installation and Inclusion
The installation of luaplot package is similar to plain latex package, where the .sty file is in LaTeX directory of texmf tree. 
The package can be included with \usepackage{luaplot} command in the preamble of the LaTeX document. 
The TeX file is to be compiled using the LuaLaTeX engine. 