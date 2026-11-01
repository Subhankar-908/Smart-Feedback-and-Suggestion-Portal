import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { MessageSquareText, LogOut, User, ShieldCheck } from 'lucide-react';

const Navbar = () => {
  const { user, logout, isStudent, isAdmin } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-30 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Brand / Logo */}
          <Link
            to={isAdmin ? '/admin/dashboard' : '/student/dashboard'}
            className="flex items-center gap-2.5 group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20 group-hover:scale-105 transition-transform">
              <MessageSquareText className="w-5 h-5" />
            </div>
            <div>
              <span className="font-bold text-gray-900 text-lg leading-none block">
                Smart Feedback Portal
              </span>
              <span className="text-xs text-gray-500 font-medium">
                Educational Feedback & NLP Analytics
              </span>
            </div>
          </Link>

          {/* User Profile & Actions */}
          {user ? (
            <div className="flex items-center gap-4">
              <div className="hidden sm:flex items-center gap-3 bg-gray-50 border border-gray-200/80 px-3 py-1.5 rounded-lg">
                <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-semibold text-sm">
                  {user.name ? user.name.charAt(0).toUpperCase() : 'U'}
                </div>
                <div className="text-left">
                  <div className="text-sm font-semibold text-gray-800 leading-tight flex items-center gap-1.5">
                    {user.name}
                    {isAdmin ? (
                      <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-bold bg-purple-100 text-purple-800 border border-purple-200">
                        ADMIN
                      </span>
                    ) : (
                      <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800 border border-blue-200">
                        STUDENT
                      </span>
                    )}
                  </div>
                  <div className="text-xs text-gray-500">
                    {user.department || user.email}
                  </div>
                </div>
              </div>

              <button
                onClick={handleLogout}
                className="inline-flex items-center gap-1.5 px-3.5 py-2 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors border border-red-200/60"
                title="Log Out"
              >
                <LogOut className="w-4 h-4" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <Link
                to="/login"
                className="text-sm font-medium text-gray-700 hover:text-blue-600 px-3 py-2 transition-colors"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg shadow-sm transition-colors"
              >
                Register
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
