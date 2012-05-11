import sys
sys.path.insert(0,'/home/danfalck/git3/free-cad/Mod/CNC/posts')
sys.path.insert(0,'/home/danfalck/git3/free-cad/Mod/CNC/machining_ops')
import math
import area
import kurve_funcs
area.set_units(1)
from nc import *
import emc2b
output('/home/danfalck/git3/free-cad/Mod/CNC/tmp/fctest.tap')
absolute()
metric()
set_plane(0)
workplane(1)
comment('tool change to 4.7752 mm Carbide End Mill')
tool_change( id=4)
spindle(7000)
feedrate_hv(840, 100)
flush_nc()
clearance = float(5)
rapid_safety_space = float(2)
start_depth = float(0)
step_down = float(1)
final_depth = float(-1)
tool_diameter = float(4.7752)
cutting_edge_angle = float(0)
#absolute() mode
roll_radius = float(2)
offset_extra = 0
comment('Sketch')
curve = area.Curve()
#open path
curve.append(area.Point(66.163292,40.55579))
curve.append(area.Point( 66.163292, -37.200397))
curve.append(area.Vertex(-1 , area.Point( 56.163292, -47.200397), area.Point(56.163292, -37.200397)))
curve.append(area.Point( -58.730675, -47.200397))
curve.append(area.Vertex(-1 , area.Point( -68.730675, -37.200397), area.Point(-58.730675, -37.200397)))
curve.append(area.Point( -68.730675, 40.55579))

roll_on = 'auto'
roll_off = 'auto'
extend_at_start= 0
extend_at_end= 0
lead_in_line_len= 0
lead_out_line_len= 0
kurve_funcs.profile(curve, 'left', tool_diameter/2, offset_extra, roll_radius, roll_on, roll_off, rapid_safety_space, clearance, start_depth, step_down, final_depth,extend_at_start,extend_at_end,lead_in_line_len,lead_out_line_len )
absolute()
program_end()