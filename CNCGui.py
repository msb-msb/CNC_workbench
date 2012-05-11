#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2012 Daniel Falck <ddfalck@gmail.com>                   *  
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

__title__="FreeCAD CNC Workbench - GUI part"
__author__ = "Daniel Falck <ddfalck@gmail.com>"
__url__ = ["http://free-cad.sourceforge.net"]

'''
This is the GUI part of the CNC Workbench.
'''

import FreeCAD, FreeCADGui
try:
    from PyQt4 import QtCore,QtGui
except:
    FreeCAD.Console.PrintMessage("Error: PyQt4 package must be installed on your system to use the CNC module.")

class ProfileOp:
    def Activated(self):
        from machining_ops import profile_op1 as profile
        profile.createTask()
        FreeCAD.Console.PrintMessage("profile op activated\n")

    def GetResources(self):
        from utils import Paths, Translator
        IconPath = Paths.iconsPath() + "/profile.png"
        MenuText = str(Translator.translate('Profile Milling'))
        ToolTip  = str(Translator.translate('Create a profile machining op'))
        return {'Pixmap' : IconPath, 'MenuText': MenuText, 'ToolTip': ToolTip} 

class PocketOp:
    def Activated(self):
        FreeCAD.Console.PrintMessage("pocket op not done yet\n")

    def GetResources(self):
        from utils import Paths, Translator
        IconPath = Paths.iconsPath() + "/pocket.png"
        MenuText = str(Translator.translate('Pocket Milling'))
        ToolTip  = str(Translator.translate('Create a pocket machining op'))
        return {'Pixmap' : IconPath, 'MenuText': MenuText, 'ToolTip': ToolTip} 

class DrillOp:
    def Activated(self):
        FreeCAD.Console.PrintMessage("drill op not done yet\n")

    def GetResources(self):
        from utils import Paths, Translator
        IconPath = Paths.iconsPath() + "/drilling.png"
        MenuText = str(Translator.translate('Drilling'))
        ToolTip  = str(Translator.translate('Create a drilling op'))
        return {'Pixmap' : IconPath, 'MenuText': MenuText, 'ToolTip': ToolTip} 

FreeCADGui.addCommand('CNC_Profile', ProfileOp())
FreeCADGui.addCommand('CNC_Pocket', PocketOp())
FreeCADGui.addCommand('CNC_Drill', DrillOp())

