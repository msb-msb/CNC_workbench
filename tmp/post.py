
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

comment('')
workplane(1)




curve = area.Curve()
#closed path
curve.append(area.Point( 16.2551994324, 9.0))
curve.append(area.Vertex(1 , area.Point( 16.2552, 17.7616031082), area.Point(16.2552, 13.3808)))
curve.append(area.Point( -24.0, 17.7616004944))
curve.append(area.Vertex(1 , area.Point( -24.0, 8.99999689178), area.Point(-24.0, 13.3808)))
curve.append(area.Point(-24.0,17.7616031082))curve.append(area.Point(16.2551994324,9.0))
curve.Reverse()
tool_diameter = float(6.35)
tool_side ='left'
flush_nc()
clearance = float(50.0)
rapid_safety_space = float(5.0)
roll_on = 'auto'
roll_off = 'auto'
roll_radius = 2.0
lead_in_line_len= 2.0
lead_out_line_len= 2.0
extend_at_start=2.0
extend_at_end=2.0
offset_extra = 0.0
start_depth = float(0.0)
final_depth = float(-5.0)
step_down = float(1.0)
feedrate_hv(650,400)
spindle(2400)
kurve_funcs.profile(curve, tool_side , tool_diameter/2, offset_extra, roll_radius, roll_on, roll_off, rapid_safety_space, clearance, start_depth, step_down, final_depth,extend_at_start,extend_at_end,lead_in_line_len,lead_out_line_len )
program_end()
