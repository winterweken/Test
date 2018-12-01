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

def tolist(TypeCheck):
	if hasattr(TypeCheck,'__iter__'): return TypeCheck
	else : return [TypeCheck]


walls = DB.FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

wallcheck = tolist(walls)

for z in walls:
	CurtWalls = [getattr(z, 'CurtainGrid', None) is not None for z in wallcheck]
	if CurtWalls == True:
		print('XX')




print(CurtWalls)	

#print(getattr(w, 'CurtainGrid', None) is not None for w in walls)