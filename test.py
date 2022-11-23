from zipfile import ZipFile
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

with ZipFile("C:/Users/Admin/Downloads/budapest_gtfs.zip") as bp:
    stops_df = pd.read_csv(bp.open("stops.txt"), dtype={
        'stop_id': 'str',
        'stop_name': 'str',
        'stop_lat': 'float',
        'stop_lon': 'float',
        'stop_code': 'str',
        'location_type': 'Int64',
        'location_sub_type': 'str',
        'parent_station': 'str',
        'wheelchair_boarding': 'Int64',
        'stop_direction': 'Int64'
    })
    stops_gdf = gpd.GeoDataFrame(stops_df, 
        geometry=gpd.points_from_xy(stops_df.stop_lon, stops_df.stop_lat)).set_crs(epsg=4326)
    # display(stops_gdf)
    
    bme_i_point = Point(19.060057883705937, 47.47285062052112)
    bme_i = { 'geometry': [bme_i_point] }
    bme_gdf = gpd.GeoDataFrame(bme_i, crs="EPSG:4326")

    stops_gdf.to_crs({"init": "EPSG:3857"}, inplace=True)
    bme_gdf.to_crs({"init": "EPSG:3857"}, inplace=True)
    
    bme_1km_radius = bme_gdf.buffer(1000).unary_union

    neighbours_selector = stops_gdf["geometry"].intersection(bme_1km_radius)

    # print all the nearby points
    stops_1km_gdf = stops_gdf[~neighbours_selector.is_empty] # select actual stops
    x = bme_gdf.iloc[[0]]
    print(x)
    stops_1km_gdf['distance'] = stops_1km_gdf.distance(bme_gdf.iloc[[0]])
    print(stops_1km_gdf)