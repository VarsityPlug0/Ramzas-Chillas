import React, { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useApp } from '../context/CartContext'
import { useCart } from '../context/CartContext'
import { motion } from 'framer-motion'

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const { getCartCount } = useCart()
  const { siteSettings } = useApp()
  const [cartCount, setCartCount] = useState(0)
  const location = useLocation()

  useEffect(() => {
    setCartCount(getCartCount())
  }, [getCartCount])

  // Update cart count when cart changes
  useEffect(() => {
    const handleStorageChange = () => {
      setCartCount(getCartCount())
    }

    window.addEventListener('storage', handleStorageChange)
    return () => window.removeEventListener('storage', handleStorageChange)
  }, [getCartCount])

  // Navigation links using dynamic site settings
  const navLinks = [
    { name: siteSettings?.nav_home_text || 'Home', path: '/' },
    { name: siteSettings?.nav_menu_text || 'Menu', path: '/menu' },
    { name: siteSettings?.nav_about_text || 'About', path: '/about' },
    { name: siteSettings?.nav_contact_text || 'Contact', path: '/contact' },
    { name: 'Track Order', path: '/order' },
  ]

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50 transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-3 group">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-400 to-primary-600 rounded-xl flex items-center justify-center transform group-hover:scale-105 transition-transform duration-200">
                <i className="fas fa-fire text-white text-lg"></i>
              </div>
              <div className="hidden sm:block">
                <h1 className="text-xl font-bold text-gray-900">
                  {siteSettings?.site_name || "Ramza's Chillas"}
                </h1>
                <p className="text-sm text-gray-600 -mt-1">
                  {siteSettings?.site_description || 'Chill Vibes • Hot Food'}
                </p>
              </div>
              {/* Mobile logo only */}
              <div className="sm:hidden">
                <h1 className="text-lg font-bold text-gray-900">
                  {siteSettings?.site_name || "Ramza's Chillas"}
                </h1>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`${
                  location.pathname === link.path
                    ? 'text-primary-600 font-medium'
                    : 'text-gray-700 hover:text-primary-600'
                } px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200`}
              >
                {link.name}
              </Link>
            ))}
          </div>

          {/* Cart and Mobile Menu */}
          <div className="flex items-center space-x-4">
            {/* Cart Button */}
            <Link
              to="/cart"
              className="relative bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-xl font-semibold transition-all duration-200 flex items-center space-x-2 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              <i className="fas fa-shopping-cart"></i>
              <span className="hidden sm:inline">
                {siteSettings?.nav_cart_text || 'Cart'}
              </span>
              {cartCount > 0 && (
                <motion.span
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center animate-pulse"
                  aria-label={`Cart has ${cartCount} items`}
                >
                  {cartCount}
                </motion.span>
              )}
            </Link>

            {/* Mobile Menu Button */}
            <button
              className="md:hidden p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors duration-200"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-label="Toggle mobile menu"
            >
              <i className="fas fa-bars"></i>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-white border-t border-gray-200"
          >
            <div className="px-2 pt-2 pb-3 space-y-1">
              {navLinks.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`${
                    location.pathname === link.path
                      ? 'text-primary-600 font-medium'
                      : 'text-gray-700 hover:text-primary-600'
                  } block px-3 py-2 rounded-lg text-base font-medium hover:bg-gray-50 transition-colors duration-200`}
                  onClick={() => setIsMenuOpen(false)}
                >
                  {link.name}
                </Link>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </nav>
  )
}

export default Navbar