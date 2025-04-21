"use client";
import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const [searchDestination, setSearchDestination] = useState('');
  const router = useRouter();

  const handleChatbotRedirect = () => {
    router.push('/tourmate?message=' + encodeURIComponent(searchDestination));
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <div className="relative h-[600px] w-full">
        <Image 
          src="/images/slbeach.jpg" 
          alt="Sri Lanka Beach" 
          fill
          priority
          className="object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-black/60 to-transparent">
          <div className="container mx-auto px-6 h-full flex flex-col justify-center">
            <h1 className="text-5xl md:text-6xl font-bold text-white max-w-2xl">
              Discover Sri Lanka with AI Assistance
            </h1>
            <p className="text-xl text-white mt-6 max-w-xl">
              Why settle for generic travel advice when you can have personalized guidance from TourMate?
            </p>
            
            {/* Search Bar */}
            <div className="mt-10 flex flex-col md:flex-row gap-2 bg-white rounded-lg p-2 shadow-lg max-w-4xl">
              <div className="flex-1 flex items-center pl-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <input 
                  type="text" 
                  placeholder="Where in Sri Lanka do you want to go?" 
                  className="flex-1 p-2 outline-none"
                  value={searchDestination}
                  onChange={(e) => setSearchDestination(e.target.value)}
                />
              </div>
              
              <button
                className="bg-emerald-600 hover:bg-emerald-700 text-white py-3 px-6 rounded-lg font-medium transition-colors"
                onClick={handleChatbotRedirect}
              >
                Ask TourMate
              </button>
            </div>

            <p className="text-white/80 mt-4 text-sm">
              Our AI-powered chatbot provides accurate, up-to-date information about Sri Lanka
            </p>
          </div>
        </div>
      </div>

      {/* Featured Destinations */}
      <div className="container mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-gray-800 mb-10 text-center">Featured Destinations</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Destination 1 */}
          <div className="rounded-xl overflow-hidden shadow-lg group hover:shadow-2xl transition-all">
            <div className="relative h-64 w-full">
              <Image 
                src="/images/sigiriya.jpg" 
                alt="Sigiriya Rock Fortress" 
                fill
                className="object-cover group-hover:scale-105 transition-transform duration-300"
              />
            </div>
            <div className="p-6">
              <div className="flex justify-between items-center mb-3">
                <h3 className="text-xl font-bold text-gray-800">Sigiriya</h3>
                <div className="flex items-center">
                  <span className="text-amber-500">★★★★★</span>
                  <span className="text-gray-600 ml-1">4.8</span>
                </div>
              </div>
              <p className="text-gray-600 mb-4">Ancient rock fortress with stunning views and remarkable history</p>
              <button 
                onClick={handleChatbotRedirect}
                className="text-emerald-600 font-medium hover:text-emerald-800"
              >
                Ask TourMate about Sigiriya →
              </button>
            </div>
          </div>

          {/* Destination 2 */}
          <div className="rounded-xl overflow-hidden shadow-lg group hover:shadow-2xl transition-all">
            <div className="relative h-64 w-full">
              <Image 
                src="/images/kandylake.jpg" 
                alt="Kandy Lake" 
                fill
                className="object-cover group-hover:scale-105 transition-transform duration-300"
              />
            </div>
            <div className="p-6">
              <div className="flex justify-between items-center mb-3">
                <h3 className="text-xl font-bold text-gray-800">Kandy</h3>
                <div className="flex items-center">
                  <span className="text-amber-500">★★★★☆</span>
                  <span className="text-gray-600 ml-1">4.7</span>
                </div>
              </div>
              <p className="text-gray-600 mb-4">Cultural capital with the famous Temple of the Sacred Tooth Relic</p>
              <button 
                onClick={handleChatbotRedirect}
                className="text-emerald-600 font-medium hover:text-emerald-800"
              >
                Ask TourMate about Kandy →
              </button>
            </div>
          </div>

          {/* Destination 3 */}
          <div className="rounded-xl overflow-hidden shadow-lg group hover:shadow-2xl transition-all">
            <div className="relative h-64 w-full">
              <Image 
                src="/images/galle.jpg" 
                alt="Galle Fort" 
                fill
                className="object-cover group-hover:scale-105 transition-transform duration-300"
              />
            </div>
            <div className="p-6">
              <div className="flex justify-between items-center mb-3">
                <h3 className="text-xl font-bold text-gray-800">Galle</h3>
                <div className="flex items-center">
                  <span className="text-amber-500">★★★★★</span>
                  <span className="text-gray-600 ml-1">4.9</span>
                </div>
              </div>
              <p className="text-gray-600 mb-4">Colonial-era fortress city with charming streets and ocean views</p>
              <button 
                onClick={handleChatbotRedirect}
                className="text-emerald-600 font-medium hover:text-emerald-800"
              >
                Ask TourMate about Galle →
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Why Use TourMate Section */}
      <div className="bg-gray-50 py-16">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-gray-800 mb-4 text-center">Why Use TourMate?</h2>
          <p className="text-gray-600 text-center mb-12 max-w-3xl mx-auto">
            The average travel planner can't compete with our AI-powered assistant. Here are a few reasons to use TourMate for your Sri Lankan adventure.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition-shadow">
              <div className="w-14 h-14 bg-emerald-100 rounded-lg flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">Accurate Accommodation Info</h3>
              <p className="text-gray-600">
                Get real-time information on hotels, resorts, and guesthouses throughout Sri Lanka with detailed ratings and amenities.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition-shadow">
              <div className="w-14 h-14 bg-emerald-100 rounded-lg flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">Local Experiences</h3>
              <p className="text-gray-600">
                Discover authentic Sri Lankan experiences with personalized recommendations based on your interests and preferences.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition-shadow">
              <div className="w-14 h-14 bg-emerald-100 rounded-lg flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">Emergency Assistance</h3>
              <p className="text-gray-600">
                Access critical information about nearby hospitals, police stations, and emergency contacts when you need it most.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Testimonials Section */}
      <div className="container mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-gray-800 mb-12 text-center">What Our Users Say</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Testimonial 1 */}
          <div className="bg-white p-8 rounded-xl shadow-md border border-gray-100">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 rounded-full bg-gray-200 overflow-hidden relative">
                <Image 
                  src="/images/userAvatar.png" 
                  alt="User" 
                  fill
                  className="object-cover"
                />
              </div>
              <div className="ml-4">
                <h4 className="font-bold text-gray-800">Sarah Johnson</h4>
                <div className="text-amber-500">★★★★★</div>
              </div>
            </div>
            <p className="text-gray-600">
              "TourMate helped me plan the perfect trip to Sri Lanka. The chatbot gave me accurate information about hotels in Ella and suggested amazing hiking trails!"
            </p>
          </div>

          {/* Testimonial 2 */}
          <div className="bg-white p-8 rounded-xl shadow-md border border-gray-100">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 rounded-full bg-gray-200 overflow-hidden relative">
                <Image 
                  src="/images/userAvatar.png" 
                  alt="User" 
                  fill
                  className="object-cover"
                />
              </div>
              <div className="ml-4">
                <h4 className="font-bold text-gray-800">Michael Patel</h4>
                <div className="text-amber-500">★★★★★</div>
              </div>
            </div>
            <p className="text-gray-600">
              "When my plans changed suddenly, I needed to find a hospital near Kandy. TourMate immediately provided me with contact details and directions."
            </p>
          </div>

          {/* Testimonial 3 */}
          <div className="bg-white p-8 rounded-xl shadow-md border border-gray-100">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 rounded-full bg-gray-200 overflow-hidden relative">
                <Image 
                  src="/images/userAvatar.png" 
                  alt="User" 
                  fill
                  className="object-cover"
                />
              </div>
              <div className="ml-4">
                <h4 className="font-bold text-gray-800">Emily Chen</h4>
                <div className="text-amber-500">★★★★☆</div>
              </div>
            </div>
            <p className="text-gray-600">
              "As a foodie traveling through Sri Lanka, TourMate's restaurant recommendations were spot-on! I discovered amazing local cuisine that I wouldn't have found otherwise."
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-emerald-700 py-16">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-white mb-6">Ready to explore Sri Lanka?</h2>
          <p className="text-white/90 max-w-2xl mx-auto mb-8">
            Let TourMate be your personal guide through the Pearl of the Indian Ocean.
            Get accurate information, personalized recommendations, and emergency assistance all in one place.
          </p>
          <button
            onClick={handleChatbotRedirect}
            className="bg-white text-emerald-700 hover:bg-gray-100 py-3 px-8 rounded-lg font-medium text-lg transition-colors"
          >
            Ask TourMate Now
          </button>
        </div>
      </div>
    </div>
  );
}