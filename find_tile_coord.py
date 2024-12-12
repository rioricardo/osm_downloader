def top_left_tile_coordinates(x_tile, y_tile, zoom):
    # Tile grid starts at (0, 0) for the top-left corner
    
    # Longitude range (-180 to 180 degrees)
    tile_width = 360 / (2 ** zoom)
    # Latitude range (-85.0511 to 85.0511 degrees)
    tile_height = 170.1022 / (2 ** zoom)
    
    # Top-left corner of the world
    lon = -180 + (x_tile * tile_width)
    lat = 85.0511 - (y_tile * tile_height)
    
    return lon, lat

# Example usage
zoom_level = 6
x_tile = 53
y_tile = 33
lon, lat = top_left_tile_coordinates(x_tile, y_tile, zoom_level)
print(f"Top-Left Tile Coordinates at Zoom Level {zoom_level}: x tile= {x_tile} y tile= {y_tile}  Longitude = {lon}, Latitude = {lat}")
x_tile = 53
y_tile = 34
lon, lat = top_left_tile_coordinates(x_tile, y_tile, zoom_level)
print(f"Top-Left Tile Coordinates at Zoom Level {zoom_level}: x tile= {x_tile} y tile= {y_tile}  Longitude = {lon}, Latitude = {lat}")

