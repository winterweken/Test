
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

from System.Collections.Generic import *


#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
collector = FilteredElementCollector(doc)
walls = collector.OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
ex = []
ex1 = []
IW = []
yy = []
for i in walls:
	try:
		IW.append(i.WallType.get_Parameter(BuiltInParameter.FUNCTION_PARAM).AsValueString() == "Exterior")
		yy.append(i)

	except:
		ex.append(None)

for s in yy:
	if s.WallType.get_Parameter(BuiltInParameter.FUNCTION_PARAM).AsValueString() == "Exterior":
		ex1.append(s)

	#if IW == True:
		#yy.append(i)

#if i.WallType.get_Parameter(BuiltInParameter.FUNCTION_PARAM).AsValueString() == "Exterior":
#		interiorWalls.append(i)


OUT = ex1
