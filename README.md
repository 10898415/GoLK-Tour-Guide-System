About

Go-LK is an AI-powered tour guide system designed to assist tourists visiting Sri Lanka. The platform features TourMate, an intelligent chatbot that provides accurate, up-to-date information about destinations, accommodations, restaurants, weather conditions, and emergency services across the country.

Built with a Neo4j graph database at its core, Go-LK delivers a comprehensive tourism experience with:

	Natural language interactions through a user-friendly chatbot interface
	Multilingual support to assist international tourists
	Location-based recommendations for attractions, accommodations, and dining
	Emergency service information including hospitals and police stations
	Accurate distance calculations between destinations
	Weather information to help plan trips effectively

This project was developed as a final year project for the BSc (Hons) in Software Engineering program at NSBM Green University/Plymouth University.


Installation and Setup

	Backend Setup
 		Navigate to the backend directory:
				cd backend
		
		Install dependencies:
				pip install -r requirements.txt
		
		Create a .env file in the backend root directory with the following variables:
				NEO4J_URI=your_neo4j_uri
				NEO4J_USERNAME=your_neo4j_username
				NEO4J_PASSWORD=your_neo4j_password
				OPENAI_API_KEY=your_openai_api_key
		
 		Start
	 			python main.py

	Frontend Setup
 		Navigate to the frontend directory:
	 			cd frontend/go-lk

	 	Install dependencies:
	 			npm install

	 	Start the frontend:
	 			npm run dev

	 	Access the application:
	 			http://localhost:3000

	
