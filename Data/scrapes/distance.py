import googlemaps
import csv


API_KEY = "AIzaSyB8AmLV_o52mpi5atWkbjafYpsn8YN2g8o"


locations = [
    "Arugam Bay",
    "Nuwara Eliya",
    "Kandy",
    "Kataragama",
    "Anuradhapura",
    "Polonnaruwa",
    "Sigiriya",
    "Trincomalee",
    "Jaffna",
    "Kalpitiya",
    "Passikudah",
    "Bentota",
    "Haputale",
    "Matara",
    "Puttalam",
    "Weligama",
    "Badulla",
    "Hambantota",
    "Diyatalawa",
    "Negombo",
    "Ella",
    "Hikkaduwa",
    "Galle",
    "Bandarawela",
    "Ratnapura",
    "Knuckles",
    "Kitulgala",
    "Tangalle",
    "Maskeliya",
    "Mannar",
    "Mirissa",
    "Pottuvil",
    "Mullaitivu",
    "Dambulla",
    "Avissawella",
    "Kalutara",
    "Deniyaya",
    "Monaragala",
    "Tissamaharama",
    "Sella Kataragama",
    "Colombo",
    "Gampaha",
    "Dodanduwa",
    "Horton Plains",
    "Sinharaja",
    "Chilaw",
    "Matale",
    "Kurunegala",
    "Ambalangoda"
]

# Initialize Google Maps client
gmaps = googlemaps.Client(key=API_KEY)

# Function to get driving distance between two locations
def get_driving_distance(origin, destination):
    try:
        # Get driving distance using Google Maps API
        result = gmaps.distance_matrix(origin, destination, mode="driving")
        distance = result["rows"][0]["elements"][0]["distance"]["text"]
        return distance
    except Exception as e:
        print(f"Error calculating distance from {origin} to {destination}: {e}")
        return "N/A"

# Calculate distances and store in a list
distances = []
for i in range(len(locations)):
    for j in range(i + 1, len(locations)):
        loc1 = locations[i]
        loc2 = locations[j]
        distance = get_driving_distance(loc1, loc2)
        distances.append([loc1, loc2, distance])
        print(f"Processed: {loc1} -> {loc2} = {distance}")

# Write to CSV
with open('driving_distances.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Location 1", "Location 2", "Driving Distance"])
    writer.writerows(distances)

print("Driving distances calculated and saved to driving_distances.csv")