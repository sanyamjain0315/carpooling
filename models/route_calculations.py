import googlemaps
import polyline
from datetime import datetime

class Route_functions:
    def __init__(self) -> None:
        self.gmaps = googlemaps.Client(key='YOUR_API_KEY')

    def call_directions(self, source, destination, departure_time=datetime.now()):
        # DO NOT CALL THIS FUNCTION MORE TIMES THAN NECESSARY
        return self.gmaps.directions(source, destination, mode='driving', departure_time=departure_time)
    
    def decode_coords(self, directions, rounding_flag=False, rounding_threshold=3):
        # We decode the polyline points into list of coordinates of the route
        decoded_coords = polyline.decode(directions[0]['overview_polyline']['points'])
        
        # Rounds the coordinates if provided
        if rounding_flag:
            decoded_coords = [(round(lat, rounding_threshold), round(lon, rounding_threshold)) for lat, lon in decoded_coords]
        
        return decoded_coords
    
    def route_similarity(self,car_owner_route, passenger_route):
        # Find common co-ordinates in bothe routes
        common_elements = set(car_owner_route).intersection(set(passenger_route))
        num_common_elements = len(common_elements)

        # Find the total number of unique coords in both routes
        total_elements = set(car_owner_route).union(set(passenger_route))
        num_total_elements = len(total_elements)

        # Calculate the similarity
        similarity = (num_common_elements / num_total_elements)

        return similarity
    
if __name__=="__main__":
    obj = Route_functions()