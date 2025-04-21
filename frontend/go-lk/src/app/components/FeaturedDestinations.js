// components/FeaturedDestinations.js
"use client";
import { useState, useEffect } from 'react';
import DestinationCard from './DestinationCard';
import { getRandomDestinations } from '../data/destinations';

export default function FeaturedDestinations({ count = 3 }) {
  const [destinations, setDestinations] = useState([]);
  
  useEffect(() => {
    // Get random destinations on component mount
    setDestinations(getRandomDestinations(count));
  }, [count]);
  
  return (
    <div className="container mx-auto px-6 py-16">
      <h2 className="text-3xl font-bold text-gray-800 mb-10 text-center">Featured Destinations</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {destinations.map((destination) => (
          <DestinationCard key={destination.id} destination={destination} />
        ))}
      </div>
    </div>
  );
}