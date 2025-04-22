"use client";
import Image from 'next/image';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function ContactPage() {
  const router = useRouter();

  const handleChatbotRedirect = () => {
    router.push('/tourmate');
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <div className="relative h-[300px] w-full">
        <Image 
          src="/images/contact-banner.jpg" 
          alt="Contact Us" 
          fill
          priority
          className="object-cover"
        />
        <div className="absolute inset-0 bg-black/40 flex items-center">
          <div className="container mx-auto px-6">
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">Contact Us</h1>
            <p className="text-xl text-white/90 max-w-2xl">
              Learn more about GOLK Tourist Guide and how to get in touch
            </p>
          </div>
        </div>
      </div>

      {/* Contact Information Section */}
      <div className="container mx-auto px-6 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* About Project */}
          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-6">About This Project</h2>
            
            <div className="bg-white p-8 rounded-xl shadow-md mb-8">
              <p className="text-gray-600 mb-4">
                Go-LK Tourist Guide is a final year project developed as part of the BSc (Hons) in Software Engineering program.
              </p>
              <p className="text-gray-600 mb-4">
                This project was created to help tourists in Sri Lanka find accurate, up-to-date information about accommodations, attractions, and emergency services in one convenient place.
              </p>
              <p className="text-gray-600">
                The system is powered by AI and a Neo4j graph database to provide personalized recommendations and real-time information to travelers.
              </p>
            </div>

            <h3 className="text-xl font-bold text-gray-800 mb-4">Project Information</h3>
            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="space-y-4">
                <div className="flex items-start">
                  <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <h4 className="font-bold text-gray-800">Developer</h4>
                    <p className="text-gray-600">Jayasanka Ariyaratne</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <h4 className="font-bold text-gray-800">University</h4>
                    <p className="text-gray-600">Plymouth University (NSBM Green University)</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <h4 className="font-bold text-gray-800">Supervisor</h4>
                    <p className="text-gray-600">Ms. Dulanjali Wijesekara</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <h4 className="font-bold text-gray-800">Project Year</h4>
                    <p className="text-gray-600">2024/2025</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <h4 className="font-bold text-gray-800">Degree Program</h4>
                    <p className="text-gray-600">BSc (Hons) in Software Engineering</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* GitHub and Project Links */}
          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Project Resources</h2>
            
            <div className="bg-white rounded-xl shadow-md p-6 mb-8">
              <h3 className="text-lg font-bold text-gray-800 mb-4">GitHub Repository</h3>
              <p className="text-gray-600 mb-4">
                This project is open source. You can view the source code, contribute, or report issues through the GitHub repository.
              </p>
              <a 
                href="https://github.com/yourusername/golk-tourist-guide" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="inline-flex items-center bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg transition-colors"
              >
                <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                  <path fillRule="evenodd" clipRule="evenodd" d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.207 11.387.6.113.793-.258.793-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.73.083-.73 1.205.085 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.195.69.8.574C20.565 21.797 24 17.3 24 12c0-6.63-5.37-12-12-12z" />
                </svg>
                View on GitHub
              </a>
            </div>
            
            <div className="bg-white rounded-xl shadow-md p-6 mb-8">
              <h3 className="text-lg font-bold text-gray-800 mb-4">Technology Stack</h3>
              <ul className="space-y-2">
                
                <li className="flex items-center">
                  <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                    <svg className="h-5 w-5 text-green-600" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M13.95 13.5h-3.9c-.152 0-.3.049-.424.14-.124.09-.225.221-.285.37l-1.95 5.5c-.1.266.03.56.29.66.252.081.528-.063.63-.32l1.854-5.22h3.235c.153 0 .3-.05.426-.142.125-.092.225-.222.286-.372l2.68-7.5c.086-.241.016-.512-.177-.68-.193-.17-.48-.186-.69-.037l-8.574 6.07h-3.38c-.152 0-.3.05-.424.141-.125.091-.225.222-.285.371l-1.95 5.5c-.1.266.03.56.29.66.252.081.528-.063.63-.32l1.854-5.22h3.235c.153 0 .3-.05.426-.142.125-.092.225-.222.286-.372l2.68-7.5c.086-.241.016-.512-.177-.68-.193-.17-.48-.186-.69-.037l-8.573 6.07h-3.313c-.267 0-.481.21-.481.47 0 .26.214.47.481.47h3.5c.152 0 .3-.49.424-.14.124-.091.225-.221.285-.37l1.95-5.5c.1-.266-.03-.56-.29-.66-.252-.081-.528.063-.63.32L6.385 12h-3.214L11 4.52 8.5 11.5h3.95L15 4.52z" />
                    </svg>
                  </div>
                  <span className="text-gray-700">Neo4j (Graph database)</span>
                </li>
                <li className="flex items-center">
                  <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center mr-3">
                    <svg className="h-5 w-5 text-purple-600" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M16.934 8.519a1.044 1.044 0 0 1 .303.23c.265.301.5.643.479 1.061-.21.404-.441.578-.857.584a2.822 2.822 0 0 1-.549-.067 3.997 3.997 0 0 0-.709-.116c-.594-.064-1.004.166-1.218.6-.206.416-.15.842.194 1.223a1.699 1.699 0 0 0 .14.17c.381.43.885.863 1.343 1.309.464.452.846.943 1.154 1.541.301.599.43 1.199.365 1.829-.073.711-.357 1.329-.978 1.794-.668.486-1.4.684-2.25.423-.817-.235-1.345-.781-1.399-1.599-.02-.339.066-.689.263-1.049.283-.524.745-.995 1.307-1.389.271-.189.511-.395.555-.676a.915.915 0 0 0-.113-.684c-.119-.17-.279-.307-.393-.465-.36-.497-.496-1.032-.361-1.644.131-.576.489-1.044 1.058-1.299.273-.122.552-.2.813-.349a1.331 1.331 0 0 0 .241-.214c.093-.108.182-.221.252-.339a.93.93 0 0 0 .088-.365c-.004-.113-.037-.212-.121-.3zm-3.496 6.676a2.651 2.651 0 0 0-.262.209c-.457.415-.783.959-.974 1.533-.051.154-.08.304-.08.461.001.141.02.245.129.349.249.226.657.225.9-.004a.877.877 0 0 0 .21-.37 2.545 2.545 0 0 0-.083-.95c-.05-.216-.139-.424-.28-.603-.106-.131-.24-.214-.33-.288l-.232-.179z" />
                      <path d="M11.55 20.649c-1.67-.359-3.197-.978-4.556-1.976A10.003 10.003 0 0 1 3.132 14.6c-.819-1.966-1.089-3.996-.734-6.094.225-1.32.706-2.544 1.426-3.645 1.095-1.687 2.587-2.967 4.334-3.9 1.455-.78 3.017-1.213 4.694-1.208 1.699.008 3.307.458 4.766 1.337 1.599.961 2.894 2.252 3.855 3.839.778 1.287 1.272 2.677 1.447 4.184.181 1.568-.034 3.016-.65 4.434-.935 2.157-2.546 3.71-4.41 4.895a14.655 14.655 0 0 1-5.446 2.034 15.677 15.677 0 0 1-1.873.172z" />
                    </svg>
                  </div>
                  <span className="text-gray-700">Python</span>
                </li>
                <li className="flex items-center">
                  <div className="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center mr-3">
                    <svg className="h-5 w-5 text-yellow-600" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M22.282 9.821a5.985 5.985 0 0 0-.516-4.91 6.046 6.046 0 0 0-6.51-2.9A6.065 6.065 0 0 0 4.981 4.18a5.985 5.985 0 0 0-3.998 2.9 6.046 6.046 0 0 0 .743 7.097 5.98 5.98 0 0 0 .51 4.911 6.051 6.051 0 0 0 6.515 2.9A5.985 5.985 0 0 0 13.26 24a6.056 6.056 0 0 0 5.772-4.206 5.99 5.99 0 0 0 3.997-2.9 6.056 6.056 0 0 0-.747-7.073z" />
                    </svg>
                  </div>
                  <span className="text-gray-700">AI (LLM Integration)</span>
                </li>
                <li className="flex items-center">
                  <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                    <svg className="h-5 w-5 text-blue-600" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M11.572 0c-.176 0-.31.001-.358.007-.092.016-.19.057-.282.11-.22.127-.506.47-.986 1.01-.792.865-1.965 2.145-3.158 3.386-2.895 3.008-6.412 6.652-6.788 7.04-1.158 1.204-1.545 2.596-1.045 3.927.35.935 1.055 1.73 1.867 2.22.345.21.703.35 1.01.41.545.106 1.235.075 1.89-.07l.026-.007.624-.195c.992-.315 2.371-.751 3.844-1.25 2.953-.996 5.694-2.097 7.628-3.054 2.158-1.08 3.315-1.935 3.674-2.79.113-.27.127-.492.089-.7l-.007-.045c-.085-.413-.442-.794-.86-1.015-.647-.341-1.347-.373-1.999-.297a11.11 11.11 0 0 0-.888.176l-.477.12c-1.06.28-2.395.629-3.516.93-1.736.473-3.634.928-4.287 1.075" />
                    </svg>
                  </div>
                  <span className="text-gray-700">Next.js</span>
                </li>
              </ul>
            </div>

            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-lg font-bold text-gray-800 mb-4">Connect with TourMate</h3>
              <p className="text-gray-600 mb-4">
                The best way to experience GOLK Tourist Guide is to interact with TourMate, our AI-powered travel assistant.
              </p>
              <button
                onClick={handleChatbotRedirect}
                className="w-full py-3 px-4 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-medium transition-colors flex items-center justify-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                Chat with TourMate
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* University Affiliation */}
      <div className="bg-gray-50 py-12">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">University Affiliation</h2>
          <div className="flex justify-center items-center mb-6 space-x-8">
            <div className="w-24 h-24 relative">
              <Image 
                src="/images/nsbm-logo.png" 
                alt="NSBM Logo" 
                fill
                className="object-contain"
              />
            </div>
            <div className="w-24 h-24 relative">
              <Image 
                src="/images/plymouth.png" 
                alt="Plymouth University Logo" 
                fill
                className="object-contain"
              />
            </div>
          </div>
          <p className="text-gray-600 max-w-2xl mx-auto mb-4">
            This project was developed as the final year project of BSc (Hons) in Software Engineering 
            program at NSBM Green University that offered by Plymouth University, UK.
          </p>

        </div>
      </div>
    </div>
  );
}