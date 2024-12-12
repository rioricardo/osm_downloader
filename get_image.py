import math
import os
import requests
import time

"""
dari nasa
perbesaran 5 20x40 19x39
perbesaran 6 30X80 29x79
klo mercator zoom 6 63*63 2^zoom level -1 , 2^zoom level -1

"""
def lon_lat_to_tile_index(lon, lat, zoom):
    # Constants
    TILE_SIZE = 256
    
    # Convert longitude and latitude to Mercator coordinates
    x = (lon + 180) / 360.0
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2.0
    
    # Scale for the given zoom level
    scale = 2 ** zoom
    x = x * TILE_SIZE * scale
    y = y * TILE_SIZE * scale
    
    # Calculate tile indices
    tile_x = int(x // TILE_SIZE)
    tile_y = int(y // TILE_SIZE)
    
    return tile_x, tile_y

def tile_to_lonlat(x_tile, y_tile, zoom):
    # Calculate longitude
    lon = x_tile / (2 ** zoom) * 360.0 - 180.0
    
    # Calculate latitude
    n = math.pi - 2.0 * math.pi * y_tile / (2 ** zoom)
    lat = math.degrees(math.atan(math.sinh(n)))
    
    return lon, lat

def lat_lon_to_tile_index_4236(lon, lat, zoom):
    # Constants for Web Mercator projection
    R = 6378137  # Radius of the Earth in meters
    TILE_SIZE = 256
    
    # Convert latitude and longitude to radians
    lon_rad = math.radians(lon)
    lat_rad = math.radians(lat)
    
    # Convert latitude and longitude to Mercator x and y coordinates
    x = R * lon_rad
    y = R * math.log(math.tan(math.pi / 4 + lat_rad / 2))
    
    # Convert Mercator coordinates to pixel coordinates
    scale = 2 ** zoom
    x_pixel = (x + R) * (TILE_SIZE / (2 * R)) * scale
    y_pixel = (R - y) * (TILE_SIZE / (2 * R)) * scale
    
    # Calculate tile indices
    tile_x = int(x_pixel // TILE_SIZE)
    tile_y = int(y_pixel // TILE_SIZE)
    
    return tile_x, tile_y

# Example usage:
longitude = 180  #x 
latitude =  -85.0511 #y

lon_java = 104.979799
lat_java = -5.863598

lat_bottom = -9
lon_bottom = 115.800477

zoom_level = 0
first_zoom = 6
last_zoom = 7
iter_rast = 0

output_prefix = "D:/5_Data_Proyek/JAMALI_lagi/5_Template/RasterSet/osm2"  # Replace with your desired path

tile_x_topl, tile_y_topl = lon_lat_to_tile_index(lon_java, lat_java, first_zoom)
print(f"Tile Index top left Java: x={tile_x_topl}, y={tile_y_topl}")
tile_x_rbot, tile_y_rbot = lon_lat_to_tile_index(lon_bottom, lat_bottom, first_zoom)
print(f"Tile Index right bottom java: x={tile_x_rbot}, y={tile_y_rbot}")

iter_top_tile_x = tile_x_topl
iter_top_tile_y = tile_y_topl
iter_bot_tile_x = tile_x_topl + 1
iter_bot_tile_y = tile_y_topl + 1
#number of raster only tilex
num_raster = tile_x_rbot - tile_x_topl + 1

while iter_rast < num_raster :
    #create directory 
   #output_directory = output_prefix + "/rast-" + str(iter_rast)
    output_directory = os.path.join(output_prefix, f"osm-{iter_rast}")
    os.makedirs(output_directory, exist_ok=True)
    iter_zoom = first_zoom
    
    #find out right top and left bottom latitude 
    current_top_lon,curent_top_lat = tile_to_lonlat(iter_top_tile_x, iter_top_tile_y , iter_zoom)
    current_bot_lon,curent_bot_lat = tile_to_lonlat(iter_bot_tile_x, iter_bot_tile_y , iter_zoom)

    while iter_zoom <= last_zoom:
       #out_zoom_directory = output_directory + "/" + str(iter_zoom - first_zoom)
        out_zoom_directory = os.path.join(output_directory, f"{iter_zoom - first_zoom}")
        os.makedirs(out_zoom_directory, exist_ok=True)
        
        #now iterate throgh tile x
        tile_x_topl, tile_y_topl = lon_lat_to_tile_index(current_top_lon, curent_top_lat, iter_zoom)
        print(f"Tile Index top left Java: x={tile_x_topl}, y={tile_y_topl}")
        tile_x_rbot, tile_y_rbot = lon_lat_to_tile_index(current_bot_lon, curent_bot_lat, iter_zoom)
        print(f"Tile Index right bottom java: x={tile_x_rbot}, y={tile_y_rbot}")

        iter_x = 0
        while iter_x < tile_x_rbot - tile_x_topl:
           #out_x_directory = out_zoom_directory + "/" + str(iter_x)
            out_x_directory = os.path.join(out_zoom_directory, f"{iter_x}")
            os.makedirs(out_x_directory, exist_ok=True)
            iter_y = 0
            while iter_y < tile_y_rbot - tile_y_topl:
           #while iter_y >= 0 :
               #print(f"iter_x={iter_x}, iter_y={iter_y}")
                while True: 
                    try:
                    #url = f"https://tile.openstreetmap.org/{iter_zoom}/{iter_x + tile_x_topl }/{iter_y + tile_y_rbot}.png"
                        url = f"https://tile.openstreetmap.org/{iter_zoom}/{iter_x + tile_x_topl}/{tile_y_rbot - iter_y - 1}.png"
                        headers = {
                            "User-Agent": "YourAppName/1.0 (rioricardos@gmail.com)"
                        }
                        response = requests.get(url, headers=headers)
                    #print("response status is : " ,response.status_code)
                        # Define the complete path where the file will be saved
                        output_path = os.path.join(out_x_directory, f"{iter_y}.jpg")
                        # Save the image as a file
                        if response.status_code == 200:
                            with open(output_path, "wb") as file:
                                file.write(response.content)
                            print(f"tile {iter_x + tile_x_topl},{tile_y_rbot - iter_y} downloaded successfully.")
                            iter_y += 1
                            break
                        else:
                            print("Failed to download map tile.")
                    except Exception as e:
                        time.sleep(15)
            iter_x += 1
        iter_zoom += 1
    
    iter_rast += 1
    #only need to move tile x
    iter_top_tile_x += 1
    iter_bot_tile_x += 1


"""
perbesaran 14
topleft 12969 8459
rightbot 13462 8603 
"""


"""
zoom 1 3x2
zoom 2 5x3
zoom 3 10x5
zoom 4 20x10
zoom 5 40x20
zoom 6 80x40

maxtile x 
maxtile y 

"""