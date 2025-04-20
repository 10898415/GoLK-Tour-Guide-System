"use client";
import Image from 'next/image';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function AboutUsPage() {
  const router = useRouter();

  const handleChatbotRedirect = () => {
    router.push('/tourmate');
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <div className="relative h-[300px] w-full">
        <Image 
          src="/images/team-banner.jpg" 
          alt="Our Team" 
          fill
          priority
          className="object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-emerald-800/70 to-emerald-600/70 flex items-center">
          <div className="container mx-auto px-6">
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">About Us</h1>
            <p className="text-xl text-white/90 max-w-2xl">
              Meet the team behind GOLK Tourist Guide and our mission to transform tourism in Sri Lanka
            </p>
          </div>
        </div>
      </div>

      {/* Our Story Section */}
      <div className="container mx-auto px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-3xl font-bold text-gray-800 mb-6">Our Story</h2>
            <p className="text-gray-600 mb-4">
              The GOLK Tourist Guide project was born from a simple observation: tourists in Sri Lanka 
              often struggle to find accurate, up-to-date information all in one place. They have to 
              consult multiple sources, which can be time-consuming and sometimes leads to outdated or 
              incorrect information.
            </p>
            <p className="text-gray-600 mb-4">
              As a final year project at the university, we set out to solve this problem by creating 
              a comprehensive, AI-powered solution that would provide visitors with instant access to 
              reliable information about accommodations, attractions, and emergency services throughout 
              Sri Lanka.
            </p>
            <p className="text-gray-600">
              Our focus on leveraging technology to enhance the tourism experience in Sri Lanka 
              has led to the development of TourMate, our AI assistant that combines cutting-edge 
              artificial intelligence with a deep knowledge of Sri Lanka's tourism landscape.
            </p>
          </div>
          <div className="relative h-80 rounded-xl overflow-hidden shadow-lg">
            <Image 
              src="/images/about-us-story.jpg" 
              alt="Our Journey" 
              fill
              className="object-cover"
            />
          </div>
        </div>
      </div>

      {/* Our Mission */}
      <div className="bg-gray-50 py-16">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-gray-800 mb-4 text-center">Our Mission</h2>
          <p className="text-gray-600 text-center mb-12 max-w-3xl mx-auto">
            At GOLK Tourist Guide, we're driven by a clear purpose that shapes everything we do.
          </p>
          
          <div className="bg-white rounded-xl shadow-lg p-8 relative">
            <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-emerald-600 rounded-full w-16 h-16 flex items-center justify-center shadow-lg">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            
            <div className="text-center mt-6">
              <h3 className="text-2xl font-bold text-gray-800 mb-6">Transforming Tourism Through Technology</h3>
              <p className="text-gray-600 max-w-3xl mx-auto">
                Our mission is to enhance the travel experience in Sri Lanka by providing visitors with instant access 
                to accurate, comprehensive information through artificial intelligence. We aim to bridge the gap 
                between travelers and the wealth of attractions, accommodations, and services that Sri Lanka has to offer, 
                while promoting sustainable and respectful tourism that benefits both visitors and local communities.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
                <div>
                  <div className="w-14 h-14 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h4 className="font-bold text-gray-800 mb-2">Accessible Information</h4>
                  <p className="text-gray-600 text-sm">
                    Making reliable travel information accessible to all visitors through an intuitive AI assistant.
                  </p>
                </div>
                
                <div>
                  <div className="w-14 h-14 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                  </div>
                  <h4 className="font-bold text-gray-800 mb-2">Safety & Security</h4>
                  <p className="text-gray-600 text-sm">
                    Ensuring travelers have immediate access to emergency services and safety information when needed.
                  </p>
                </div>
                
                <div>
                  <div className="w-14 h-14 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                    </svg>
                  </div>
                  <h4 className="font-bold text-gray-800 mb-2">Cultural Connection</h4>
                  <p className="text-gray-600 text-sm">
                    Promoting deeper understanding and appreciation of Sri Lanka's rich culture and heritage.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Our Technology */}
      <div className="container mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-gray-800 mb-4 text-center">Our Technology</h2>
        <p className="text-gray-600 text-center mb-12 max-w-3xl mx-auto">
          GOLK Tourist Guide leverages cutting-edge technologies to deliver a seamless, intelligent travel assistant experience.
        </p>
        
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <div className="grid grid-cols-1 md:grid-cols-2">
            <div className="p-8">
              <h3 className="text-xl font-bold text-gray-800 mb-6">Powered by Innovation</h3>
              
              <div className="space-y-6">
                <div className="flex items-start">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <h4 className="font-bold text-gray-800 mb-1">Artificial Intelligence</h4>
                    <p className="text-gray-600 text-sm">
                      Our TourMate chatbot uses advanced language models to understand and respond to natural language queries about Sri Lanka tourism.
                    </p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <h4 className="font-bold text-gray-800 mb-1">Neo4j Graph Database</h4>
                    <p className="text-gray-600 text-sm">
                      Our knowledge is stored in a sophisticated graph database that captures relationships between locations, services, and attractions.
                    </p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <h4 className="font-bold text-gray-800 mb-1">Responsive Design</h4>
                    <p className="text-gray-600 text-sm">
                      Our application is built with Next.js and optimized for all devices, ensuring travelers can access information wherever they are.
                    </p>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 p-8 flex items-center justify-center">
              <div className="max-w-md">
                <div className="relative h-96 w-full">
                  <Image 
                    src="/images/tech-architecture.jpg" 
                    alt="Technology Architecture" 
                    fill
                    className="object-contain"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* The Team */}
      <div className="bg-gray-50 py-16">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-gray-800 mb-4 text-center">The Team</h2>
          <p className="text-gray-600 text-center mb-12 max-w-3xl mx-auto">
            Meet the dedicated individual behind the GOLK Tourist Guide project.
          </p>
          
          <div className="max-w-lg mx-auto bg-white rounded-xl shadow-lg overflow-hidden">
            <div className="flex flex-col md:flex-row">
              <div className="md:w-1/3 relative">
                <div className="h-60 md:h-full relative">
                  <Image 
                    src="/images/team-profile.jpg" 
                    alt="Korale Ariyaratne" 
                    fill
                    className="object-cover"
                  />
                </div>
              </div>
              <div className="md:w-2/3 p-6">
                <h3 className="text-xl font-bold text-gray-800 mb-1">Korale Ariyaratne</h3>
                <p className="text-emerald-600 text-sm mb-4">Project Developer & Creator</p>
                <p className="text-gray-600 mb-4">
                  Software Engineering student with a passion for artificial intelligence and tourism. 
                  Created GOLK Tourist Guide as a final year project to solve real-world problems in Sri Lanka's tourism sector.
                </p>
                <div className="space-x-2">
                  <a href="#" className="inline-block p-2 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors">
                    <svg className="h-5 w-5 text-gray-700" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                    </svg>
                  </a>
                  <a href="#" className="inline-block p-2 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors">
                    <svg className="h-5 w-5 text-gray-700" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-12 text-center">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Academic Support</h3>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Special thanks to Ms. Dulanjali Wijesekara for supervising this project and providing valuable guidance throughout its development.
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-emerald-700 py-16">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-white mb-6">Experience TourMate Now</h2>
          <p className="text-white/90 max-w-2xl mx-auto mb-8">
            See for yourself how our AI-powered assistant can enhance your Sri Lankan travel experience.
          </p>
          <button
            onClick={handleChatbotRedirect}
            className="bg-white text-emerald-700 hover:bg-gray-100 py-3 px-8 rounded-lg font-medium text-lg transition-colors"
          >
            Start Chatting with TourMate
          </button>
        </div>
      </div>
    </div>
  );
}