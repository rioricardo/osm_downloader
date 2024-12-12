from pyproj import  Transformer

#transformer = Transformer.from_crs("EPSG:4326", "EPSG:32633", always_xy=True)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

# Example coordinates (longitude, latitude)
# lon, lat = 104.979799, -5.863598  
# left top
# tile 50,33
lon, lat = 101.25,-2.657846875000004
#tile 51, 33
lon, lat = 106.875, -2.657846875000004
#tile 52, 33
lon, lat = 112.5, -2.657846875000004

# Convert to UTM
x, y = transformer.transform(lon, lat)

print(f"Top Longitude: {lon}, Latitude: {lat}")
print(f"Top X (meters): {x}, Y (meters): {y}")

# Example coordinates (longitude, latitude)
#lon, lat = 115.800477, -9 

# left bottom
# tile 50,34
lon, lat = 101.25, -5.315693749999994
# tile 51, 34
lon, lat = 106.875, -5.315693749999994
# tile 52, 34
lon, lat = 112.5, -5.315693749999994


# Convert to UTM
x, y = transformer.transform(lon, lat)

print(f"Bottom Longitude: {lon}, Latitude: {lat}")
print(f"Bottom X (meters): {x}, Y (meters): {y}")