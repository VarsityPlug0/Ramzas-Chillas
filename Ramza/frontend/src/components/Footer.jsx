import React from 'react'
import { useApp } from '../context/CartContext'

const Footer = () => {
  const { siteSettings } = useApp()
  
  // Quick links using dynamic site settings
  const quickLinks = [
    { name: siteSettings?.nav_home_text || 'Home', path: '/' },
    { name: siteSettings?.nav_menu_text || 'Menu', path: '/menu' },
    { name: siteSettings?.nav_about_text || 'About', path: '/about' },
    { name: siteSettings?.nav_contact_text || 'Contact', path: '/contact' },
  ]

  return (
    <footer className="bg-gray-900 text-white mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="md:col-span-2">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-400 to-primary-600 rounded-xl flex items-center justify-center">
                <i className="fas fa-fire text-white"></i>
              </div>
              <div>
                <h3 className="text-xl font-bold">
                  {siteSettings?.site_name || "Ramza's Chillas"}
                </h3>
                <p className="text-gray-300 text-sm">
                  {siteSettings?.site_description || 'Chill Vibes • Hot Food'}
                </p>
              </div>
            </div>
            <p className="text-gray-300 mb-6 max-w-md">
              {siteSettings?.footer_description || 'Serving the finest food with fresh ingredients and chill vibes since 2024. Your go-to spot for quality meals in a relaxed atmosphere.'}
            </p>
            <div className="flex space-x-4">
              {siteSettings?.facebook_url && (
                <a
                  href={siteSettings.facebook_url}
                  className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-primary-600 transition-colors duration-200"
                  aria-label="Facebook"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <i className="fab fa-facebook-f"></i>
                </a>
              )}
              {siteSettings?.instagram_url && (
                <a
                  href={siteSettings.instagram_url}
                  className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-primary-600 transition-colors duration-200"
                  aria-label="Instagram"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <i className="fab fa-instagram"></i>
                </a>
              )}
              {siteSettings?.twitter_url && (
                <a
                  href={siteSettings.twitter_url}
                  className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-primary-600 transition-colors duration-200"
                  aria-label="Twitter"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <i className="fab fa-twitter"></i>
                </a>
              )}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              {quickLinks.map((link) => (
                <li key={link.path}>
                  <a
                    href={link.path}
                    className="text-gray-300 hover:text-white transition-colors duration-200"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Contact Info</h4>
            <div className="space-y-3 text-gray-300">
              <div className="flex items-center space-x-3">
                <i className="fas fa-map-marker-alt text-primary-400"></i>
                <span>{siteSettings?.address || '123 Chill Street, Island City'}</span>
              </div>
              <div className="flex items-center space-x-3">
                <i className="fas fa-phone text-primary-400"></i>
                <span>{siteSettings?.phone_number || '(555) 123-CHILL'}</span>
              </div>
              <div className="flex items-center space-x-3">
                <i className="fas fa-envelope text-primary-400"></i>
                <span>{siteSettings?.email || 'hello@ramzaschillas.com'}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>{siteSettings?.footer_copyright || '© 2024 Ramza\'s Chillas. All rights reserved.'}</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer