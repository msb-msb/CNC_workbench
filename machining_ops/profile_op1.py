#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2012 Daniel Falck  <ddfalck@gmail.com>                  *  
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

import os
import time
import math
from utils import Paths
from DraftGeomUtils import sortEdges, findMidpoint
from FreeCAD import Vector,Base,Part
import FreeCADGui
import FreeCAD
import FreeCAD as App
import FreeCADGui as Gui
from PyQt4 import QtGui,QtCore
#from PySide import QtGui,QtCore


class TaskPanelCurves:
    def __init__(self):
        #self.ui = App.getResourceDir() + "src/Mod/TemplatePyMod/TaskPanel.ui"
        self.ui = Paths.modulePath() + "/Gui/TaskPanelCurve.ui"

    def accept(self):
        return True

    def reject(self):
        return True

    def clicked(self, index):
        pass

    def open(self):
        pass

    def needsFullSpace(self):
        return False

    def isAllowedAlterSelection(self):
        return True

    def isAllowedAlterView(self):
        return True

    def isAllowedAlterDocument(self):
        return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)

    def helpRequested(self):
        pass

    def setupUi(self):
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget, "TaskPanel")

#comments in header
        form.textEditHeaderComments = form.findChild(QtGui.QTextEdit, "textEditHeaderComments")
#fixture offset combo
        form.comboBoxFixtureOffsets = form.findChild(QtGui.QComboBox, "comboBoxFixtureOffsets")
        form.comboBoxFixtureOffsets.addItems(['G54.1','G54.2','G54.3']) #add additional items to list this way
        form.comboBoxFixtureOffsets.setCurrentIndex(0)

#tool number combo
        form.comboBoxToolSelect =form.findChild(QtGui.QComboBox,"comboBoxToolSelect")
#tool diameter
        form.lineEditToolDaimeter = form.findChild(QtGui.QLineEdit,"lineEditToolDaimeter")
        form.lineEditToolDaimeter.setText('6.35') #read from config file later

#cut mode combo
        form.comboBoxCutMode =form.findChild(QtGui.QComboBox,"comboBoxCutMode")
#tool on side combo
        form.comboBoxToolSide =form.findChild(QtGui.QComboBox,"comboBoxToolSide")
#add curves pushbutton
        form.pushButtonAddCurves = form.findChild(QtGui.QPushButton, "pushButtonAddCurves")
#clear path pushbutton
        form.pushButtonReset = form.findChild(QtGui.QPushButton, "pushButtonReset")
#curve path textEdit
        form.textEditCurve = form.findChild(QtGui.QTextEdit, "textEditCurve")
#reverse path pushbutton
        form.pushButtonReverse = form.findChild(QtGui.QPushButton, "pushButtonReverse")
#start point pushbutton
        form.pushButtonStartPoint = form.findChild(QtGui.QPushButton, "pushButtonStartPoint")
#start point entry box
        form.lineEditStartPoint = form.findChild(QtGui.QLineEdit,"lineEditStartPoint")
#end point pushbutton
        form.pushButtonEndPoint = form.findChild(QtGui.QPushButton, "pushButtonEndPoint")
#end point entry box
        form.lineEditEndPoint = form.findChild(QtGui.QLineEdit, "lineEditEndPoint")
#extend before start lineedit
        form.lineEditExtendStart = form.findChild(QtGui.QLineEdit,"lineEditExtendStart")
        form.lineEditExtendStart.setText('2.0') #read from config file later
#extend after end lineedig
        form.lineEditExtendEnd = form.findChild(QtGui.QLineEdit,"lineEditExtendEnd")
        form.lineEditExtendEnd.setText('2.0') #read from config file later
#auto roll on
        form.checkBoxAutoRollOn = form.findChild(QtGui.QCheckBox, "checkBoxAutoRollOn")
#auto roll off
        form.checkBoxAutoRollOff = form.findChild(QtGui.QCheckBox, "checkBoxAutoRollOff")
#roll on and off radius'
        form.lineEditRollRadius = form.findChild(QtGui.QLineEdit,"lineEditRollRadius")
        form.lineEditRollRadius.setText('2.0') #read from config file later
#lead in length
        form.lineEditLeadIn = form.findChild(QtGui.QLineEdit, "lineEditLeadIn")
        form.lineEditLeadIn.setText('2.0') #read from config file later
#lead out length
        form.lineEditLeadOut = form.findChild(QtGui.QLineEdit, "lineEditLeadOut")
        form.lineEditLeadOut.setText('2.0') #read from config file later
#extra offset
        form.lineEditExtraOffset = form.findChild(QtGui.QLineEdit, "lineEditExtraOffset")
        form.lineEditExtraOffset.setText('0.0') #read from config file later
#absolute incremental mode
        form.comboBoxAbsInc = form.findChild(QtGui.QComboBox, "comboBoxAbsInc")
#clearance height
        form.lineEditClearanceHt = form.findChild(QtGui.QLineEdit, "lineEditClearanceHt")
        form.lineEditClearanceHt.setText('50.0') #read from config file later
#safety space
        form.lineEditSafetySpace = form.findChild(QtGui.QLineEdit, "lineEditSafetySpace")
        form.lineEditSafetySpace.setText('5.0') #read from config file later
#start depth
        form.lineEditStartDepth = form.findChild(QtGui.QLineEdit,"lineEditStartDepth")
        form.lineEditStartDepth.setText('0.0') #read from config file later
#final depth
        form.lineEditFinalDepth = form.findChild(QtGui.QLineEdit,"lineEditFinalDepth")
        form.lineEditFinalDepth.setText('-5.0') #read from config file later
#step down
        form.lineEditStepDown = form.findChild(QtGui.QLineEdit,"lineEditStepDown")
        form.lineEditStepDown.setText('1.0') #read from config file later
#feedrate horizontal
        form.lineEditHorizFeed = form.findChild(QtGui.QLineEdit,"lineEditHorizFeed")
        form.lineEditHorizFeed.setText('650') #read from config file later
#feedrate vertical
        form.lineEditVerticalFeed = form.findChild(QtGui.QLineEdit,"lineEditVerticalFeed")
        form.lineEditVerticalFeed.setText('400') #read from config file later
#spindle speed
        form.lineEditSpindleSpeed = form.findChild(QtGui.QLineEdit,"lineEditSpindleSpeed")
        form.lineEditSpindleSpeed.setText('2400') #read from config file later
#comments in footer
        form.textEditFooterComments = form.findChild(QtGui.QTextEdit, "textEditFooterComments")
#post button
        form.pushButtonPostToFile = form.findChild(QtGui.QPushButton, "pushButtonPostToFile")

        self.form = form

        #Connect Signals and Slots

        QtCore.QObject.connect(form.pushButtonAddCurves, QtCore.SIGNAL("clicked()"), self.make_curves)

        QtCore.QObject.connect(form.pushButtonReset, QtCore.SIGNAL("clicked()"), self.resetPath)

        QtCore.QObject.connect(form.pushButtonReverse, QtCore.SIGNAL("clicked()"), self.reversePath)

        QtCore.QObject.connect(form.pushButtonPostToFile, QtCore.SIGNAL("clicked()"), self.print_it)

    def getMainWindow(self):
        "returns the main window"
        # using QtGui.qApp.activeWindow() isn't very reliable because if another
        # widget than the mainwindow is active (e.g. a dialog) the wrong widget is
        # returned
        toplevel = QtGui.qApp.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                return i
        raise Exception("No main window found")

    def printFixtureIndex(self):
        '''a bug in qt prevents us from just getting the currentIndex from a combobox'''
#        text2 = str(self.comboBoxFixtureOffsets.itemData(self.form.comboBoxFixtureOffsets.currentIndex(),2))+'\n'
#        FreeCAD.Console.PrintMessage(text2)
#        text = str(self.form.comboBoxFixtureOffsets.currentText()+'\n') 
#        FreeCAD.Console.PrintMessage(text)
#        fixture = str(self.form.comboBoxFixtureOffsets.currentText())
#        index =  (self.form.comboBoxFixtureOffsets.findText(fixture))
#        FreeCAD.Console.PrintMessage(str(index))
        fixture = str(self.form.comboBoxFixtureOffsets.currentText())
        index =  self.form.comboBoxFixtureOffsets.findText(fixture)
#        FreeCAD.Console.PrintMessage('workplane('+str(index+1)+')\n')
        return ('workplane('+str(index+1)+')\n')


    def printToolOnSide(self):
        toolside =  (self.form.comboBoxToolSide.currentText())
#        FreeCAD.Console.PrintMessage('tool_side =\''+str(toolside)+'\'\n')
        return ('tool_side =\''+str(toolside)+'\'\n')

    def print_it(self):
        collector = ''
        headerinfo = '''
import os,sys
abspath = os.path.abspath( __file__ )
splitpath = os.path.split( __file__ )
strippedpath = abspath.strip(splitpath[1])
striptmp = len('tmp/')
libs = strippedpath[:-striptmp]+ 'libs'

sys.path.insert(0,libs)
posts = strippedpath[:-striptmp]+ 'posts'

sys.path.insert(0,posts)
machining  = strippedpath[:-striptmp]+ '/machining_ops'

sys.path.insert(0,machining)
import math
import area
area.set_units(1)
import kurve_funcs
from nc import *
import centroid1
output(strippedpath[:-striptmp]+ 'tmp/test.tap')
program_begin(123, 'Test program')
absolute()
metric()

'''
        FreeCAD.Console.PrintMessage(headerinfo)
        collector+=headerinfo
        FreeCAD.Console.PrintMessage('comment(\''+ str(self.form.textEditHeaderComments.toPlainText())+'\')\n')
        collector+=('comment(\''+ str(self.form.textEditHeaderComments.toPlainText())+'\')\n')

        FreeCAD.Console.PrintMessage(self.printFixtureIndex())
        collector+=(self.printFixtureIndex())

        FreeCAD.Console.PrintMessage(self.form.textEditCurve.toPlainText())
        collector+=str(self.form.textEditCurve.toPlainText())

        FreeCAD.Console.PrintMessage('tool_diameter = float('+str(self.form.lineEditToolDaimeter.displayText())+')\n')
        collector+=('tool_diameter = float('+str(self.form.lineEditToolDaimeter.displayText())+')\n')

        FreeCAD.Console.PrintMessage(self.printToolOnSide())
        collector+=(self.printToolOnSide())

        FreeCAD.Console.PrintMessage('flush_nc()\n')
        collector+= ('flush_nc()\n')

        if self.form.lineEditStartPoint.isModified():
            self.start_pt = str(self.form.lineEditStartPoint.displayText())


        if self.form.lineEditEndPoint.isModified():
            self.end_pt = str(self.form.lineEditEndPoint.displayText())



        FreeCAD.Console.PrintMessage('clearance = float('+str(self.form.lineEditClearanceHt.displayText())+')\n')
        collector+=('clearance = float('+str(self.form.lineEditClearanceHt.displayText())+')\n')

        FreeCAD.Console.PrintMessage('rapid_safety_space = float('+str(self.form.lineEditSafetySpace.displayText())+')\n')
        collector+=('rapid_safety_space = float('+str(self.form.lineEditSafetySpace.displayText())+')\n')

        FreeCAD.Console.PrintMessage('roll_on = ' + '\'auto\'\n')
        collector+=('roll_on = ' + '\'auto\'\n')

        FreeCAD.Console.PrintMessage('roll_off = ' + '\'auto\'\n')
        collector+=('roll_off = ' + '\'auto\'\n')

        FreeCAD.Console.PrintMessage('roll_radius = '+str(self.form.lineEditRollRadius.displayText())+'\n')
        collector+=('roll_radius = '+str(self.form.lineEditRollRadius.displayText())+'\n')

        FreeCAD.Console.PrintMessage('lead_in_line_len= '+str(self.form.lineEditLeadIn.displayText())+'\n')
        collector+=('lead_in_line_len= '+str(self.form.lineEditLeadIn.displayText())+'\n')

        FreeCAD.Console.PrintMessage('lead_out_line_len= '+str(self.form.lineEditLeadOut.displayText())+'\n')
        collector+=('lead_out_line_len= '+str(self.form.lineEditLeadOut.displayText())+'\n')

        FreeCAD.Console.PrintMessage('extend_at_start='+str(self.form.lineEditExtendStart.displayText())+'\n')
        collector+=('extend_at_start='+str(self.form.lineEditExtendStart.displayText())+'\n')

        FreeCAD.Console.PrintMessage('extend_at_end='+str(self.form.lineEditExtendEnd.displayText())+'\n')
        collector+=('extend_at_end='+str(self.form.lineEditExtendEnd.displayText())+'\n')

        FreeCAD.Console.PrintMessage('offset_extra = '+str(self.form.lineEditExtraOffset.displayText())+'\n')
        collector+=('offset_extra = '+str(self.form.lineEditExtraOffset.displayText())+'\n')

        FreeCAD.Console.PrintMessage('start_depth = float('+str(self.form.lineEditStartDepth.displayText())+')\n')
        collector+=('start_depth = float('+str(self.form.lineEditStartDepth.displayText())+')\n')

        FreeCAD.Console.PrintMessage('final_depth = float('+str(self.form.lineEditFinalDepth.displayText())+')\n')
        collector+=('final_depth = float('+str(self.form.lineEditFinalDepth.displayText())+')\n')

        FreeCAD.Console.PrintMessage('step_down = float('+str(self.form.lineEditStepDown.displayText())+')\n')
        collector+=('step_down = float('+str(self.form.lineEditStepDown.displayText())+')\n')

        FreeCAD.Console.PrintMessage('feedrate_hv('+str(self.form.lineEditHorizFeed.displayText())+','+str(self.form.lineEditVerticalFeed.displayText())+')\n')
        collector+=('feedrate_hv('+str(self.form.lineEditHorizFeed.displayText())+','+str(self.form.lineEditVerticalFeed.displayText())+')\n')

        #FreeCAD.Console.PrintMessage('roll_on = '+str(self.form.lineEditVerticalFeed.displayText())+'\n')

        FreeCAD.Console.PrintMessage('spindle('+str(self.form.lineEditSpindleSpeed.displayText())+')\n')
        collector+=('spindle('+str(self.form.lineEditSpindleSpeed.displayText())+')\n')

        #FreeCAD.Console.PrintMessage('roll_on = '+str(self.form.lineEditRollRadius.displayText())+'\n')


#kurve_funcs.make_smaller( curve, start = area.Point(63.010089874267578, -49.959426879882812), finish  = area.Point(-74.034454345703125, -15.607303619384766))


        FreeCAD.Console.PrintMessage('kurve_funcs.profile(curve, tool_side , tool_diameter/2, offset_extra, roll_radius, roll_on, roll_off, rapid_safety_space, clearance, start_depth, step_down, final_depth,extend_at_start,extend_at_end,lead_in_line_len,lead_out_line_len )\n')
        collector+=('kurve_funcs.profile(curve, tool_side , tool_diameter/2, offset_extra, roll_radius, roll_on, roll_off, rapid_safety_space, clearance, start_depth, step_down, final_depth,extend_at_start,extend_at_end,lead_in_line_len,lead_out_line_len )\n')

        FreeCAD.Console.PrintMessage("program_end()\n")
        collector+=("program_end()\n")

        pyout = Paths.modulePath() +'/tmp/post.py'
        print pyout
        FILE = open(pyout,"w")

        # Write all the lines at once:
        FILE.writelines(collector)
        FILE.close()
        self.postCode(pyout)



    def postCode(self,postfile):
        if FreeCAD.ActiveDocument.findObjects("Part::Feature","moves"):
            FreeCAD.ActiveDocument.removeObject("moves")
        if FreeCAD.ActiveDocument.findObjects("Part::Feature","rapids"):
            FreeCAD.ActiveDocument.removeObject("rapids")
#        print 'posting code\n'

#        print '###############################'
#        print collector

#        exec str(collector)
#        pyout = '/tmp/post.py'
#        FILE = open(pyout,"w")

#        # Write all the lines at once:
#        FILE.writelines(collector)

#        os.system('python /tmp/post.py')
#        eval(str(collector))
        from subprocess import call
        call(["python", postfile])

#        cncscript= "/home/danfalck/Documents/freecad/backplot/curve_test.py"
#        call(["python", cncscript])

        fin = Paths.modulePath() +"/tmp/test.tap"
        fout = Paths.modulePath() +"/tmp/test.py"
        #print Paths.modulePath() +"/backplot/mill_read.py"
        call([Paths.modulePath() +"/backplot/mill_read.py", fin, fout])
        execfile(Paths.modulePath() +"/tmp/test.py")

##        os.remove("/tmp/test.py")

#        gcodefileSize= os.path.getsize("/tmp/test.tap")
#        if gcodefileSize > 0:
#            execfile("/tmp/test.py")
#        else:
#            print 'file was too small-try again'


    def resetPath(self):
        self.form.textEditCurve.clear()

    def reversePath(self):
        self.form.textEditCurve.append('curve.Reverse()\n')

    def testPost(self):
        self.form.listWidgetCurve.addItem('test\n')



    def make_curves(self):
        item = ""
        edges=[]
        s=Gui.Selection.getSelectionEx()
        for i in s:
            for e in i.SubElementNames:
                edges.append(getattr(i.Object.Shape,e))


        sorted_edges = []
        sorted_edges = sortEdges(edges)
        #item += '#another test after sorted_edges \n'
        def isSameVertex(V1, V2):#borrowed from yorik's fcgeo.py- thanks yorik!
            ''' Test if vertexes have same coordinates with precision 10E(-precision)'''
            if round(V1.X-V2.X,1)==0 and round(V1.Y-V2.Y,1)==0 and round(V1.Z-V2.Z,1)==0 :
                return True
            else :
                return False

        start=sorted_edges[0]
        end=sorted_edges[-1]
        startingZ = start.Vertexes[0].Z
        #set starting depth to same Z as starting curve element
        self.form.lineEditStartDepth.setText(str(start.Vertexes[0].Z))
        item += "curve = area.Curve()\n"
        if isSameVertex(start.Vertexes[0],end.Vertexes[1]) :
            item += '#closed path\n'
            path = 'closedpath'
        else:
            item += '#open path\n'
            path = 'openpath'

        if path ==  'openpath' :
            item += "curve.append(area.Point(" + str(start.Vertexes[0].X) + "," + str(start.Vertexes[0].Y)+ "))\n"

        for s in sorted_edges:
            #edges.append(s)
            if (isinstance(s.Curve,Part.Circle)):
                mp = findMidpoint(s)
                ce = s.Curve.Center
                tang1 = s.Curve.tangent(s.ParameterRange[0]) ; tang2 = s.Curve.tangent(s.ParameterRange[1])
                cross1 = Vector.cross(Base.Vector(tang1[0][0],tang1[0][1],tang1[0][2]),Base.Vector(tang2[0][0],tang2[0][1],tang2[0][2]))
                if cross1[2] > 0:
                    direct = '1 ' #we seem to be working in a rh system in FreeCAD 
                else:
                    direct = '-1 ' 
                item += "curve.append(area.Vertex("+str(direct)+ ", area.Point( "+ str(s.Vertexes[-1].Point[0])+", "+str(s.Vertexes[-1].Point[1])+ "), area.Point("+str(s.Curve.Center [0])+ ", " + str(s.Curve.Center[1])+ ")))\n"

            elif (isinstance(s.Curve,Part.Line)):
                item += "curve.append(area.Point( "+str(s.Vertexes[-1].Point[0])+", " +str(s.Vertexes[-1].Point[1])+ "))\n"
            else:
                pass

        #export curve elements to heekscnc
        #to reverse the curve:

        #item += "curve.append(area.Point(" + str(end.Vertexes[0].X) + "," + str(end.Vertexes[0].Y) + "))"
        if path ==  'closedpath':
            item += "curve.append(area.Point(" + str(start.Vertexes[1].X) + "," + str(start.Vertexes[1].Y)+ "))\n"
            item += "curve.Reverse()\n"
        self.form.textEditCurve.append(item)

    def addElement(self):
        item=QtGui.QInputDialog.getText(self.form, 'Add item', 'Enter:')
        if item[1]:
            self.form.listWidget.addItem(item[0])




def createTask():
    panel1 = TaskPanelCurves()
    Gui.Control.showDialog(panel1)
    panel1.setupUi()
    return panel1


