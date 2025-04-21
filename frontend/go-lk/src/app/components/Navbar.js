export default function Navbar() {
  return (
    <nav className="bg-white shadow p-4 flex items-center justify-between">
      {/* Left: Logo + Title */}
      <div className="flex items-center space-x-2">
        <img
          src="/logo.png"
          alt="GO-LK Logo"
          className="h-6 w-6 object-contain"
        />
        <span className="font-bold text-lg">GO-LK</span>
      </div>

      {/* Right: Nav Links */}
      <div className="space-x-6">
        <a href="#" className="hover:underline">
          Home
        </a>
        <a href="#" className="hover:underline">
          TourMate
        </a>
        <a href="#" className="hover:underline">
          AboutUs
        </a>
        <a href="#" className="hover:underline">
          ContactUs
        </a>
      </div>
    </nav>
  );
}