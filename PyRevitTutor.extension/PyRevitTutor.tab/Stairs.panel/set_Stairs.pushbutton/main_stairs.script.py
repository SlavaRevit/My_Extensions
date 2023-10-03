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

transaction = Transaction(doc, 'Set coating marble values')
transaction.Start()
for el in stairs_collector:
    associated_railings = el.GetAssociatedRailings()
    runs = el.GetStairsRuns()
    coatingMarble_param = el.LookupParameter("CoatingMarble")
    LineForBlindPeople_param = el.LookupParameter("LineForBlindPeople")
    PanelStairs_param = el.LookupParameter("PanelStairs")
    actualNumberOfRises = el.LookupParameter("Actual Number of Risers").AsInteger()

    #setting Coating marble
    act_Result = 0.0
    lengthPanel = 0
    count_runs = 0
    blindLineLength = 0 
    for r in runs:
        count_runs += 2
        runs_element = doc.GetElement(r)
        runs_width = runs_element.ActualRunWidth * 0.3048
        runs_actualNumberOfRises = runs_element.LookupParameter("Actual Number of Risers").AsInteger()
        riser_width = // need to get this param
        riser_height = // need to get this param (how it called in Revit)
        lengthPanel = ((riser_width + riser_height) * runs_actualNumberOfRises)  
        act_Result += (runs_width * runs_actualNumberOfRises)
        blindLineLength += (runs_width * count_runs) * 2

    
    coatingMarble_param.Set(act_Result / 30.48)
    
    #setting Panel stairs
    count = 0
    for railing in associated_railings:
        railing_element = doc.GetElement(railing)
        if "Home" or "Stairway" in railing_element.Name:
            count += 1
            print(railing_element.Name)
    PanelStairs_param.Set(lengthPanel * count)
    

     





transaction.Commit()