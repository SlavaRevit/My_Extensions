import sys
import os
import clr
import sys

import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit import script

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
                    "STR_Concrete_Sloped", "STR_Concrete_protection", "STR_Air_Pergola_Aluminium"]


def check_element(material_name, list_to_pass):
    for el in list_to_pass:
        if el == material_name:
            return True


def get_element_params(element):
    element_id = element.GetTypeId()
    element_type = doc.GetElement(element_id)
    element_name = element.Name
    element_level_param = element.LookupParameter("Level").AsValueString()
    element_area = element.LookupParameter("Area").AsDouble() * 0.09290304
    element_duplication_typemark = element_type.LookupParameter("Duplication Type Mark").AsString()
    try:
        element_material = element.GetMaterialIds(False)
        material_id = element_material[0]
        material = doc.GetElement(material_id)
        material_element_name = material.Name
    except TypeError as err:
        print(err)

    return element_level_param, element_area, material_element_name, element_name, element_duplication_typemark


def check_if_element_not_equal_to(param_to_check, level_name, dict, element_area, element_name, elevations_level):
    if level_name not in dict:
        dict[level_name] = {param_to_check: element_area, "Elements name": "\n" + element_name,
                            "Elevation": elevations_level}
    else:
        if param_to_check not in dict[level_name]:
            dict[level_name][param_to_check] = element_area
        else:
            dict[level_name][param_to_check] += element_area
            if element_name in dict[level_name]['Elements name']:
                pass
            else:
                dict[level_name]['Elements name'] += "\n" + element_name


total_check = {}
elevations = []
area_of_total_check = {}
for level in levels:
    level_name = level.Name
    elevations_level = level.Elevation * 30.48

    for floor in floors:
        # getting all necessary parameters for checking
        floor_level_param, floor_area, material_name, floor_name, floor_dupl_mark = get_element_params(floor)
        if "STR_" in material_name and level_name == floor_level_param:
            if check_element(material_name, elements_to_pass):
                pass
            elif floor_level_param == level_name:
                if material_name == 'STR_Air_Total_Area' or material_name == 'STR_Air_Total_Area_Dn' or material_name == "STR_Air_Total_Area_Commercial" \
                        or material_name == "STR_Air_Double_Level":
                    total_area = floor_area
                    if level_name not in total_check:
                        total_check[level_name] = {'area': 0, 'total': total_area, 'floor name': ""}
                    else:
                        if 'total' not in total_check[level_name]:
                            total_check[level_name]['total'] = total_area
                        else:
                            total_check[level_name]['total'] += total_area
                else:
                    check_if_element_not_equal_to("area", level_name, total_check, floor_area, floor_name,
                                                  elevations_level)

    for found in foundations:
        # getting all necessary parameters for checking
        found_level_param, found_area, material_of_found, found_name, fond_duplication_type_mark = get_element_params(
            found)

        if "STR_" in material_of_found and fond_duplication_type_mark == "Bisus" or fond_duplication_type_mark == "Dipun" \
                or fond_duplication_type_mark == "Head":
            pass
        elif "STR_" in material_of_found and level_name == found_level_param:
            if found_level_param == level_name:
                if level_name not in total_check:
                    total_check[level_name] = {'area': found_area, "floor name": "\n" + found_name}
                else:
                    check_if_element_not_equal_to("area", level_name, total_check, found_area, found_name,
                                                  elevations_level)


def by_level_name(elem):
    try:
        elevation_level = elem[1].get("Elevation")
        sort_by = elevation_level
        return sort_by
    except:
        pass


sorted_total_check = sorted(total_check.items(), key=by_level_name, reverse=False)

output = script.get_output()

data = []
for el in sorted_total_check:
    type_of_floors_list = []
    name_of_level = el[0]
    area = el[1].get('area', 0)
    total = el[1].get('total', 0)

    difference = total - area
    try:
        in_percent = ((area - total) / total) * 100
    except ZeroDivisionError:
        in_percent = "No Total "

    type_of_floors = el[1].get('Elements name', "don't have")
    type_of_floors_list.append(type_of_floors)
    cleaned_list = [item.replace('\n', ',') for item in type_of_floors_list]
    cleaned_list[0] = cleaned_list[0].lstrip(',')
    data.append([name_of_level, area, total, difference, in_percent, cleaned_list])
try:
    output.print_table(table_data=data,
                       title="Check Total Area to Area of floors + airs",
                       columns=["Level name", "Area", "Total Area", "Difference", "in Percentage", "Type of floors:"],
                       formats=["", "", "", "", "{}%", ""]
                       )
except:
    print("No data.")
