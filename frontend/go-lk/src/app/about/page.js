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
      <div className="relative h-[300px] w-full bg-emerald-700">
        <div className="absolute inset-0 flex items-center">
          <div className="container mx-auto px-6">
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">About Us</h1>
            <p className="text-xl text-white/90 max-w-2xl">
              Meet the creator behind Go-LK Tourist Guide and the mission to transform tourism in Sri Lanka
            </p>
          </div>
        </div>
      </div>

      {/* Our Story Section  */}
        <div className="container mx-auto px-6 py-16">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
          <h2 className="text-3xl font-bold text-gray-800 mb-6">Our Story</h2>
          <p className="text-gray-600 mb-4">
            The Go-LK Tourist Guide project was born from a simple observation: tourists in Sri Lanka 
            often struggle to find accurate, up-to-date information all in one place. They have to 
            consult multiple sources, which can be time-consuming and sometimes leads to outdated or 
            incorrect information.
          </p>
          <p className="text-gray-600 mb-4">
            As a final year project at NSBM Green University, I set out to solve this problem by creating 
            a comprehensive, AI-powered solution that would provide visitors with instant access to 
            reliable information about accommodations, attractions, and emergency services throughout 
            Sri Lanka.
          </p>
          <p className="text-gray-600">
            My focus on leveraging technology to enhance the tourism experience in Sri Lanka 
            has led to the development of TourMate, an AI assistant that combines cutting-edge 
            artificial intelligence with a deep knowledge of Sri Lanka's tourism landscape.
          </p>
            </div>
            <div className="relative h-96 rounded-xl overflow-hidden shadow-lg">
          <Image 
            src="/images/journey.png"
            alt="Our Journey" 
            fill
            className="object-cover"
          />
            </div>
          </div>
        </div>

        {/* Project Creator Section */}
      <div className="bg-gray-50 py-16">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-gray-800 mb-4 text-center">The Creator</h2>
          
          <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden mt-12">
            <div className="md:flex">
              <div className="md:w-1/3 relative">
                <div className="h-64 md:h-full relative">
                  <Image 
                    src="/images/profile.jpg" 
                    alt="Jayasanka Ariyaratne" 
                    fill
                    className="object-cover"
                  />
                </div>
              </div>
              <div className="md:w-2/3 p-8">
                <h3 className="text-2xl font-bold text-gray-800 mb-1">Jayasanka Ariyaratne</h3>
                <p className="text-emerald-600 text-sm mb-4">BSc (Hons) in Software Engineering</p>
                <p className="text-gray-600 mb-4">
                  I'm a Software Engineering student at NSBM Green University. 
                  I created GOLK Tourist Guide as my final year project to solve real-world problems in Sri Lanka's tourism sector.
                </p>
                <p className="text-gray-600 mb-4">
                  By combining my technical skills in web development, AI, and databases with my love for Sri Lanka's 
                  culture and beauty, I've developed a solution that aims to make travel planning easier and more 
                  personalized for visitors to Sri Lanka.
                </p>
                <div className="space-x-3 mt-4">
                  <a href="https://www.linkedin.com/in/jayasanka-ariyaratne/" target="_blank" rel="noopener noreferrer" className="inline-block p-2 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors">
                    <svg className="h-5 w-5 text-gray-700" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                    </svg>
                  </a>
                  <a href="https://github.com/10898415" target="_blank" rel="noopener noreferrer" className="inline-block p-2 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors">
                    <svg className="h-5 w-5 text-gray-700" fill="currentColor" viewBox="0 0 24 24">
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

      {/* University Section */}
      <div className="container mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">University</h2>
        
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <div className="grid grid-cols-1 md:grid-cols-2">
            <div className="p-8">
              <h3 className="text-2xl font-bold text-gray-800 mb-4">NSBM Green University</h3>
              <p className="text-gray-600 mb-4">
                This project was completed as part of the BSc (Hons) in Software Engineering program at NSBM Green University, 
                the first green university in South Asia. NSBM is committed to providing quality higher education and promoting 
                sustainable development.
              </p>
              <p className="text-gray-600 mb-4">
                As a student at NSBM, I've had access to state-of-the-art facilities and expert guidance that has 
                been instrumental in developing this AI-powered tourism guide.
              </p>
              <p className="text-gray-600">
                The project was completed under the supervision of the Department of Software Engineering, 
                with a focus on practical application of emerging technologies to solve real-world problems.
              </p>
            </div>
            <div className="relative h-80 md:h-auto">
              <Image 
                src="/images/nsbm.jpg" 
                alt="NSBM Green University" 
                fill
                className="object-cover"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Our Mission */}
      <div className="bg-gray-50 py-16">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">Our Mission</h2>
          
          <div className="bg-white rounded-xl shadow-lg p-8 relative">
            <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-emerald-600 rounded-full w-16 h-16 flex items-center justify-center shadow-lg">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            
            <div className="text-center mt-6">
              <h3 className="text-2xl font-bold text-gray-800 mb-6">Transforming Tourism Through Technology</h3>
              <p className="text-gray-600 max-w-3xl mx-auto">
                The mission of Go-LK Tourist Guide is to enhance the travel experience in Sri Lanka by providing visitors with instant access 
                to accurate, comprehensive information through artificial intelligence. The project aims to bridge the gap 
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