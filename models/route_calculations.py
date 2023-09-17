import googlemaps
import polyline
from datetime import datetime
import numpy as np
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyBa2xLbIRxFss9cJ4bWAgWH2yylGQgp-hk')

def call_directions(start, end, time):
    departure_time = datetime.strptime(time, "%Y-%m-%dT%H:%M")
    return gmaps.directions(start, end, mode='driving', departure_time=departure_time)

class Route_functions:
    def __init__(self) -> None:
        self.gmaps = googlemaps.Client(key='AIzaSyBa2xLbIRxFss9cJ4bWAgWH2yylGQgp-hk')

    # Function to do all the processes at once. Only to be used when __main__
    def similarity_wrapper(self, car_owner_source, car_owner_destination, passenger_source, passenger_destination, departure_time=datetime.now(),rounding_flag=False, rounding_threshold=3):
        # Getting directions from the api
        car_directions = self.call_directions(car_owner_source, car_owner_destination)
        passenger_directions = self.call_directions(passenger_source, passenger_destination)

        # Decoding coords
        car_decoded_coords = self.decode_coords(car_directions, rounding_flag, rounding_threshold)
        passenger_decoded_coords = self.decode_coords(passenger_directions, rounding_flag, rounding_threshold)

        # Getting route similarity
        similarity = self.route_similarity(car_decoded_coords, passenger_decoded_coords)

        print(similarity)

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
    
    def euclidean_distance(self,point1, point2):
        lat1, lon1 = point1
        lat2, lon2 = point2
        return np.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

    # Calculate the DTW alignment cost
    def dtw_alignment_cost(self, sequence1, sequence2):
        n = len(sequence1)
        m = len(sequence2)
        dtw_matrix = np.zeros((n, m))

        for i in range(n):
            for j in range(m):
                cost = self.euclidean_distance(sequence1[i], sequence2[j])
                if i == 0 and j == 0:
                    dtw_matrix[i][j] = cost
                elif i == 0:
                    dtw_matrix[i][j] = cost + dtw_matrix[i][j - 1]
                elif j == 0:
                    dtw_matrix[i][j] = cost + dtw_matrix[i - 1][j]
                else:
                    dtw_matrix[i][j] = cost + min(dtw_matrix[i - 1][j], dtw_matrix[i][j - 1], dtw_matrix[i - 1][j - 1])

        return dtw_matrix[n - 1][m - 1]

    def route_similarity(self,car_owner_route, passenger_route):
        # Calculate the normalized alignment cost
        alignment_cost = self.dtw_alignment_cost(car_owner_route, passenger_route)
        normalized_cost = alignment_cost / max(len(car_owner_route), len(passenger_route))

        print("DTW Alignment Cost:", alignment_cost)
        print("Normalized Cost:", normalized_cost)

        return normalized_cost
    
if __name__=="__main__":
    obj = Route_functions()
    car_owner_source =      ""
    car_owner_destination = ""
    passenger_source =      ""
    passenger_destination = ""
    obj.similarity_wrapper(car_owner_source, 
                           car_owner_destination, 
                           passenger_source, 
                           passenger_destination)