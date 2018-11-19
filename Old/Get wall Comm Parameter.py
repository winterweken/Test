import clr
# import RevitNodes
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
# import Revit Services
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
# import Revit API
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
# import system.
import System
from System.Collections.Generic import *

# get the current Revit document. 
doc = DocumentManager.Instance.CurrentDBDocument

Walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
outList = []
builtInParamType = BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS
# get the type parameter
x = []
y = []
for i in Walls:
	Comments = i.get_Parameter(builtInParamType)
	outList.append(Comments.AsString())
	if Comments.AsString() == "North":
		x.append(i)

    #x.append(Comments.AsString())


OUT = x
