from Autodesk.Revit.DB import *
import clr

clr.AddReference("RevitNodes")
import Revit

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

doc = __revit__.ActiveUIDocument.Document

stairs_collector = FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_Stairs). \
    WhereElementIsNotElementType(). \
    ToElements()
runs_collector = FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_StairsRuns). \
    WhereElementIsNotElementType(). \
    ToElements()


def IsRailingAssociatedWithRun(railing_element, runs_element):
    # Get the bounding boxes of the railing and the run
    railing_bb = railing_element.get_BoundingBox(None)
    run_bb = runs_element.get_BoundingBox(None)
    # Extract the min and max points of the outlines
    railing_min = railing_bb.Min
    railing_max = railing_bb.Max
    run_min = run_bb.Min
    run_max = run_bb.Max

    # Check if the outlines intersect by comparing the min and max points
    if (railing_min.X <= run_max.X and railing_max.X >= run_min.X and
        railing_min.Y <= run_max.Y and railing_max.Y >= run_min.Y and
        railing_min.Z <= run_max.Z and railing_max.Z >= run_min.Z):

        return True
    else:
        return False

transaction = Transaction(doc, 'Set coating marble values')
transaction.Start()
for el in stairs_collector:
    #get runs
    associated_railings = el.GetAssociatedRailings()
    runs = el.GetStairsRuns()

    #getting parameters from stairs
    coatingMarble_param = el.LookupParameter("CoatingMarble")
    LineForBlindPeople_param = el.LookupParameter("LineForBlindPeople")
    PanelStairs_param = el.LookupParameter("PanelStairs")
    actualNumberOfRises = el.LookupParameter("Actual Number of Risers").AsInteger()

    #initial variables
    coatingMarbleResult = 0.0
    blindLineLength = 0 
    lengthPanel = 0
    r_depth = 0
    r_height = 0
    count = 0 
    for r in runs:
        runs_element = doc.GetElement(r)

        #getting run_width
        runs_width = runs_element.ActualRunWidth * 0.3048
        #params of rises and treads
        runs_actualNumberOfRises = runs_element.LookupParameter("Actual Number of Risers").AsInteger()
        runs_actualNumberOfTreads = runs_element.LookupParameter("Actual Number of Treads").AsInteger()
        #marble for run 
        coatingMarbleResult += (runs_width * runs_actualNumberOfRises)
        #getting run params
        r_depth = runs_element.LookupParameter("Actual Tread Depth").AsDouble() * 0.3048
        r_height = runs_element.LookupParameter("Actual Riser Height").AsDouble() * 0.3048
        # blinde line for run
        blindLineLength += (runs_width * 2)
        
        #checking if reiling that we need exist, and if so we calculating lengthPanel for this run
        for railing in associated_railings:    
            railing_element = doc.GetElement(railing)
            if "on Wall" in railing_element.Name and IsRailingAssociatedWithRun(railing_element, runs_element):
                lengthPanel += (r_depth * runs_actualNumberOfTreads) + (r_height * runs_actualNumberOfRises)
                count += 1


    coatingMarble_param.Set(coatingMarbleResult / 0.3048)
    PanelStairs_param.Set((lengthPanel) / 0.3048)
    LineForBlindPeople_param.Set((blindLineLength) / 0.3048)


transaction.Commit()