
import clr
import sys
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
clr.AddReference("RevitNodes")
import Revit
import RevitServices
clr.ImportExtensions(Revit.Elements)
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
Windows = collector.OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()
Win =  []

for z in Windows:
	Win.append(z)

if isinstance(Win, list):
	elements = []
	for i in Win:
		elements.append(UnwrapElement(i))
else:
	elements = Win

def GetHostElement(element):
	doc = DocumentManager.Instance.CurrentDBDocument
	try:
		host = element.Host
		return host
	except:
		try:
			hostIds = []
			for i in element.GetHostIds():
				hostIds.append(doc.GetElement(i))
			return hostIds
		except:
			return None

def ProcessList(_func, _list):
	return map( lambda x: ProcessList(_func, x) if type(x) == list else _func(x), _list )

try:
	errorReport = None
	if isinstance(elements, list):
		output = ProcessList(GetHostElement, elements)
	else:
		output = GetHostElement(elements)
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = output
else:
	OUT = errorReport
