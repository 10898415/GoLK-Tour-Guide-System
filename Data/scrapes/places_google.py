import googlemaps
import csv
import time

# Replace with your Google Maps API key
API_KEY = "AIzaSyB8AmLV_o52mpi5atWkbjafYpsn8YN2g8o"

# Initialize Google Maps client
gmaps = googlemaps.Client(key=API_KEY)

# List of all 25 districts in Sri Lanka and their major areas
districts_and_areas = {
    "Colombo": ["Colombo", "Dehiwala", "Mount Lavinia", "Pettah", "Fort"],
    "Gampaha": ["Gampaha", "Negombo", "Katunayake", "Ja-Ela", "Wattala", "Kandana"],
    "Kalutara": ["Kalutara", "Panadura", "Beruwala", "Aluthgama", "Wadduwa", "Horana"],
    "Kandy": ["Kandy", "Peradeniya", "Gampola", "Kundasale", "Kadugannawa", "Nawalapitiya"],
    "Matale": ["Matale", "Dambulla", "Sigiriya", "Naula", "Rattota", "Palapathwela"],
    "Nuwara Eliya": ["Nuwara Eliya", "Horton Plains", "Ella", "Talawakele", "Hatton", "Ragala"],
    "Galle": ["Galle", "Hikkaduwa", "Unawatuna", "Ambalangoda", "Bentota", "Ahangama"],
    "Matara": ["Matara", "Weligama", "Mirissa", "Dikwella", "Hambantota", "Tangalle"],
    "Hambantota": ["Hambantota", "Tangalle", "Tissamaharama", "Ambalantota", "Bundala", "Kataragama"],
    "Jaffna": ["Jaffna", "Nallur", "Point Pedro", "Chavakachcheri", "Karainagar", "Delft"],
    "Kilinochchi": ["Kilinochchi", "Pallai", "Paranthan", "Kandavalai"],
    "Mannar": ["Mannar", "Talaimannar", "Madhu", "Nanattan"],
    "Vavuniya": ["Vavuniya", "Cheddikulam", "Nedunkeni", "Omanthai"],
    "Mullaitivu": ["Mullaitivu", "Puthukudiyiruppu", "Oddusuddan", "Alampil"],
    "Batticaloa": ["Batticaloa", "Kalkudah", "Pasikudah", "Valaichchenai", "Kattankudy", "Eravur"],
    "Ampara": ["Ampara", "Arugam Bay", "Pottuvil", "Sainthamaruthu", "Kalmunai", "Sammanthurai"],
    "Trincomalee": ["Trincomalee", "Nilaveli", "Kuchchaveli", "Kinniya", "Seruwila", "Gomarankadawala"],
    "Kurunegala": ["Kurunegala", "Puttalam", "Chilaw", "Kuliyapitiya", "Narammala", "Polgahawela"],
    "Puttalam": ["Puttalam", "Kalpitiya", "Chilaw", "Anamaduwa", "Wennappuwa", "Madampe"],
    "Anuradhapura": ["Anuradhapura", "Mihintale", "Thanthirimale", "Kekirawa", "Nochchiyagama", "Rambewa"],
    "Polonnaruwa": ["Polonnaruwa", "Hingurakgoda", "Kaduruwela", "Medirigiriya", "Lankapura", "Dimbulagala"],
    "Badulla": ["Badulla", "Bandarawela", "Ella", "Haputale", "Passara", "Welimada"],
    "Monaragala": ["Monaragala", "Sella Kataragama", "Wellawaya", "Bibile", "Buttala", "Kataragama"],
    "Ratnapura": ["Ratnapura", "Sinharaja", "Balangoda", "Embilipitiya", "Kuruwita", "Eheliyagoda"],
    "Kegalle": ["Kegalle", "Pinnawala", "Mawanella", "Rambukkana", "Warakapola", "Ruwanwella"]
}

# Function to classify activity type
def classify_activity_type(place_types):
    outdoor_types = ["park", "natural_feature", "waterfall", "hiking_area", "mountain", "zoo", "garden"]
    indoor_types = ["museum", "art_gallery", "shopping_mall", "aquarium", "theater", "library", "church", "temple"]

    for type in place_types:
        if type in outdoor_types:
            return "Outdoor"
        elif type in indoor_types:
            return "Indoor"
    return "Outdoor"  # Default to Outdoor if no specific type is found

# Open a CSV file to save the results
with open('all_tourist_attractions.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["District", "Area", "Place to Visit", "Activity Type", "Google Map Link"])

    # Loop through each district and area
    for district, areas in districts_and_areas.items():
        for area in areas:
            print(f"Processing {area}, {district}...")

            # Define the search query (e.g., tourist attractions)
            query = f"tourist attractions in {area}, {district}"

            # Perform a text search using the Google Places API
            try:
                places_result = gmaps.places(query)

                # Loop through the results and extract relevant information
                while True:
                    for place in places_result['results']:
                        try:
                            place_name = place['name']
                            place_id = place['place_id']
                            place_types = place.get('types', [])
                            activity_type = classify_activity_type(place_types)
                            google_map_link = f"https://www.google.com/maps/place/?q=place_id:{place_id}"

                            # Write the data to the CSV file
                            writer.writerow([district, area, place_name, activity_type, google_map_link])
                            print(f"Added: {place_name} in {area}, {district}")

                        except Exception as e:
                            print(f"Error processing place {place_name}: {e}")

                    # Check if there are more results
                    if 'next_page_token' not in places_result:
                        break

                    # Wait for a few seconds before making the next request (required by Google API)
                    time.sleep(2)

                    # Fetch the next page of results
                    next_page_token = places_result['next_page_token']
                    places_result = gmaps.places(query, page_token=next_page_token)

            except Exception as e:
                print(f"An error occurred while processing {area}, {district}: {e}")

print("All tourist attractions saved to all_tourist_attractions.csv")