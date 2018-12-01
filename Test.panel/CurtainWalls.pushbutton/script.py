#IMPORTS

#for timing
from pyrevit.coreutils import Timer
from pyrevit.output import charts
from pyrevit import script
timer = Timer()

#for the script to work
import math
import clr
import sys
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

output = script.get_output()

def tolist(TypeCheck):
	if hasattr(TypeCheck,'__iter__'): return TypeCheck
	else : return [TypeCheck]


walls = DB.FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

wallcheck = tolist(walls)
CurtWalls = []
CurtID = []

#CurtWalls = [getattr(z, 'CurtainGrid', None) is not None for z in wallcheck]

for z in wallcheck:
	if getattr(z, 'CurtainGrid', None) is not None:
		CurtWalls.append(z)




#print(output.linkify(CurtWalls))
for zz in CurtWalls:
	print(output.linkify(zz.Id))
print(CurtID)

#print(getattr(w, 'CurtainGrid', None) is not None for w in walls)
