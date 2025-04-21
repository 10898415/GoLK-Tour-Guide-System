// data/destinations.js

// Array of all Sri Lankan destinations
const destinations = [
    {
      id: 1,
      name: "Sigiriya",
      rating: 4.8,
      description: "Ancient rock fortress with stunning views and remarkable history",
      image: "/images/sigiriya.jpg"
    },
    {
      id: 2,
      name: "Kandy",
      rating: 4.7,
      description: "Cultural capital with the famous Temple of the Sacred Tooth Relic",
      image: "/images/kandylake.jpg"
    },
    {
      id: 3,
      name: "Galle",
      rating: 4.9,
      description: "Colonial-era fortress city with charming streets and ocean views",
      image: "/images/galle.jpg"
    },
    {
      id: 4,
      name: "Anuradhapura",
      rating: 4.6,
      description: "Ancient city with sacred Buddhist sites and impressive stupas",
      image: "/images/anuradhapura.jpg"
    },
    {
      id: 5,
      name: "Polonnaruwa",
      rating: 4.7,
      description: "Medieval capital with well-preserved ruins and ancient temples",
      image: "/images/polonnaruwa.jpg"
    },
    {
      id: 6,
      name: "Mirissa",
      rating: 4.8,
      description: "Beautiful beach town famous for whale watching and surfing",
      image: "/images/mirissa.jpg"
    },
    {
      id: 7,
      name: "Nuwara Eliya",
      rating: 4.5,
      description: "Hill country city with tea plantations and cool climate",
      image: "/images/nuwaraeliya.jpg"
    },
    {
      id: 8,
      name: "Yala National Park",
      rating: 4.9,
      description: "Wildlife sanctuary with the highest leopard density in the world",
      image: "/images/yala.jpg"
    },
    {
      id: 9,
      name: "Ella",
      rating: 4.8,
      description: "Scenic mountain town with hiking trails and stunning views",
      image: "/images/ella.jpg"
    },
    {
      id: 10,
      name: "Hikkaduwa",
      rating: 4.5,
      description: "Vibrant beach town with coral reefs and great nightlife",
      image: "/images/hikkaduwa.jpg"
    },
    {
      id: 11,
      name: "Jaffna",
      rating: 4.4,
      description: "Northern cultural hub with unique Tamil heritage and cuisine",
      image: "/images/jaffna.jpg"
    },
    {
      id: 12,
      name: "Trincomalee",
      rating: 4.7,
      description: "Port city with gorgeous beaches and natural harbor",
      image: "/images/trincomalee.jpg"
    },
    {
      id: 13,
      name: "Arugam Bay",
      rating: 4.8,
      description: "World-class surfing destination with laid-back atmosphere",
      image: "/images/arugambay.jpg"
    }
  ];
  
  // Function to get random destinations
  export function getRandomDestinations(count = 3) {
    // Create a copy of the array to avoid modifying the original
    const shuffled = [...destinations];
    
    // Fisher-Yates shuffle algorithm
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    
    // Return the first 'count' elements
    return shuffled.slice(0, count);
  }
  
  // Function to get all destinations
  export function getAllDestinations() {
    return destinations;
  }
  
  // Function to get a specific destination by ID
  export function getDestinationById(id) {
    return destinations.find(destination => destination.id === id);
  }
  
  export default destinations;