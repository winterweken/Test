#IMPORTS

#for timing
from pyrevit.coreutils import Timer
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

#function that assigns an orientation to a 2D vector according to the Spanish CTE compass rose.
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

#get workset neames
def GetWorkset(itemx):
	if hasattr(itemx, "WorksetId"): return itemx.Document.GetWorksetTable().GetWorkset(itemx.WorksetId)
	else: return None


#VARIABLES

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#Angle between project north and real north (in radians).
#final -1 "undoes" real to project north transformation.
#Modify collector for exterior walls only
angle = doc.ActiveProjectLocation.get_ProjectPosition(XYZ(0,0,0)).Angle * -1
walls = DB.FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
doors = DB.FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
windows = DB.FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()

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


# Used for filtering out model in place elements
for i in walls:
 	try:
 		WallSortBool.append(i.WallType.get_Parameter(BuiltInParameter.FUNCTION_PARAM).AsValueString() == "Exterior")
 		WallSort.append(i)
 	except:
 		ex.append(None)


# ### Old
# ###
# for s in WallSort:
# 	if s.WallType.get_Parameter(BuiltInParameter.FUNCTION_PARAM).AsValueString() == "Exterior":
# 			DirWall.append(s)



for p in WallSort:
    if str(GetWorkset(p).Name) == "Hello":
        DirWall.append(p)

print(GetWorkset(p).Name)


		#DATA PROCESSING

#print(p)


#initial wall normals.

for wall in DirWall:
                try:
                                ori_x.append( round( wall.Orientation.Normalize().X , 4))
                                ori_y.append( round( wall.Orientation.Normalize().Y , 4))
                                new_walls.append(wall)
                except:
                                print("Could not obtain wall orientation.")
print("Exterior Walls: " + str(len(new_walls)))

#normal transform (project to real north).
new_ori_x = list()
new_ori_y = list()
for x, y in zip(ori_x, ori_y):
                new_ori_x.append(project_to_real_north(x,y,angle)[0])
                new_ori_y.append(project_to_real_north(x,y,angle)[1])

#final vector orientation assignment.
res = []
for x, y in zip (new_ori_x,new_ori_y):
                res.append(vector_orientation(x,y))


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
t.Commit()




#print(wall.LookupParameter("Comments").AsString)


#Sort processed walls

builtInParamType = BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS
    # get the type parameter

for n in DirWall:
		Comments = n.get_Parameter(builtInParamType)
		if Comments.AsString() == "North":
				NWalls.append(n)
		elif Comments.AsString() == "South":
				SWalls.append(n)
		elif Comments.AsString() == "East":
				EWalls.append(n)
		elif Comments.AsString() == "East":
				EWalls.append(n)
		elif Comments.AsString() == "Northeast":
				NEWalls.append(n)
		elif Comments.AsString() == "Southeast":
				SEWalls.append(n)
		elif Comments.AsString() == "Southwest":
				SWWalls.append(n)
		elif Comments.AsString() == "Northwest":
				NWWalls.append(n)

Nhosts = []
Shost = []
Ehost = []
Whost = []

for h in windows:
	hosts = h.Host
	Comments = hosts.get_Parameter(builtInParamType)
	if Comments.AsString() == "North":
				Nhosts.append(h)

print('North Hosts: ' + str(len(Nhosts)))

#reporting time

print("Number of North Facing Walls: " + str(len(NWalls)))
print("Number of South Facing Walls: " + str(len(SWalls)))
print("Number of East Facing Walls: " + str(len(EWalls)))
print("Number of West Facing Walls: " + str(len(WWalls)))
print("Number of Northeast Facing Walls: " + str(len(NEWalls)))
print("Number of Southeast Facing Walls: " + str(len(SEWalls)))
print("Number of Southwest Facing Walls: " + str(len(SWWalls)))
print("Number of Northwest Facing Walls: " + str(len(NWWalls)))

print("Total Number of Windows: " + str(len(windows)))
print("Total Number of Doors: " + str(len(doors)))
endtime ="It took me: " + str(timer.get_time()) + " seconds to perform this task."
print(endtime)
