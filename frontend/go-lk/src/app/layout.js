"use client";

import "./globals.css";
import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';

export default function RootLayout({ children }) {
  const pathname = usePathname();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  // Handle scroll effect for navbar
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close mobile menu when route changes
  useEffect(() => {
    setIsMenuOpen(false);
  }, [pathname]);

  return (
    <html lang="en">
      <head>
        <title>Go-LK Tourist Guide</title>
        <meta name="description" content="GOLK Tourist Guide provides AI-powered assistance for travelers in Sri Lanka, offering accurate information about accommodations, attractions, and emergency services." />
      </head>
      <body className="bg-gray-50 text-gray-800 min-h-screen flex flex-col">
        {/* Navigation */}
        <header className={`sticky top-0 z-50 transition-all duration-300 ${scrolled ? 'bg-white shadow-md py-2' : 'bg-white/80 backdrop-blur-md py-4'}`}>
          <div className="container mx-auto px-6">
            <nav className="flex items-center justify-between">
              {/* Logo */}
              <Link href="/" className="flex items-center space-x-3">
                <div className="relative w-10 h-10">
                  <Image 
                    src="/images/logo.png" 
                    alt="GOLK Logo" 
                    fill
                    className="object-contain"
                  />
                </div>
                <span className="text-xl font-bold text-gray-800">Go-LK </span>
              </Link>
              
              {/* Desktop Navigation */}
              <div className="hidden md:flex items-center space-x-8">
                <Link 
                  href="/" 
                  className={`font-medium transition-colors ${
                    pathname === '/' 
                      ? 'text-emerald-600 border-b-2 border-emerald-600' 
                      : 'text-gray-600 hover:text-emerald-600'
                  }`}
                >
                  Home
                </Link>
                <Link 
                  href="/tourmate" 
                  className={`font-medium transition-colors ${
                    pathname === '/tourmate' 
                      ? 'text-emerald-600 border-b-2 border-emerald-600' 
                      : 'text-gray-600 hover:text-emerald-600'
                  }`}
                >
                  TourMate
                </Link>
                <Link 
                  href="/about" 
                  className={`font-medium transition-colors ${
                    pathname === '/about' 
                      ? 'text-emerald-600 border-b-2 border-emerald-600' 
                      : 'text-gray-600 hover:text-emerald-600'
                  }`}
                >
                  About Us
                </Link>
                
                <Link 
                  href="/contact" 
                  className={`font-medium transition-colors ${
                    pathname === '/contact' 
                      ? 'text-emerald-600 border-b-2 border-emerald-600' 
                      : 'text-gray-600 hover:text-emerald-600'
                  }`}
                >
                  Contact
                </Link>
                
                <Link 
                  href="/tourmate" 
                  className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-full font-medium transition-colors"
                >
                  Ask TourMate
                </Link>
              </div>
              
              {/* Mobile Menu Button */}
              <button 
                className="md:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100 focus:outline-none"
                onClick={() => setIsMenuOpen(!isMenuOpen)}
              >
                {isMenuOpen ? (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                )}
              </button>
            </nav>
          </div>
          
          {/* Mobile Menu */}
          {isMenuOpen && (
            <div className="md:hidden bg-white border-t border-gray-200 py-2 shadow-lg">
              <div className="container mx-auto px-6 space-y-1">
                <Link 
                  href="/" 
                  className={`block py-3 px-4 rounded-lg ${
                    pathname === '/' 
                      ? 'bg-emerald-50 text-emerald-600 font-medium' 
                      : 'text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  Home
                </Link>
                <Link 
                  href="/tourmate" 
                  className={`block py-3 px-4 rounded-lg ${
                    pathname === '/tourmate' 
                      ? 'bg-emerald-50 text-emerald-600 font-medium' 
                      : 'text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  TourMate
                </Link>
                <Link 
                  href="/about" 
                  className={`block py-3 px-4 rounded-lg ${
                    pathname === '/about' 
                      ? 'bg-emerald-50 text-emerald-600 font-medium' 
                      : 'text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  About Us
                </Link>
                
                <Link 
                  href="/contact" 
                  className={`block py-3 px-4 rounded-lg ${
                    pathname === '/contact' 
                      ? 'bg-emerald-50 text-emerald-600 font-medium' 
                      : 'text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  Contact
                </Link>
                
                <Link 
                  href="/tourmate" 
                  className="block py-3 px-4 my-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-medium text-center"
                >
                  Ask TourMate Now
                </Link>
              </div>
            </div>
          )}
        </header>
        
        {/* Main Content */}
        <main className="flex-grow">{children}</main>
        
        {/* Footer */}
        <footer className="bg-gray-800 text-white py-12">
          <div className="container mx-auto px-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              {/* Logo & About */}
              <div className="col-span-1 md:col-span-1">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="relative w-10 h-10 bg-white rounded-full p-1">
                    <Image 
                      src="/images/logo.png" 
                      alt="GOLK Logo" 
                      fill
                      className="object-contain"
                    />
                  </div>
                  <span className="text-xl font-bold">GOLK</span>
                </div>
                <p className="text-gray-400 text-sm">
                  Your AI-powered guide to exploring the wonders of Sri Lanka. Get accurate information and personalized recommendations.
                </p>
              </div>
              
              {/* Quick Links */}
              <div>
                <h3 className="text-lg font-bold mb-4">Quick Links</h3>
                <ul className="space-y-3">
                  <li>
                    <Link href="/" className="text-gray-400 hover:text-white transition-colors">
                      Home
                    </Link>
                  </li>
                  <li>
                    <Link href="/tourmate" className="text-gray-400 hover:text-white transition-colors">
                      TourMate
                    </Link>
                  </li>
                  <li>
                    <Link href="/about" className="text-gray-400 hover:text-white transition-colors">
                      About Us
                    </Link>
                  </li>

                  <li>
                    <Link href="/contact" className="text-gray-400 hover:text-white transition-colors">
                      Contact
                    </Link>
                  </li>
                </ul>
              </div>
              
              {/* Destinations */}
              <div>
                <h3 className="text-lg font-bold mb-4">Popular Destinations</h3>
                <ul className="space-y-3">
                  <li>
                    <Link href="/tourmate" className="text-gray-400 hover:text-white transition-colors">
                      Colombo
                    </Link>
                  </li>
                  <li>
                    <Link href="/tourmate" className="text-gray-400 hover:text-white transition-colors">
                      Kandy
                    </Link>
                  </li>
                  <li>
                    <Link href="/tourmate" className="text-gray-400 hover:text-white transition-colors">
                      Galle
                    </Link>
                  </li>
                  <li>
                    <Link href="/tourmate" className="text-gray-400 hover:text-white transition-colors">
                      Sigiriya
                    </Link>
                  </li>
                  <li>
                    <Link href="/tourmate" className="text-gray-400 hover:text-white transition-colors">
                      Ella
                    </Link>
                  </li>
                </ul>
              </div>
              
              {/* Connect */}
              <div>
                <h3 className="text-lg font-bold mb-4">Connect</h3>
                <ul className="space-y-3">
                  <li className="flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-emerald-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    <a href="mailto:contact@golktourguide.com" className="text-gray-400 hover:text-white transition-colors">
                      contact@golktourguide.com
                    </a>
                  </li>
                  <li className="flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-emerald-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span className="text-gray-400">
                      NSBM Green University, Sri Lanka
                    </span>
                  </li>
                  
                  <li className="pt-2">
                    <div className="flex space-x-4">
                      <a href="#" className="text-gray-400 hover:text-white transition-colors">
                        <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                        </svg>
                      </a>
                      <a href="#" className="text-gray-400 hover:text-white transition-colors">
                        <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723 10.016 10.016 0 01-3.127 1.195 4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.937 4.937 0 004.604 3.417 9.868 9.868 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.054 0 13.999-7.496 13.999-13.986 0-.209 0-.42-.015-.63a9.936 9.936 0 002.46-2.548l-.047-.02z"/>
                        </svg>
                      </a>
                      <a href="#" className="text-gray-400 hover:text-white transition-colors">
                        <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path d="M12 0C8.74 0 8.333.015 7.053.072 5.775.132 4.905.333 4.14.63c-.789.306-1.459.717-2.126 1.384S.935 3.35.63 4.14C.333 4.905.131 5.775.072 7.053.012 8.333 0 8.74 0 12s.015 3.667.072 4.947c.06 1.277.261 2.148.558 2.913.306.788.717 1.459 1.384 2.126.667.666 1.336 1.079 2.126 1.384.766.296 1.636.499 2.913.558C8.333 23.988 8.74 24 12 24s3.667-.015 4.947-.072c1.277-.06 2.148-.262 2.913-.558.788-.306 1.459-.718 2.126-1.384.666-.667 1.079-1.335 1.384-2.126.296-.765.499-1.636.558-2.913.06-1.28.072-1.687.072-4.947s-.015-3.667-.072-4.947c-.06-1.277-.262-2.149-.558-2.913-.306-.789-.718-1.459-1.384-2.126C21.319 1.347 20.651.935 19.86.63c-.765-.297-1.636-.499-2.913-.558C15.667.012 15.26 0 12 0zm0 2.16c3.203 0 3.585.016 4.85.071 1.17.055 1.805.249 2.227.415.562.217.96.477 1.382.896.419.42.679.819.896 1.381.164.422.36 1.057.413 2.227.057 1.266.07 1.646.07 4.85s-.015 3.585-.074 4.85c-.061 1.17-.256 1.805-.421 2.227-.224.562-.479.96-.899 1.382-.419.419-.824.679-1.38.896-.42.164-1.065.36-2.235.413-1.274.057-1.649.07-4.859.07-3.211 0-3.586-.015-4.859-.074-1.171-.061-1.816-.256-2.236-.421-.569-.224-.96-.479-1.379-.899-.421-.419-.69-.824-.9-1.38-.165-.42-.359-1.065-.42-2.235-.045-1.26-.061-1.649-.061-4.844 0-3.196.016-3.586.061-4.861.061-1.17.255-1.814.42-2.234.21-.57.479-.96.9-1.381.419-.419.81-.689 1.379-.898.42-.166 1.051-.361 2.221-.421 1.275-.045 1.65-.06 4.859-.06l.045.03zm0 3.678c-3.405 0-6.162 2.76-6.162 6.162 0 3.405 2.76 6.162 6.162 6.162 3.405 0 6.162-2.76 6.162-6.162 0-3.405-2.76-6.162-6.162-6.162zM12 16c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4zm7.846-10.405c0 .795-.646 1.44-1.44 1.44-.795 0-1.44-.646-1.44-1.44 0-.794.646-1.439 1.44-1.439.793-.001 1.44.645 1.44 1.439z"/>
                        </svg>
                      </a>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
            
            {/* Copyright */}
            <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400 text-sm">
              <p>&copy; {new Date().getFullYear()} GOLK Tourist Guide. All rights reserved.</p>
              <p className="mt-2">A project by Korale Ariyaratne | Student ID: 10898415</p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}