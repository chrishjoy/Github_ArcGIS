<!--
To see this Markdown file in Preview mode

ctrl + shift + v
-->
# Using the AI assistant in VS Code for ArcGIS tasks

This short guide explains how to use the AI tool in VS Code to automate ArcGIS/ArcPy tasks (what to provide, how to prompt, and practical tips).

## Where to find the AI tool
- The AI is available inside your VS Code workspace (the assistant operates on files in the workspace root).
- Place scripts and data paths inside the workspace so the assistant can read and edit them.

## What to provide when asking for ArcGIS work
Always include:
- Exact file paths (use full absolute paths on Windows, e.g. `C:\PSUGIS\...\CA_Counties.shp`).
- APRX path if you want the script to modify a specific project: `C:\Users\...\MyProject.aprx`.
- Output target (shapefile or geodatabase): e.g. `C:\...\MyProject.gdb\OutputName`.
- The field name and value used for selection (e.g. `field_name='NAME', value='Fresno'`).
- Coordinate system expectations or note if reprojection is needed.

Optional helpful info:
- Whether the APRX will be open while the script runs (close it when possible).
- Desired buffer distance and units (e.g. `0.5 Miles`) and whether you want geodesic buffering.
- Whether to add resulting layers to the project (`add_to_project=True`) or just write to disk.

## How to prompt the AI (examples)
- Task-oriented: "Create a 0.5-mile buffer around Fresno from this shapefile (path: ...), save to this geodatabase (path: ...), and add to APRX (path: ...)."
- Code-editing: "Edit `forFun.py` to add a function that selects `NAME='Fresno'` and buffers it by 0.5 miles; test runner should save into `GEOG483_Lesson6.gdb`."
- Troubleshooting: "I get a locking error when adding a layer to the APRX — make sure the script handles APRX locks and provides clear guidance." 

## What the assistant will (and won't) do
- Will: create/edit Python files, run scripts using the configured ArcGIS Pro Python interpreter, write outputs into specified geodatabases, and add layers to APRX if the project file is not locked.
- Won't: access external servers/accounts or change system settings without explicit user commands.

## How the assistant runs scripts safely
- It uses the ArcGIS Pro Python executable in the workspace environment (e.g. `C:/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe`).
- It will ask you to close ArcGIS Pro before modifying an APRX if needed.

## Quick checklist for smooth runs
- Confirm the shapefile / GDB paths exist and are readable/writable.
- Close ArcGIS Pro when a script needs to modify or save the APRX.
- Ensure you have write permissions for OneDrive or GDB locations.
- Prefer writing outputs into a geodatabase (`.gdb`) when planning to add into an APRX.
- Provide desired coordinate system guidance if accurate distances are required.

## Example one-line command the assistant may run (PowerShell)
```powershell
& "C:/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" "c:\Users\cschm\Python_practice\run_buffer2.py"
```

## Troubleshooting tips the assistant will suggest
- "FileNotFoundError": verify path spelling and existence.
- APRX locked: close ArcGIS Pro and re-run the add-to-aprx step.
- Wrong buffer size: check CRS and reproject to a suitable projected CRS.
- OneDrive or permissions issues: try a local folder or pause OneDrive sync.

## Best practices for prompts
- Provide concrete outputs and exact paths.
- Say whether you want the assistant to also run the script or only generate code.
- Ask for an explanation if a change is unclear; the assistant can annotate and document.

## Example prompt template you can copy
> "Edit `forFun.py` to add a function `buffer_county(shapefile, gdb_out, county_field, county_name, distance)` that selects `county_name` from `county_field`, creates a buffer `distance`, saves to `gdb_out`, and optionally adds to an APRX at `aprx_path`. Then run it and save the output to `C:\Users\...\GEOG483_Lesson6.gdb\MyBuffer`."

## Want a layer symbology or `.lyrx` file?
- Mention the style (fill color, opacity, outline width) and the assistant can apply programmatic symbology changes or create a `.lyrx` you can import.

---