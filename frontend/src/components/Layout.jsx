import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Plane, User, LogOut, Menu, X } from 'lucide-react';
import { useState } from 'react';

const Layout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="min-h-screen flex flex-col bg-aviation-50">
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link to="/" className="flex items-center gap-2 text-aviation-600 hover:text-aviation-700 transition-colors">
                <Plane className="h-8 w-8 rotate-[-45deg]" />
                <span className="font-bold text-xl tracking-tight">FlyClaim</span>
              </Link>
            </div>

            {/* Desktop Menu */}
            <div className="hidden md:flex items-center space-x-4">
              <Link to="/track" className="text-slate-600 hover:text-aviation-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                Track Claim
              </Link>

              {user ? (
                <div className="flex items-center gap-4">
                  <Link to="/dashboard" className="text-slate-600 hover:text-aviation-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                    Dashboard
                  </Link>
                  <div className="flex items-center gap-2 pl-4 border-l border-slate-200">
                    <div className="flex flex-col text-right">
                      <span className="text-sm font-semibold text-slate-700">{user.name}</span>
                      <span className="text-xs text-slate-500">{user.phone}</span>
                    </div>
                    <button
                      onClick={handleLogout}
                      className="p-2 text-slate-400 hover:text-red-500 transition-colors"
                      title="Logout"
                    >
                      <LogOut size={20} />
                    </button>
                  </div>
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <Link to="/login" className="text-slate-600 hover:text-aviation-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                    Log In
                  </Link>
                  <Link to="/signup" className="bg-aviation-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-aviation-700 transition-colors shadow-sm hover:shadow-md">
                    Sign Up
                  </Link>
                </div>
              )}
            </div>

            {/* Mobile menu button */}
            <div className="flex items-center md:hidden">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="text-slate-500 hover:text-aviation-600 p-2"
              >
                {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden bg-white border-t border-slate-100 pb-4">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              <Link
                to="/track"
                className="block px-3 py-2 rounded-md text-base font-medium text-slate-600 hover:text-aviation-600 hover:bg-aviation-50"
                onClick={() => setIsMenuOpen(false)}
              >
                Track Claim
              </Link>

              {user ? (
                <>
                  <Link
                    to="/dashboard"
                    className="block px-3 py-2 rounded-md text-base font-medium text-slate-600 hover:text-aviation-600 hover:bg-aviation-50"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Dashboard
                  </Link>
                  <button
                    onClick={() => {
                      handleLogout();
                      setIsMenuOpen(false);
                    }}
                    className="w-full text-left px-3 py-2 rounded-md text-base font-medium text-red-500 hover:bg-red-50"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="block px-3 py-2 rounded-md text-base font-medium text-slate-600 hover:text-aviation-600 hover:bg-aviation-50"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Log In
                  </Link>
                  <Link
                    to="/signup"
                    className="block px-3 py-2 rounded-md text-base font-medium text-aviation-600 hover:bg-aviation-50"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </nav>

      <main className="flex-grow">
        {children}
      </main>

      <footer className="bg-white border-t border-slate-200 mt-auto">
        <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center gap-2 mb-4 md:mb-0">
              <Plane className="h-6 w-6 text-aviation-400 rotate-[-45deg]" />
              <span className="text-slate-600 font-medium">FlyClaim AI</span>
            </div>
            <p className="text-slate-400 text-sm">
              &copy; {new Date().getFullYear()} FlyClaim AI. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
