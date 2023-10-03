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

    act_Result = 0.0
    # result = []
    for r in runs:
        runs_element = doc.GetElement(r)
        runs_width = runs_element.ActualRunWidth * 0.3048
        runs_actualNumberOfRises = runs_element.LookupParameter("Actual Number of Risers").AsInteger()
        act_Result += (runs_width * runs_actualNumberOfRises)

    coatingMarble_param.Set(act_Result / 30.48)

transaction.Commit()

# for railing in associated_railings:
#     railing_element = doc.GetElement(railing)
#     print(railing_element.Name)

# number_stairs = stairs_collector[0].LookupParameter("ActualRisersNumber")
# coatingMarble_param.Set(width_Run * number_stairs)
