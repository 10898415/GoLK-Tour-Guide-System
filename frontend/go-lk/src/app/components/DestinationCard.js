// components/DestinationCard.js
"use client";
import Image from 'next/image';

export default function DestinationCard({ destination }) {
  const { name, rating, description, image } = destination;
  
  const handleAskTourMate = () => {
    // Navigate to TourMate page with query parameter
    window.location.href = `/tourmate?message=Tell me about ${name}`;
  };

  return (
    <div className="rounded-xl overflow-hidden shadow-lg group hover:shadow-2xl transition-all">
      <div className="relative h-64 w-full">
        <Image 
          src={image} 
          alt={`${name} in Sri Lanka`} 
          fill
          className="object-cover group-hover:scale-105 transition-transform duration-300"
        />
      </div>
      
      <div className="p-6">
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-xl font-bold text-gray-800">{name}</h3>
          <div className="flex items-center">
            <span className="text-amber-500">{'★'.repeat(Math.floor(rating)) + (rating % 1 >= 0.5 ? '★' : '') + '☆'.repeat(5 - Math.ceil(rating))}</span>
            <span className="text-gray-600 ml-1">{rating}</span>
          </div>
        </div>
        
        <p className="text-gray-600 mb-4">{description}</p>
        
        <button 
          onClick={handleAskTourMate}
          className="text-emerald-600 font-medium hover:text-emerald-800"
        >
          Ask TourMate about {name} →
        </button>
      </div>
    </div>
  );
}