
import clr
import sys

import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

doc = __revit__.ActiveUIDocument.Document
__highlight__ = "new"
floors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors). \
    WhereElementIsNotElementType(). \
    ToElements()


levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels). \
    WhereElementIsNotElementType(). \
    ToElements()


foundations = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFoundation). \
    WhereElementIsNotElementType().ToElements()


elements_to_pass = ["STR_Concrete_Slab_Stairways", "STR_Air_Pergola_Wood", "STR_Air_Total_Area_Pergola",
                    "STR_Aggregate",
                    'STR_Backfilling', 'STR_Concrete_Lite_Beton', 'STR_Concrete_Sidewalk', "STR_CLSM",
                    "STR_Concrete_Koteret",
                    "STR_Concrete_Topping", "STR_Polivid", "STR_Steel_Stairs_Landing", "STR_Geoplast",
                    "STR_Concrete_Sloped", "STR_Concrete_protection"]


def check_element(material_name, list_to_pass):
    for el in list_to_pass:
        if el == material_name:
            return True

total_check = {}
area_of_total_check = {}
for level in levels:
    level_name = level.Name
    for floor in floors:
        floor_id = floor.GetTypeId()
        floor_type = doc.GetElement(floor_id)
        floor_type_valid = floor.GetType()

        # getting parameters
        floor_level_param = floor.LookupParameter("Level").AsValueString()
        floor_area = floor.LookupParameter("Area").AsDouble() * 0.09290304

        # getting material name
        material_of_floor = floor.GetMaterialIds(False)

        material_id = material_of_floor[0]
        material = doc.GetElement(material_id)
        material_name = material.Name

        if "STR_" in material_name and level_name == floor_level_param:
            if check_element(material_name, elements_to_pass):
                pass
            elif floor_level_param == level_name:
                if material_name == 'STR_Air_Total_Area' or material_name == 'STR_Air_Total_Area_Dn':
                    total_area = floor_area
                    if level_name not in total_check:
                        total_check[level_name] = {'area': 0, 'total': total_area, 'floor name': ""}
                    else:
                        if 'total' not in total_check[level_name]:
                            total_check[level_name]['total'] = total_area
                        else:
                            total_check[level_name]['total'] += total_area
                else:
                    if level_name not in total_check:
                        total_check[level_name] = {'area': floor_area, "floor name": "\n" + floor.Name}
                    else:
                        if 'area' not in total_check[level_name]:
                            total_check[level_name]['area'] = floor_area

                        else:
                            total_check[level_name]['area'] += floor_area
                            if floor.Name in total_check[level_name]['floor name']:
                                pass
                            else:
                                total_check[level_name]['floor name'] += "\n" + floor.Name

    for found in foundations:
        found_id = found.GetTypeId()
        found_type = doc.GetElement(found_id)
        found_level_param = found.LookupParameter("Level").AsValueString()
        found_area = found.LookupParameter("Area").AsDouble() * 0.09290304
        dupl_type_mark = found_type.LookupParameter("Duplication Type Mark").AsString()
        # getting material name
        material_of_found = found.GetMaterialIds(False)

        material_id = material_of_found[0]
        material = doc.GetElement(material_id)
        material_name = material.Name
        if "STR_" in material_name and dupl_type_mark == "Bisus" or dupl_type_mark == "Dipun":
            pass
        elif "STR_" in material_name and level_name == found_level_param:
            if found_level_param == level_name:
                if level_name not in total_check:
                    total_check[level_name] = {'area': found_area, "floor name": "\n" + found.Name}
                else:
                    if 'area' not in total_check[level_name]:
                        total_check[level_name]['area'] = found_area
                    else:
                        total_check[level_name]['area'] += found_area
                        if found.Name in total_check[level_name]['floor name']:
                            pass
                        else:
                            total_check[level_name]['floor name'] += "\n" + found.Name


def by_level_name(elem):
    sort_by = elem[0].split(" ")
    return int(sort_by[1])


# sorted_total_check = sorted(total_check.items(), key=by_level_name, reverse=False)
sorted_total_check = sorted(total_check.items())
# print(sorted_total_check)

for el in sorted_total_check:
    area = el[1].get('area', 0)
    total = el[1].get('total', 0)
    type_of_floor = el[1].get('floor name', "don't have")
    print("{0}, Area: {1} / Total_Area: {2} / Difference is: {3} / Type of Floors: {4}".format(el[0], area, total,
                                                                                               (total - area),
                                                                                               type_of_floor))
