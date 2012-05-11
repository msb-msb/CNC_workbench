import FreeCAD 
from FreeCAD import Base
import Part
rapids = []
shapes = []
object=FreeCAD.ActiveDocument.addObject("Part::Feature","rapids")
object.Shape=Part.makeCompound(rapids)
object.ViewObject.LineColor = (1.0,0.33,1.0)#light magenta/purple
object.ViewObject.LineWidth = 2.0
object=FreeCAD.ActiveDocument.addObject("Part::Feature","moves")
object.Shape=Part.makeCompound(shapes)
object.ViewObject.LineColor = (0.0,1.0,0.0)#green
object.ViewObject.LineWidth = 1.0
#end of file 
