import clr
from Autodesk.Revit.DB import *
import random

clr.AddReference("RevitAPI")
clr.AddReference("System")

doc = __revit__.ActiveUIDocument.Document

walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls). \
    WhereElementIsNotElementType(). \
    ToElements()

transaction = Transaction(doc, "Change TypeID elements")
transaction.Start()

IdsToChange = []

for wall in walls:
    # Get the current TypeId of the wall

    current_type_id = wall.GetTypeId()
    print('current type id is: {0}'.format(current_type_id))
    # Create a new TypeId (random in this example)
    new_type_id = ElementId(random.randint(100000, 999999))
    print('new_type_id is : {0}'.format(new_type_id))

    # Change the TypeId of the wall
    wall.ChangeTypeId(new_type_id)

    # Append the wall's Id to the list for reference
    # IdsToChange.append(wall.Id)

transaction.Commit()
print(IdsToChange)
print("Type IDs changed for the following wall elements:")
for wall_id in IdsToChange:
    print(wall_id)