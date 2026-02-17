import arcpy
import os

def buffer_fresno(shapefile=r"C:\PSUGIS\GEOG483\Lesson6\Lesson6\Lesson6_data\CA_Counties.shp",
				  out_path=None,
				  buffer_distance="0.5 Miles",
				  field_name="NAME",
				  target_name="Fresno",
				  add_to_project=False,
				  aprx_path=None):
	"""Create a half-mile buffer around Fresno county from a counties shapefile.

	Args:
		shapefile (str): Path to the counties shapefile.
		out_path (str|None): Output path for the buffer feature class/shapefile. If None, a shapefile
			named 'Fresno_halfmile_buffer.shp' will be created in the same folder as the input.
		buffer_distance (str): Buffer distance string compatible with ArcPy (e.g. '0.5 Miles').
		field_name (str): Field used to find Fresno (default 'NAME').
		target_name (str): Value in `field_name` to select (default 'Fresno').
		add_to_project (bool): If True, attempt to add the output to the open ArcGIS Pro project ('CURRENT').
		aprx_path (str|None): If provided and `add_to_project` is True, open this APRX instead of 'CURRENT'.

	Returns:
		str: Path to the created buffer feature class/shapefile, or None if nothing created.
	"""
	arcpy.env.overwriteOutput = True

	if not os.path.exists(shapefile):
		raise FileNotFoundError(f"Shapefile not found: {shapefile}")

	if out_path is None:
		out_dir = os.path.dirname(shapefile)
		out_path = os.path.join(out_dir, "Fresno_halfmile_buffer.shp")

	layer_name = "counties_lyr"
	try:
		arcpy.management.MakeFeatureLayer(shapefile, layer_name)
		# Build a safe SQL where clause using AddFieldDelimiters
		field_delimited = arcpy.AddFieldDelimiters(shapefile, field_name)
		where = f"{field_delimited} = '{target_name}'"
		arcpy.management.SelectLayerByAttribute(layer_name, "NEW_SELECTION", where)

		count = int(arcpy.management.GetCount(layer_name).getOutput(0))
		if count == 0:
			print(f"No features selected for {target_name} using {field_name}.")
			return None

		# Create the buffer (dissolve all so result is a single polygon)
		arcpy.analysis.Buffer(layer_name, out_path, buffer_distance, dissolve_option="ALL")
		print(f"Buffer created: {out_path}")

		if add_to_project:
			try:
				if aprx_path is None:
					aprx = arcpy.mp.ArcGISProject("CURRENT")
				else:
					aprx = arcpy.mp.ArcGISProject(aprx_path)
				maps = aprx.listMaps()
				if not maps:
					print("No maps found in APRX to add the layer to.")
				else:
					maps[0].addDataFromPath(out_path)
					aprx.save()
					print("Added buffer layer to the first map in the APRX.")
			except Exception as ex:
				print("Warning: could not add to project:", ex)

		return out_path

	except arcpy.ExecuteError:
		print(arcpy.GetMessages(2))
		raise
	except Exception as e:
		print("Error:", e)
		raise


if __name__ == "__main__":
	# Example usage: run inside ArcGIS Pro (for add_to_project=True use CURRENT aprx)
	try:
		out = buffer_fresno(add_to_project=False)
		if out:
			print("Success:", out)
	except Exception as e:
		print("Failed:", e)

# End of module