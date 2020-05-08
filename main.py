import json
import Floor_planning

with open('example1.json') as json_file:
    data = json.load(json_file)
    my_floorplan = Floor_planning.make_floorplan(data, 0.6)
    my_floorplan.make_test_file("myfloorplan.txt")
