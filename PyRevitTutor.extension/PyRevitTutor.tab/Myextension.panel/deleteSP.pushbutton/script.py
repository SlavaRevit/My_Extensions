import clr
from Autodesk.Revit.DB import *



clr.AddReference("RevitAPI")
clr.AddReference("System")

doc = __revit__.ActiveUIDocument.Document
transaction = Transaction(doc, "Delete Global Parameters")
transaction.Start()

global_params = list(FilteredElementCollector(doc).OfClass(GlobalParameter))


elements_to_delete = []

for param in global_params:
    elements_to_delete.append(param.Id)

for element_id in elements_to_delete:
    doc.Delete(element_id)

transaction.Commit()