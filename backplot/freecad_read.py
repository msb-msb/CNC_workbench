#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2011,2012 Daniel Falck <ddfalck@gmail.com>              *
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
################################################################################
# freecad_read.py
#
# Base class for NC code parsing into FreeCAD
#
# Dan Falck, 2011-10-21
################################################################################
import geom2d as g2d


#coords = Save(repr(0),repr(0),repr(0))        
class Save:
    def __init__(self, str1,str2,str3):
    
      self.x = str1
      self.y = str2
      self.z = str3
  # Two methods:
    def show(self):
        return self.x+' '+self.y+ ' '+ self.z
    def show_arc(self):
        return self.x+' '+self.y
    def x_old(self):
        return self.x
    def y_old(self):
        return self.y    
    def z_old(self):
        return self.z

class arc_save:
	#need to save some info on arcs for creating tangent arcs
	#with center point and end point
	#probably need a line segment to start off with before doing first arc in path
	def __init__(self,cen_pt,end_pt):
		self.cent= cen_pt
		self.end = end_pt
		self.cen_x,self.cen_y = cen_pt #just in case...
		self.end_x,self.end_y = end_pt
		
	def center(self):
		return self.cent
	def end(self):
		return self.end
		
class line_save:
	#need to save some info on lines for creating tangent arcs
	#with start point and end point- will help find center of next arc
	def __init__(self,start_pt,end_pt):
		self.start= start_pt
		self.end = end_pt
		
	def start(self):
		return self.start
	def end(self):
		return self.end		

################################################################################
class Parser:

    def __init__(self):
        self.currentx = 0.0
        self.currenty = 0.0
        self.currentz = 12.0
        self.old_position = Save(self.currentx,self.currenty,self.currentz)
        self.absolute_flag = True

    ############################################################################
    ##  Internals

    def files_open(self, name, oname=None):
        if (oname == None ):
            oname = (name+'.py')
        self.file_in = open(name, 'r')
        self.file_out = open(oname, 'w')
        
        #self.file_out.write('SET_ORIGIN_OFFSETS[0.0,0.0,0.0]\n')
        #self.file_out.write('<?xml version="1.0" ?>\n')
        #self.file_out.write('<nccode>\n')

    def files_close(self):
        #self.file_out.write('</nccode>\n')

        self.file_in.close()
        self.file_out.close()

    def readline(self):
        self.line = self.file_in.readline().rstrip()
        if (len(self.line)) : return True
        else : return False

    def write(self, s):
        self.file_out.write(s)

    ############################################################################

    def begin_ncblock(self):
        self.file_out.write('import FreeCAD \n')
        self.file_out.write('from FreeCAD import Base\n')
        self.file_out.write('import Part\n')
        self.file_out.write('rapids = []\n')
        self.file_out.write('shapes = []\n')

    def end_ncblock(self):
        #self.file_out.write('shapes.append(move)\n')

        self.file_out.write('object=FreeCAD.ActiveDocument.addObject("Part::Feature","rapids")\n')
        self.file_out.write('object.Shape=Part.makeCompound(rapids)\n')
        self.file_out.write('object.ViewObject.LineColor = (1.0,0.33,1.0)#light magenta/purple\n')
        self.file_out.write('object.ViewObject.LineWidth = 2.0\n')


        self.file_out.write('object=FreeCAD.ActiveDocument.addObject("Part::Feature","moves")\n')
        self.file_out.write('object.Shape=Part.makeCompound(shapes)\n')
        self.file_out.write('object.ViewObject.LineColor = (0.0,1.0,0.0)#green\n')
        self.file_out.write('object.ViewObject.LineWidth = 1.0\n')
        self.file_out.write('#end of file \n')

    def add_text(self, s, col=None, cdata=False):
        s.replace('&', '&amp;')
        s.replace('"', '&quot;')
        s.replace('<', '&lt;')
        s.replace('>', '&gt;')
        if (cdata) : (cd1, cd2) = ('<![CDATA[', ']]>')
        else : (cd1, cd2) = ('', '')
        if (col != None) : self.file_out.write('\t\t<text col="'+col+'">'+cd1+s+cd2+'</text>\n')
        else : self.file_out.write('\t\t<text>'+cd1+s+cd2+'</text>\n')

    def set_mode(self, units=None):
        pass
        #self.file_out.write('\t\t<mode')
        #if (units != None) : self.file_out.write(' units="'+str(units)+'"')
        #self.file_out.write(' />\n')

    def set_tool(self, number=None):
        pass
        
    def move_style(self, line_stl="0"): 
        if (line_stl== "0"):
             #self.line_style_font= "/colorno 5 /linefontno 5 ]" #rapids
            self.movement= 'rapid'
        else:
            #self.line_style_font= "/colorno 3 ]" #feed moves
            self.movement= 'feed'


    def begin_path(self, col=None):
        pass
        #if (col != None) : self.file_out.write(col)
        #else : self.file_out.write('\t\t<path>\n')

    def end_path(self):
        #self.file_out.write('\n')
        pass

    def add_line(self, x=None, y=None, z=None, a=None, b=None, c=None):
        if (x == None and y == None and z == None and a == None and b == None and c == None) : return
        #self.file_out.write('object=FreeCAD.ActiveDocument.addObject("Part::Feature","G1_")\n')
        if self.movement == 'rapid':
            if ( self.old_position.x_old() == x and self.old_position.y_old() == y ):
                self.file_out.write('#rapid=Part.makeLine(('+str(self.old_position.x_old())+' ,'+str(self.old_position.y_old())+' ,'+str(self.old_position.z_old())+' ),( ')
            else:
                self.file_out.write('rapid=Part.makeLine(('+str(self.old_position.x_old())+' ,'+str(self.old_position.y_old())+' ,'+str(self.old_position.z_old())+' ),( ')
        else:
            self.file_out.write('move=Part.makeLine(('+str(self.old_position.x_old())+' ,'+str(self.old_position.y_old())+' ,'+str(self.old_position.z_old())+' ),( ')
        if (x == None):
            x = self.old_position.x_old()
        if (x != None) :
            if self.absolute_flag: self.currentx = x
            else: self.currentx = self.currentx + x
            self.file_out.write(str(self.currentx)+' ,')
        if (y == None):
            y = self.old_position.y_old()
        if (y != None) :
            if self.absolute_flag: self.currenty = y
            else: self.currenty = self.currenty + y
            self.file_out.write(str(self.currenty)+' ,')
        if (z == None):
            z = self.old_position.z_old()
        if (z != None) :
            if self.absolute_flag: self.currentz = z
            else: self.currentz = self.currentz + z
            self.file_out.write(str(self.currentz))
        self.file_out.write('))\n')
        self.old_position = Save(self.currentx,self.currenty,self.currentz)
        if self.movement == 'rapid':
            self.file_out.write('rapids.append(rapid)\n')
        else:
            self.file_out.write('shapes.append(move)\n')


    def add_arc(self, x=None, y=None, z=None, i=None, j=None, k=None, r=None, d=None):
        #print self.old_pts.start, ' ' , self.old_pts.end
        if (x == None and y == None and z == None and i == None and j == None and k == None and r == None and d == None) : return
        if (x != None) :
            if self.absolute_flag: self.currentx = x
            else: self.currentx = self.currentx + x

        if (y != None) :
            if self.absolute_flag: self.currenty = y
            else: self.currenty = self.currenty + y

        if (z == None):
            z = self.old_position.z_old()
        if (z != None) :
            if self.absolute_flag: self.currentz = z
            else: self.currentz = self.currentz + z

        #first case- no i,j components
        if (i == None and j == None and r != None):
            #find midpoint of line between start_pt and end_pt
            p1 = (self.old_position.x_old(), self.old_position.y_old())
            p2 = (self.currentx, self.currenty)
            xstart,ystart= p1;xend,yend=p2
            #find center of radius by creating circles with radius r
            #at start and end points- then determine the intersection point
            #that is on the correct side of the line going from p1 to p2 
            circ_ints= g2d.circ_circ_inters(xstart,ystart, r, xend,yend, r)
            '''Return list of intersection pts of 2 circles.'''
            #print circ_ints
            cen_pt1,cen_pt2 = circ_ints
            #pt_on_RHS_p(pt, p0, p1)
            """Return True if pt is on right hand side going from p0 to p1."""
            if (d ==-1 and g2d.pt_on_RHS_p(cen_pt1,p1,p2)):
                center = cen_pt1
                xcen,ycen = center
                #self.file_out.write('object=FreeCAD.ActiveDocument.addObject("Part::Feature","G2_")\n')
                direction = (0,0,1)
                radius, center, start_angle, end_angle = g2d.arc_angle_format(direction,(self.currentx, self.currenty),(xcen,ycen),(self.old_position.x_old(),self.old_position.y_old()))
                self.file_out.write('move=Part.makeCircle('+str(radius)+ ', Base.Vector('+str(center[0])+','+str(center[1])+','+str(self.currentz)+')'+','+' Base.Vector('+str(direction[0])+','+str(direction[1])+','+str(direction[2])+'),'+str(start_angle)+','+str(end_angle)+')\n') 
                self.file_out.write('shapes.append(move)\n') 

            else:
                center = cen_pt2
                xcen,ycen = center
                #self.file_out.write('object=FreeCAD.ActiveDocument.addObject("Part::Feature","G3_")\n')
                direction = (0,0,1)
                radius, center, start_angle, end_angle = g2d.arc_angle_format(direction,(self.old_position.x_old(),self.old_position.y_old()),(xcen,ycen),(self.currentx, self.currenty))
                self.file_out.write('move=Part.makeCircle('+str(radius)+ ', Base.Vector('+str(center[0])+','+str(center[1])+','+str(self.currentz)+')'+','+' Base.Vector('+str(direction[0])+','+str(direction[1])+','+str(direction[2])+'),'+str(start_angle)+','+str(end_angle)+')\n')  
                self.file_out.write('shapes.append(move)\n')
            
        elif (i != None and j !=None):#use i and j centers
            
            xcen = self.old_position.x_old() + i; ycen = self.old_position.y_old() + j 
            if (d ==-1):
                #self.file_out.write('object=FreeCAD.ActiveDocument.addObject("Part::Feature","G2_")\n')
                direction = (0,0,1)
                radius, center, start_angle, end_angle = g2d.arc_angle_format(direction,(self.currentx, self.currenty),(xcen,ycen),(self.old_position.x_old(),self.old_position.y_old()))
                self.file_out.write('move=Part.makeCircle('+str(radius)+ ', Base.Vector('+str(center[0])+','+str(center[1])+','+str(self.currentz)+')'+','+' Base.Vector('+str(direction[0])+','+str(direction[1])+','+str(direction[2])+'),'+str(start_angle)+','+str(end_angle)+')\n')  
                self.file_out.write('shapes.append(move)\n')
                
            else:
                #self.file_out.write('object=FreeCAD.ActiveDocument.addObject("Part::Feature","G2_")\n')
                direction = (0,0,1)
                radius, center, start_angle, end_angle = g2d.arc_angle_format(direction,(self.old_position.x_old(),self.old_position.y_old()),(xcen,ycen),(self.currentx, self.currenty))
                self.file_out.write('move=Part.makeCircle('+str(radius)+ ', Base.Vector('+str(center[0])+','+str(center[1])+','+str(self.currentz)+')'+','+' Base.Vector('+str(direction[0])+','+str(direction[1])+','+str(direction[2])+'),'+str(start_angle)+','+str(end_angle)+')\n')  
                self.file_out.write('shapes.append(move)\n')
            
        elif (x == None and i == None and j !=None):#use inferred x and i 
            
            xcen = self.old_position.x_old(); ycen = self.old_position.y_old() + j 
            if (d ==-1):
                #self.file_out.write('object=FreeCAD.ActiveDocument.addObject("Part::Feature","G3_")\n')
                direction = (0,0,1)
                radius, center, start_angle, end_angle = g2d.arc_angle_format(direction,(self.old_position.x_old(),self.old_position.y_old()),(xcen,ycen),(self.currentx, self.currenty))
                self.file_out.write('move=Part.makeCircle('+str(radius)+ ', Base.Vector('+str(center[0])+','+str(center[1])+','+str(self.currentz)+')'+','+' Base.Vector('+str(direction[0])+','+str(direction[1])+','+str(direction[2])+'),'+str(start_angle)+','+str(end_angle)+')\n')  
                self.file_out.write('shapes.append(move)\n')
                
            else:
                #self.file_out.write('object=FreeCAD.ActiveDocument.addObject("Part::Feature","G3_")\n')
                direction = (0,0,1)
                radius, center, start_angle, end_angle = g2d.arc_angle_format(direction,(self.old_position.x_old(),self.old_position.y_old()),(xcen,ycen),(self.currentx, self.currenty))
                self.file_out.write('move=Part.makeCircle('+str(radius)+ ', Base.Vector('+str(center[0])+','+str(center[1])+','+str(self.currentz)+')'+','+' Base.Vector('+str(direction[0])+','+str(direction[1])+','+str(direction[2])+'),'+str(start_angle)+','+str(end_angle)+')\n')  
                self.file_out.write('shapes.append(move)\n')
                 
        elif (i == None and j !=None):#use inferred i 
            
            xcen = self.old_position.x_old(); ycen = self.old_position.y_old() + j 
            if (d ==-1):
                #self.file_out.write('object=FreeCAD.ActiveDocument.addObject("Part::Feature","G2_")\n')
                direction = (0,0,1)
                radius, center, start_angle, end_angle = g2d.arc_angle_format(direction,(self.currentx, self.currenty),(xcen,ycen),(self.old_position.x_old(),self.old_position.y_old()))
                self.file_out.write('move=Part.makeCircle('+str(radius)+ ', Base.Vector('+str(center[0])+','+str(center[1])+','+str(self.currentz)+')'+','+' Base.Vector('+str(direction[0])+','+str(direction[1])+','+str(direction[2])+'),'+str(start_angle)+','+str(end_angle)+')\n')   
                self.file_out.write('shapes.append(move)\n')
                
            else:
                #self.file_out.write('object=FreeCAD.ActiveDocument.addObject("Part::Feature","G2_")\n')
                direction = (0,0,1)
                radius, center, start_angle, end_angle = g2d.arc_angle_format(direction,(self.old_position.x_old(),self.old_position.y_old()),(xcen,ycen),(self.currentx, self.currenty))
                self.file_out.write('move=Part.makeCircle('+str(radius)+ ', Base.Vector('+str(center[0])+','+str(center[1])+','+str(self.currentz)+')'+','+' Base.Vector('+str(direction[0])+','+str(direction[1])+','+str(direction[2])+'),'+str(start_angle)+','+str(end_angle)+')\n')                         
                self.file_out.write('shapes.append(move)\n')
            
        elif (i != None and j ==None): #use inferred j
            
            xcen = self.old_position.x_old() + i; ycen = self.old_position.y_old()  
            if (d ==-1):
                #self.file_out.write('object=FreeCAD.ActiveDocument.addObject("Part::Feature","G2_")\n')
                direction = (0,0,1)
                radius, center, start_angle, end_angle = g2d.arc_angle_format(direction,(self.currentx, self.currenty),(xcen,ycen),(self.old_position.x_old(),self.old_position.y_old()))
                self.file_out.write('move=Part.makeCircle('+str(radius)+ ', Base.Vector('+str(center[0])+','+str(center[1])+','+str(self.currentz)+')'+','+' Base.Vector('+str(direction[0])+','+str(direction[1])+','+str(direction[2])+'),'+str(start_angle)+','+str(end_angle)+')\n')   
                self.file_out.write('shapes.append(move)\n')
                
            else:
                #self.file_out.write('object=FreeCAD.ActiveDocument.addObject("Part::Feature","G3_")\n')
                direction = (0,0,1)
                radius, center, start_angle, end_angle = g2d.arc_angle_format(direction,(self.old_position.x_old(),self.old_position.y_old()),(xcen,ycen),(self.currentx, self.currenty))
                self.file_out.write('move=Part.makeCircle('+str(radius)+ ', Base.Vector('+str(center[0])+','+str(center[1])+','+str(self.currentz)+')'+','+' Base.Vector('+str(direction[0])+','+str(direction[1])+','+str(direction[2])+'),'+str(start_angle)+','+str(end_angle)+')\n')   
                self.file_out.write('shapes.append(move)\n')
                
            #self.file_out.write(self.line_style_color)
                
        
        self.old_position = Save(self.currentx,self.currenty,self.currentz)
        
    def incremental(self):
        self.absolute_flag = False
        #print 'incremental!\n'
    def absolute(self):
        self.absolute_flag = True
        #print 'absolute!\n'

    def u_move(self):
        self.u_flag = True

    def w_move(self):
        self.w_flag = True
