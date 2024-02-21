import geopandas as gpd
from haversine import haversine

edges = gpd.read_file('adapted_data/Edin/map/edges.shp')
nodes = gpd.read_file('adapted_data/Edin/map/nodes.shp')

for i in range(len(edges)):
    edge = edges.iloc[i]
    edge_start = edge['geometry'].coords[0]
    edge_end = edge['geometry'].coords[-1]

    found = 0
    for j in range(len(nodes)):
        node = nodes.iloc[j]
        node_coord = node['geometry'].coords[0]

        if node_coord == edge_start:
            edges.at[i, 'u'] = node['osm_id']
            found += 1

        if node_coord == edge_end:
            edges.at[i, 'v'] = node['osm_id']
            found += 1
        
        if found == 2: break
            
    edges.at[i, 'length'] = haversine((edge_start[1], edge_start[0]), (edge_end[1], edge_end[0]))
    
edges.to_file('adapted_data/Edin/map/edges.shp')