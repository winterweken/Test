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

#FUNCTIONS

#function that transforms project north 2D normals into real north 2D normals, given the angle between project and real north.
def project_to_real_north(x, y, radians):
                newX = x * math.cos(radians) + y * math.sin(radians)
                newY = -x * math.sin(radians) + y * math.cos(radians)
                return round(newX, 4), round(newY, 4)

#function that assigns an orientation to a 2D vector according a compass rose.
def vector_orientation (x, y):
                if x <= 0.3826 and x >= -0.3826 and y <= 1 and y >= 0.9238:
                                return "North"
                elif x < 0.8660 and x > 0.3826 and y < 0.9238 and y > 0.5000:
                                return "Northeast"
                elif x <= 1 and x >= 0.8660 and y <= 0.5000 and y >= -0.3583:
                                return "East"
                elif x < 0.9335 and x > 0.3090 and y < -0.3583 and y > -0.9510:
                                return "Southeast"
                elif x <= 0.3090 and x >= -0.3090 and y <= -0.9510 and y >= -1:
                                return "South"
                elif x < -0.3090 and x > -0.9335 and y < -0.3583 and y > -0.9510:
                                return "Southwest"
                elif x <= -0.8660 and x >= -1 and y <= 0.5000 and y >= -0.3583:
                                return "West"
                elif x < -0.3826 and x > -0.8660 and y < 0.9238 and y > 0.5000:
                                return "Northwest"
                else:
                                return "No orientation"

#get workset names
def GetWorkset(itemx):
	if hasattr(itemx, "WorksetId"): return itemx.Document.GetWorksetTable().GetWorkset(itemx.WorksetId)
	else: return None

#Check for curtain walls
def CurtainCheck(TypeCheck):
	if hasattr(TypeCheck,'__iter__'): return TypeCheck
	else : return [TypeCheck]
	
	
#VARIABLES

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


#Angle between project north and real north (in radians).
#final -1 "undoes" real to project north transformation.

angle = doc.ActiveProjectLocation.get_ProjectPosition(XYZ(0,0,0)).Angle * -1
walls = DB.FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
#doors = DB.FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
collwindows = DB.FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()
windows = []

new_walls = []
ori_x = []
ori_y = []
ExcludedWalls = []

print("Total walls in model: " + str(len(walls)))


NWalls = []
NEWalls = []
EWalls = []
SEWalls = []
SWalls = []
WWalls = []
SWWalls = []
NWWalls = []

WallSort = []
DirWall = []
WallSortBool = []
ex = []
AreaParam = BuiltInParameter.HOST_AREA_COMPUTED
WallArea = BuiltInParameter.SURFACE_AREA
HParam = BuiltInParameter.WINDOW_HEIGHT
WParam = BuiltInParameter.WINDOW_WIDTH
builtInParamType = BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS
total = []

NTotal = []
STotal = []
ETotal = []
WTotal = []
NETotal = []
NWTotal = []
SETotal = []
SWTotal = []

Nhosts = []
Shosts = []
Ehosts = []
Whosts = []
NEhosts = []
NWhosts = []
SEhosts = []
SWhosts = []


NWallArea = []
SWallArea = []
EWallArea = []
WWallArea = []
NEWallArea = []
NWWallArea = []
SEWallArea = []
SWWallArea = []

CPWall = []

# Used for filtering out model in place elements
for i in walls:
 	try:
 		WallSortBool.append(i.WallType.get_Parameter(BuiltInParameter.FUNCTION_PARAM).AsValueString() == "Exterior")
 		WallSort.append(i)
 	except:
 		ex.append(None)




for cw in collwindows:
	if str(GetWorkset(cw).Name) == "QAL_ENVELOPE":
		windows.append(cw)

for p in WallSort:
		if str(GetWorkset(p).Name) == "QAL_ENVELOPE":
			if (getattr(p, 'CurtainGrid', None) is not None) == True:
				CPWall.append(p)
			else:
				DirWall.append(p)

		
print(GetWorkset(p).Name)
print('Number of Curtain Walls: ' + str(len(CPWall)))

#DATA PROCESSING

new_CPwalls = []

#initial wall normals.

for wall in DirWall:
                try:
                                ori_x.append( round( wall.Orientation.Normalize().X , 4))
                                ori_y.append( round( wall.Orientation.Normalize().Y , 4))
                                new_walls.append(wall)
                except:
                                print("Could not obtain wall orientation.")
print("Exterior Walls: " + str(len(new_walls)))

CPori_x = []
CPori_y = []

for zz in CPWall:
                try:
                                CPori_x.append( round( zz.Orientation.Normalize().X , 4))
                                CPori_y.append( round( zz.Orientation.Normalize().Y , 4))
                                new_CPwalls.append(zz)
                except:
                                print("Could not obtain wall orientation.")

#normal transform (project to real north).
new_ori_x = list()
new_ori_y = list()
for x, y in zip(ori_x, ori_y):
                new_ori_x.append(project_to_real_north(x,y,angle)[0])
                new_ori_y.append(project_to_real_north(x,y,angle)[1])
				
new_CPori_x = list()
new_CPori_y = list()



#Invert curtain walls, b/c curtain...walls...
				
for x, y in zip(CPori_x, CPori_y):
                new_CPori_x.append(project_to_real_north(x,y,angle)[0] * -1)
                new_CPori_y.append(project_to_real_north(x,y,angle)[1] * -1)			

#final vector orientation assignment.
res = []
CPres = []
for x, y in zip (new_ori_x,new_ori_y):
                res.append(vector_orientation(x,y))
				
for x, y in zip (new_CPori_x,new_CPori_y):
                CPres.append(vector_orientation(x,y))

#print(CPres)
#DB WRITE

#transaction to write into DB.
t = Transaction(doc, "Wall Orientation")
t.Start()
for wall, dir in zip(new_walls,res):
                if wall.LookupParameter("Comments"):
                                try:
                                                wall.LookupParameter("Comments").Set(dir)
                                except:
                                                print("Could not write parameter in one of the walls.")
for zz, dir in zip(new_CPwalls,CPres):
                if zz.LookupParameter("Comments"):
                                try:
                                                zz.LookupParameter("Comments").Set(dir)
                                except:
                                                print("Could not write parameter in one of the walls.")

												
												
												
t.Commit()




    # get the type parameter

for n in DirWall:
		Comments = n.get_Parameter(builtInParamType)
		Area = n.get_Parameter(AreaParam)
		AreaCa = round((Area.AsDouble()) / 10.7639, 3)
		if Comments.AsString() == "North":
				NWalls.append(n)
				NWallArea.append(AreaCa)
		elif Comments.AsString() == "South":
				SWalls.append(n)
				SWallArea.append(AreaCa)
		elif Comments.AsString() == "East":
				EWalls.append(n)
				EWallArea.append(AreaCa)
		elif Comments.AsString() == "West":
				WWalls.append(n)
				WWallArea.append(AreaCa)
		elif Comments.AsString() == "Northeast":
				NEWalls.append(n)
				NEWallArea.append(AreaCa)
		elif Comments.AsString() == "Southeast":
				SEWalls.append(n)
				SEWallArea.append(AreaCa)
		elif Comments.AsString() == "Southwest":
				SWWalls.append(n)
				SWWallArea.append(AreaCa)
		elif Comments.AsString() == "Northwest":
				NWWalls.append(n)
				NWWallArea.append(AreaCa)


for nx in CPWall:
		Comments = nx.get_Parameter(builtInParamType)
		Area = nx.get_Parameter(AreaParam)
		AreaCa = round((Area.AsDouble()) / 10.7639, 3)
		if Comments.AsString() == "North":
				
				NTotal.append(AreaCa)
		elif Comments.AsString() == "South":
				
				STotal.append(AreaCa)
		elif Comments.AsString() == "East":
				
				ETotal.append(AreaCa)
		elif Comments.AsString() == "West":
				
				WTotal.append(AreaCa)
		elif Comments.AsString() == "Northeast":
				
				NETotal.append(AreaCa)
		elif Comments.AsString() == "Southeast":
				
				SETotal.append(AreaCa)
		elif Comments.AsString() == "Southwest":
				
				SWTotal.append(AreaCa)
		elif Comments.AsString() == "Northwest":
				
				NWTotal.append(AreaCa)


				
t2 = Transaction(doc, "Window Orientation")
t2.Start()
for h in windows:
	hosts = h.Host
	Comments = hosts.get_Parameter(builtInParamType)
	h.LookupParameter("Comments").Set(Comments.AsString())


t2.Commit()



for m in windows:
		Comments = m.get_Parameter(builtInParamType)
		WindowType = (m.Document.GetElement(m.GetTypeId()))
		Height = WindowType.get_Parameter(HParam)
		Width = WindowType.get_Parameter(WParam)

		if Comments.AsString() == "North":
				Nhosts.append(m)
				NTotal.append(round((Height.AsDouble() * Width.AsDouble()) / 10.7639, 3))
		elif Comments.AsString() == "South":
				Shosts.append(m)
				STotal.append(round((Height.AsDouble() * Width.AsDouble()) / 10.7639, 3))
		elif Comments.AsString() == "East":
				Ehosts.append(m)
				ETotal.append(round((Height.AsDouble() * Width.AsDouble()) / 10.7639, 3))
		elif Comments.AsString() == "West":
				Whosts.append(m)
				WTotal.append(round((Height.AsDouble() * Width.AsDouble()) / 10.7639, 3))
		elif Comments.AsString() == "Northeast":
				NEhosts.append(n)
				NETotal.append(round((Height.AsDouble() * Width.AsDouble()) / 10.7639, 3))
		elif Comments.AsString() == "Southeast":
				SEhosts.append(n)
				SETotal.append(round((Height.AsDouble() * Width.AsDouble()) / 10.7639, 3))
		elif Comments.AsString() == "Southwest":
				SWhosts.append(n)
				SWTotal.append(round((Height.AsDouble() * Width.AsDouble()) / 10.7639, 3))
		elif Comments.AsString() == "Northwest":
				NWhosts.append(n)
				NWTotal.append(round((Height.AsDouble() * Width.AsDouble()) / 10.7639, 3))


# get the type parameter


## Conditional in case a value = 00



try:
	(round((sum(NTotal)) / (sum(NWallArea)) + sum(NTotal)))
	print('----------------------------------')
	print('Total North Window Area: ' + str(sum(NTotal)) + ' sq.m.')
	print('Total North Wall Area ' + str((sum(NWallArea) + sum(NTotal))))
	print('North WWR ' + str(round((sum(NTotal) / (sum(NWallArea) + sum(NTotal)) * 100), 1)) + '%')
	print('----------------------------------')
except:
	print('North Elements Total to 0')

try:
	(round((sum(STotal)) / (sum(SWallArea)) + sum(STotal))) > 0
	print('----------------------------------')
	print('Total South Window Area: ' + str(sum(STotal)) + ' sq.m.')
	print('Total South Wall Area: ' + str((sum(SWallArea) + sum(STotal))))
	print('South WWR: ' + str(round((sum(STotal) / (sum(SWallArea) + sum(STotal)) * 100), 1)) + '%')
	print('----------------------------------')
except:
	print('South Elements Total to 0')

try:
	(round((sum(ETotal)) / (sum(EWallArea)) + sum(ETotal))) > 0	
	print('----------------------------------')
	print('Total East Window Area: ' + str(sum(ETotal)) + ' sq.m.')
	print('Total North Wall Area: ' + str((sum(EWallArea) + sum(ETotal))))
	print('East WWR: ' + str(round((sum(ETotal) / (sum(EWallArea) + sum(ETotal)) * 100), 1)) + '%')
	print('----------------------------------')
except:
	print('East Elements Total to 0')
	
try:
	(round((sum(WTotal)) / (sum(WWallArea)) + sum(WTotal))) > 0	
	print('----------------------------------')
	print('Total West Window Area: ' + str(sum(WTotal)) + ' sq.m.')
	print('Total West Wall Area: ' + str((sum(WWallArea) + sum(WTotal))))
	print('West WWR: ' + str(round((sum(WTotal) / (sum(WWallArea) + sum(WTotal)) * 100), 1)) + '%')
	print('----------------------------------')
except:
	print('West Elements Total to 0')
	
try:
	(round((sum(NETotal)) / (sum(NEWallArea)) + sum(NETotal)))
	print('----------------------------------')
	print('Total Northeast Window Area: ' + str(sum(NETotal)) + ' sq.m.')
	print('Total Northeast Wall Area ' + str((sum(NEWallArea) + sum(NETotal))))
	print('Northeast WWR ' + str(round((sum(NETotal) / (sum(NEWallArea) + sum(NETotal)) * 100), 1)) + '%')
	print('----------------------------------')
except:
	print('Northeast Elements Total to 0')
	
try:
	(round((sum(SETotal)) / (sum(SEWallArea)) + sum(SETotal))) > 0
	print('----------------------------------')
	print('Total Southeast Window Area: ' + str(sum(SEotal)) + ' sq.m.')
	print('Total Southeast Wall Area: ' + str((sum(SEWallArea) + sum(SETotal))))
	print('Southeast WWR: ' + str(round((sum(SETotal) / (sum(SEWallArea) + sum(SETotal)) * 100), 1)) + '%')
	print('----------------------------------')
except:
	print('Southeast Elements Total to 0')

try:
	(round((sum(SWTotal)) / (sum(SWWallArea)) + sum(SWTotal))) > 0
	print('----------------------------------')
	print('Total Southwest Window Area: ' + str(sum(SWTotal)) + ' sq.m.')
	print('Total Southwest Wall Area: ' + str((sum(SWWallArea) + sum(SWTotal))))
	print('South WWR: ' + str(round((sum(SWTotal) / (sum(SWWallArea) + sum(SWTotal)) * 100), 1)) + '%')
	print('----------------------------------')
except:
	print('Southwest Elements Total to 0')
	
try:
	(round((sum(NWTotal)) / (sum(NWWallArea)) + sum(NWTotal)))
	print('----------------------------------')
	print('Total Northwest Window Area: ' + str(sum(NTotal)) + ' sq.m.')
	print('Total Northwest Wall Area ' + str((sum(NWWallArea) + sum(NWTotal))))
	print('North WWR ' + str(round((sum(NWTotal) / (sum(NWWallArea) + sum(NWTotal)) * 100), 1)) + '%')
	print('----------------------------------')
except:
	print('Northwest Elements Total to 0')
	

print('North Openings: ' + str(len(Nhosts)))
print('South Openings: ' + str(len(Shosts)))
print('East Openings: ' + str(len(Ehosts)))
print('West Openings: ' + str(len(Whosts)))


#reporting time
print('----------------------------------')
print("Number of North Facing Walls: " + str(len(NWalls)))
print("Number of South Facing Walls: " + str(len(SWalls)))
print("Number of East Facing Walls: " + str(len(EWalls)))
print("Number of West Facing Walls: " + str(len(WWalls)))
print("Number of Northeast Facing Walls: " + str(len(NEWalls)))
print("Number of Southeast Facing Walls: " + str(len(SEWalls)))
print("Number of Southwest Facing Walls: " + str(len(SWWalls)))
print("Number of Northwest Facing Walls: " + str(len(NWWalls)))
print('----------------------------------')
print("Total Number of Windows: " + str(len(windows)))


output = script.get_output()
output.set_width(900)
chart = output.make_bar_chart()



chart.data.labels = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']

WallsChart = chart.data.new_dataset('Wall Total')
WallsChart.data = [100, 100, 100, 100, 100, 100, 100, 100]
WallsChart.set_color(233, 30, 99, 0.3)

try:
	NChart = round((sum(NTotal) / (sum(NWallArea) + sum(NTotal)) * 100), 1)
except:
	NChart= 0

try:	
	SChart = round((sum(STotal) / (sum(SWallArea) + sum(STotal)) * 100), 1)
except:
	SChart = 0

try:	
	EChart = round((sum(ETotal) / (sum(EWallArea) + sum(ETotal)) * 100), 1)
except:
	EChart = 0

try:
	WChart = round((sum(WTotal) / (sum(WWallArea) + sum(WTotal)) * 100), 1)
except:
	WChart = 0

try:
	NEChart = round((sum(NETotal) / (sum(NEWallArea) + sum(NETotal)) * 100), 1)
except:
	NEChart = 0
try:
	SEChart = round((sum(SETotal) / (sum(SEWallArea) + sum(SETotal)) * 100), 1)
except:
	SEChart = 0
try:
	SWChart = round((sum(SWTotal) / (sum(SWWallArea) + sum(SWTotal)) * 100), 1)
except:
	SWChart = 0 

try:
	NWChart = round((sum(NWTotal) / (sum(NWWallArea) + sum(NWTotal)) * 100), 1)
except:
	NWChart = 0

WindowsChart = chart.data.new_dataset('Window Openings')
WindowsChart.data = [NChart, NEChart, EChart, SEChart, SChart, SWChart, WChart, NWChart]
WindowsChart.set_color(3, 169, 244, 0.6)

#FortyMark = chart.data.new_dataset('40% Mark')
#FortyMark.data = [(((sum(NWallArea)) + (sum(NTotal))) * .4), (((sum(NEWallArea)) + (sum(NETotal))) * .4)]
#FortyMark.set_color(51, 255, 54, 0.7)

#chart.randomize_colors()
chart.draw()



#print("Total Number of Doors: " + str(len(doors)))
endtime ="It took me: " + str(timer.get_time()) + " seconds to perform this task."
print(endtime)
