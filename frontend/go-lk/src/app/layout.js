"use client"; // For Next.js 13 App Router

import "./globals.css"; // Tailwind CSS imports
import Navbar from "./components/Navbar";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-100 text-gray-800">
        {/* Top navbar always visible */}
        <Navbar />
        {/* Page content (the chat) */}
        <div className="container mx-auto mt-4">{children}</div>
      </body>
    </html>
  );
}
