This Python script tool was developed for the final project in **GEOG 485: GIS Programming and Software Development** at Penn State. It compares current and historical Chicago bike lane datasets to identify removed bike lanes, merges geometries, and exports results as a shapefile.

## 🔍 What It Does

- Loads two datasets (current and historical) in CSV format
- Identifies which older bike lanes are missing from the current data
- Builds new polylines using coordinate strings
- Labels current lanes as `"No"` and removed lanes as `"Yes"` in the `HISTORICAL` field
- Merges duplicate segments into single polylines using `Dissolve`

## 📂 Files

- `FinalProjectScript.py`: Main script with hardcoded file paths
- `FinalLessonScriptTool.py`: Modified version intended for use in ArcGIS Pro as a script tool with parameters
- `FinalProjectScriptWithPDFExport.py`: Optional version (early stage) intended to expand features

## 🛠️ Tools & Libraries

- ArcPy
- Python 3.9+
- ArcGIS Pro
- CSV input files with WKT `MULTILINESTRING` geometry

## 📌 Instructions

1. Run the script from ArcGIS Pro (via toolbox or Python window), or use `FinalProjectScript.py` directly with your file paths.
2. Ensure both CSV files use:
   - A `STREET` field (for bike lane name)
   - A `the_geom` field (WKT-style geometry)
3. A shapefile named `BikeLane.shp` will be created, with merged results.
4. Output will show current vs. removed lanes in the `HISTORICAL` field.

## 📷 Output Example *(Optional)*

![Map Screenshot](outputs/example_bike_lanes_map.png)

## 🧠 Reflection

This project helped me apply:
- Data parsing and cleaning
- Use of dictionaries for spatial logic
- `arcpy` geometry construction
- `InsertCursor`, `Dissolve`, and conditional logic

## 👤 Author

Jeffery Rodriguez  
GIS Master's Student @ Penn State  
[Portfolio](https://jeffarodriguez.weebly.com/)
