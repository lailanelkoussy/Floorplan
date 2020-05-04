import json
import Floor_planning

with open('example4.json') as json_file:
    data = json.load(json_file)
    my_floorplan = Floor_planning.make_floorplan(data, 0.6)
