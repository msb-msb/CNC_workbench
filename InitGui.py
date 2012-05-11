#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2012                                              *  
#*   Daniel Falck <ddfalck@gmail.com>                                      *  
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


class CNCWorkbench (Workbench ):
    """CNC module. Here toolbars & icons are placed. """
    from utils import Paths
    import CNCGui


    Icon = Paths.iconsPath() + "/end_mill.xpm"

    MenuText = "CNC Machining"
    ToolTip = "A CNC programming workbench using python libs"

    def Initialize(self):
        depsOK = False
        try:
            from pivy import coin
            if FreeCADGui.getSoDBVersion() != coin.SoDB.getVersion():
                raise AssertionError("FreeCAD and Pivy use different versions of Coin. This will lead to unexpected behaviour.")
        except AssertionError:
            FreeCAD.Console.PrintWarning("Error: FreeCAD and Pivy use different versions of Coin. This will lead to unexpected behaviour.\n")
        except ImportError:
            FreeCAD.Console.PrintWarning("Error: Pivy not found, CNC workbench will be disabled.\n")
        except:
            FreeCAD.Console.PrintWarning("Error: Unknown error while trying to load Pivy\n")
        else:
            try:
                from PyQt4 import QtGui,QtCore
            except ImportError:
                FreeCAD.Console.PrintWarning("Error: PyQt not found, CNC workbench will be disabled.\n")
            else:
                depsOK = True

        if depsOK:
            FreeCAD.Console.PrintMessage("OK, let's try to do something now\n")

        # ToolBar
        list = ["CNC_Profile","CNC_Pocket","CNC_Drill"]
        self.appendToolbar("Machining",list)
        
        # Menu
        list = ["CNC_Profile","CNC_Pocket","CNC_Drill"]
        self.appendMenu("Machining",list)


    def Activated(self):
#        self.tab = self.getComboView(self.getMainWindow())
#        self.tab2=QtGui.QDialog()
#        self.tab.addTab(self.tab2,"A Special Tab")
#        self.tab2.show()
        FreeCAD.Console.PrintMessage("Beam me down Scotty.\n")
#        self.profile.createTask()



    def Deactivated(self):
#        tab = getComboView(getMainWindow())
#        tab.removeTab(2)
        FreeCAD.Console.PrintMessage("Jim, another 'red shirt' died on the planet's surface!\n")

#    def ContextMenu(self, recipient):
#        if (recipient == "View"):
#            if (FreeCAD.activeCNCCommand == None):
#                if (FreeCADGui.Selection.getSelection()):
#                    self.appendContextMenu("CNC",self.cmdList+self.modList)
#                    self.appendContextMenu("Display options",self.treecmdList)
#                else:
#                    self.appendContextMenu("CNC",self.cmdList)
#            else:
#                if (FreeCAD.activeCNCCommand.featureName == "Profile"):
#                    self.appendContextMenu("",self.profile)
#        else:
#            if (FreeCADGui.Selection.getSelection()):
#                self.appendContextMenu("Display options",self.treecmdList)



Gui.addWorkbench(CNCWorkbench())
