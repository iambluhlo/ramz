import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X, TrendingUp, Wallet, Settings, LogOut } from 'lucide-react';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'خانه', icon: TrendingUp },
    { path: '/dashboard', label: 'داشبورد', icon: TrendingUp },
    { path: '/trading', label: 'معاملات', icon: TrendingUp },
    { path: '/wallet', label: 'کیف پول', icon: Wallet },
    { path: '/admin', label: 'پنل مدیریت', icon: Settings },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="bg-dark-800 border-b border-dark-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 space-x-reverse">
            <TrendingUp className="h-8 w-8 text-primary-500" />
            <span className="text-xl font-bold text-white">بیت‌کوین پلاس</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8 space-x-reverse">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center space-x-2 space-x-reverse px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive(item.path)
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-300 hover:bg-dark-700 hover:text-white'
                }`}
              >
                <item.icon className="h-4 w-4" />
                <span>{item.label}</span>
              </Link>
            ))}
          </div>

          {/* Auth Buttons */}
          <div className="hidden md:flex items-center space-x-4 space-x-reverse">
            <Link
              to="/login"
              className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              ورود
            </Link>
            <Link
              to="/register"
              className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
            >
              ثبت نام
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-300 hover:text-white focus:outline-none"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 space-x-reverse px-3 py-2 rounded-md text-base font-medium transition-colors ${
                    isActive(item.path)
                      ? 'bg-primary-600 text-white'
                      : 'text-gray-300 hover:bg-dark-700 hover:text-white'
                  }`}
                  onClick={() => setIsOpen(false)}
                >
                  <item.icon className="h-5 w-5" />
                  <span>{item.label}</span>
                </Link>
              ))}
              <div className="border-t border-dark-700 pt-4">
                <Link
                  to="/login"
                  className="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-dark-700 transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  ورود
                </Link>
                <Link
                  to="/register"
                  className="block px-3 py-2 rounded-md text-base font-medium bg-primary-600 text-white hover:bg-primary-700 transition-colors mt-2"
                  onClick={() => setIsOpen(false)}
                >
                  ثبت نام
                </Link>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;