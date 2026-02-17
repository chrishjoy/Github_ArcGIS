# Fresno half-mile buffer — Notes and how it works

## Overview
This document summarizes the steps and key code I used to create a 0.5-mile buffer around Fresno County from a counties shapefile and add the result into your ArcGIS Pro project geodatabase. The notes are written for someone learning ArcPy and want to understand what was done and why.

## Files created or modified
- `forFun.py` — contains `buffer_fresno()` (the ArcPy function that selects Fresno and creates the buffer).
- `run_buffer2.py` — runner script that executes `buffer_fresno()` and writes the buffer into the project geodatabase.
- `run_only_add_layer.py` — small helper that adds the saved buffer feature class into the specified APRX and saves it.
- `run_add_to_aprx.py`, `run_buffer.py` — other runner variants created during testing.
- Output feature class (in your project geodatabase):
  - `C:\Users\cschm\OneDrive\Documents\ArcGIS\Projects\GEOG483_Lesson6\GEOG483_Lesson6.gdb\Fresno_halfmile_buffer`

## High-level steps performed
1. Read the counties shapefile (path: `C:\PSUGIS\GEOG483\Lesson6\Lesson6\Lesson6_data\CA_Counties.shp`).
2. Make a temporary feature layer from the shapefile so it can be queried and selected.
3. Select the record where the `NAME` field equals `Fresno`.
4. Create a buffer of `0.5 Miles` around that selected feature; dissolve the buffer so the output is a single polygon.
5. Save the buffer as a feature class in your project geodatabase (`GEOG483_Lesson6.gdb`).
6. Add the new feature class to your APRX (ArcGIS Pro project) and save the APRX (done after you closed the APRX to avoid locking problems).

## Key ArcPy concepts used (plain language)
- `arcpy.management.MakeFeatureLayer`: creates an in-memory layer from a feature class or shapefile. Useful for selecting records with SQL and operating on just that selection.
- `arcpy.AddFieldDelimiters`: formats field names safely for SQL queries depending on data source.
- `arcpy.management.SelectLayerByAttribute`: selects features in a layer using SQL (e.g., `NAME = 'Fresno'`).
- `arcpy.management.GetCount`: returns how many features are currently in the layer/selection.
- `arcpy.analysis.Buffer`: creates buffer polygons at a given distance around features. The `dissolve_option='ALL'` parameter merges individual buffers into one polygon if needed.
- `arcpy.mp.ArcGISProject`: used to open an ArcGIS Pro project (`.aprx`) and manipulate maps and layers programmatically; `addDataFromPath()` adds a layer to a map.
- `arcpy.env.overwriteOutput = True`: allows outputs to be overwritten if the same path already exists.

## Most important code (simplified)
```python
import arcpy

def buffer_fresno(shapefile, out_path, buffer_distance='0.5 Miles', field_name='NAME', target_name='Fresno'):
    arcpy.env.overwriteOutput = True
    arcpy.management.MakeFeatureLayer(shapefile, 'counties_lyr')
    field_delimited = arcpy.AddFieldDelimiters(shapefile, field_name)
    where = f"{field_delimited} = '{target_name}'"
    arcpy.management.SelectLayerByAttribute('counties_lyr', 'NEW_SELECTION', where)
    arcpy.analysis.Buffer('counties_lyr', out_path, buffer_distance, dissolve_option='ALL')
```

And to add the resulting feature class to an APRX:
```python
from arcpy.mp import ArcGISProject
aprx = ArcGISProject(r'C:\path\to\project.aprx')
first_map = aprx.listMaps()[0]
first_map.addDataFromPath(r'C:\path\to\gdb.gdb\Fresno_halfmile_buffer')
aprx.save()
```

## How I ran the script (important practical notes)
- ArcPy is installed with ArcGIS Pro and must be run with the ArcGIS Pro Python interpreter. In your environment that executable was:

```
C:/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe
```

- Example command (PowerShell) I used to run the runner script:

```powershell
& "C:/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" "c:\Users\cschm\Python_practice\run_buffer2.py"
```

- Running code that modifies an APRX requires the APRX file not be open in ArcGIS Pro (the file is locked when the project is open). If you try to add a layer while the APRX is open, you'll get an error. Close ArcGIS Pro, then run the script, or use `add_to_project=False` and add the layer manually from the Catalog pane.

## Coordinate systems and distance units (very important)
- Buffer distances like `0.5 Miles` are interpreted in the coordinate system of the data. If your counties shapefile is in a geographic coordinate system (latitude/longitude, units degrees), specifying `Miles` will cause ArcPy to project on-the-fly but results may be inaccurate.
- Best practice: use a projected coordinate system appropriate for the area (for California, use an appropriate State Plane or UTM zone) so buffer distances are accurate.
- If needed, reproject your input or run the buffer using the `geoprocessing` tool's `geodesic` parameter if you want true geodesic buffering.

## Troubleshooting tips (things I can't fix remotely)
- File not found errors: confirm the shapefile path exists and is accessible.
- APRX locked / cannot add layer: close ArcGIS Pro (the project) and re-run the add script; or add the layer manually from Catalog.
- Permission errors saving to OneDrive/GDB: ensure you have write permission; OneDrive sometimes locks files — try saving to a local folder or ensure OneDrive sync isn't blocking writes.
- Wrong buffer size: check the input CRS and reproject if necessary.

## Next steps and styling suggestions (quick)
- Apply a semi-transparent fill and a colored outline to the buffer to make it stand out (e.g., 40% opacity fill, 2px outline).
- Use `arcpy.mp` to programmatically change symbology, or create a `.lyrx` template (layer file) and add it to the map.
- If your workflow repeats, wrap the code to accept arguments (shapefile path, county name, buffer distance, output gdb) so it's reusable.

## Useful learning resources
- ArcGIS Pro / ArcPy documentation (Esri): https://pro.arcgis.com
- ArcPy mapping (`arcpy.mp`) guide for automating ArcGIS Pro projects
- ArcGIS Python API vs ArcPy: ArcPy is the desktop/geoprocessing library included with ArcGIS Pro for working with local data and tools; the ArcGIS Python API focuses on web/GIS server workflows.

---
If you'd like, I can now:
- apply a recommended symbology to the `Fresno_halfmile_buffer` layer programmatically, or
- export a `.lyrx` symbology file you can reuse or drag into other projects.

Tell me which and I'll proceed.