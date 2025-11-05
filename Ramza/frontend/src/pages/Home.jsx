import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useApp } from '../context/CartContext'

const Home = () => {
  const { featuredItems, categories, siteSettings, contentSections, testimonials, loading, error } = useApp()

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-primary-500 mb-4"></div>
        <p className="text-xl text-gray-700">Loading delicious experience...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-screen">
        <div className="text-2xl text-red-500 mb-4">Oops! Something went wrong.</div>
        <p className="text-gray-700 mb-4">{error}</p>
        <button 
          onClick={() => window.location.reload()} 
          className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 rounded-2xl font-semibold transition-all duration-300"
        >
          Try Again
        </button>
      </div>
    )
  }

  // Get content sections
  const homeHeroSection = contentSections?.home_hero || {}
  const homeFeaturesSection = contentSections?.home_features || {}
  const homeCtaSection = contentSections?.home_cta || {}

  return (
    <div>
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-gray-800 via-gray-900 to-black text-white overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div 
            className="absolute inset-0" 
            style={{
              backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cdefs%3E%3Cpattern id='grain' width='100' height='100' patternUnits='userSpaceOnUse'%3E%3Ccircle cx='25' cy='25' r='1' fill='%23ffffff'/%3E%3Ccircle cx='75' cy='75' r='1' fill='%23ffffff'/%3E%3Ccircle cx='50' cy='10' r='0.5' fill='%23ffffff'/%3E%3Ccircle cx='10' cy='60' r='0.5' fill='%23ffffff'/%3E%3Ccircle cx='90' cy='30' r='0.5' fill='%23ffffff'/%3E%3C/pattern%3E%3C/defs%3E%3Crect width='100' height='100' fill='url(%23grain)'/%3E%3C/svg%3E")`,
              backgroundSize: '100px 100px'
            }}
          ></div>
        </div>
        
        {/* Add a color overlay for the brand theme */}
        <div className="absolute inset-0 bg-gradient-to-br from-orange-600/20 via-amber-500/10 to-red-600/20"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24 lg:py-32">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 md:gap-12 items-center">
            {/* Content */}
            <div className="text-center lg:text-left">
              <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold leading-tight mb-4 md:mb-6 animate-fade-in drop-shadow-lg">
                {homeHeroSection.title || 'Chill Vibes & Hot Chillas'}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-300 to-yellow-300 drop-shadow-lg">
                  {homeHeroSection.subtitle || 'Hot Chillas'}
                </span>
              </h1>
              
              <p className="text-lg sm:text-xl lg:text-2xl text-white mb-6 md:mb-8 animate-fade-in drop-shadow-md">
                {homeHeroSection.description || 'Experience the ultimate chill spot with the hottest food in town. Fresh ingredients, cool atmosphere, amazing taste.'}
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start animate-fade-in">
                <Link 
                  to="/menu" 
                  className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 md:px-8 md:py-4 rounded-2xl font-semibold text-base md:text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-2xl flex items-center justify-center space-x-2"
                >
                  <i className="fas fa-fire"></i>
                  <span>{siteSettings?.nav_menu_text || 'Order Now'}</span>
                </Link>
                <a 
                  href="#features" 
                  className="bg-white/10 backdrop-blur-sm hover:bg-white/20 text-white px-6 py-3 md:px-8 md:py-4 rounded-2xl font-semibold text-base md:text-lg transition-all duration-300 border border-white/20 flex items-center justify-center space-x-2"
                >
                  <i className="fas fa-play"></i>
                  <span>{homeHeroSection.button_text || 'Learn More'}</span>
                </a>
              </div>
              
              {/* Stats - Using dynamic data if available */}
              <div className="grid grid-cols-3 gap-4 md:gap-6 mt-8 md:mt-12 animate-fade-in">
                <div className="text-center">
                  <div className="text-2xl md:text-3xl font-bold">1000+</div>
                  <div className="text-white text-sm">Happy Customers</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl md:text-3xl font-bold">25min</div>
                  <div className="text-white text-sm">Avg Delivery</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl md:text-3xl font-bold">4.9★</div>
                  <div className="text-white text-sm">Rating</div>
                </div>
              </div>
            </div>
            
            {/* Hero Image/Illustration */}
            <div className="relative animate-fade-in">
              <div className="relative w-full max-w-lg mx-auto">
                {/* Ramza's Chillas Signature Stacked Burger */}
                <div className="relative w-full h-64 sm:h-80 md:h-96 bg-white rounded-3xl shadow-2xl overflow-hidden transform rotate-3 hover:rotate-0 transition-transform duration-500 group">
                  {/* Featured Burger Image */}
                  <div className="absolute inset-0 flex items-center justify-center">
                    {/* Using an actual food image instead of placeholder */}
                    <div className="w-full h-full flex items-center justify-center overflow-hidden">
                      <img 
                        src="/static/images/pork-rib-kota.jpeg" 
                        alt="Ramza's Chillas Signature Stacked Burger" 
                        className="w-full h-full object-cover"
                      />
                    </div>
                    {/* Overlay with branding */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/30 rounded-2xl flex items-center justify-center p-0">
                      {/* Restaurant Logo */}
                      {siteSettings?.logo && (
                        <img 
                          src={siteSettings.logo} 
                          alt={`${siteSettings.site_name} Logo`} 
                          className="absolute inset-0 w-full h-full object-cover rounded-2xl"
                        />
                      )}
                    </div>
                  </div>
                </div>
                
                {/* Floating elements */}
                <div className="absolute -top-4 -right-4 sm:-top-6 sm:-right-6 w-12 h-12 sm:w-20 sm:h-20 bg-yellow-400 rounded-2xl shadow-lg flex items-center justify-center animate-bounce">
                  <i className="fas fa-star text-white text-lg sm:text-2xl"></i>
                </div>
                <div className="absolute -bottom-3 -left-3 sm:-bottom-4 sm:-left-4 w-10 h-10 sm:w-16 sm:h-16 bg-red-500 rounded-2xl shadow-lg flex items-center justify-center animate-pulse">
                  <i className="fas fa-heart text-white text-base sm:text-xl"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-12 sm:py-16 md:py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12 md:mb-16">
            <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-4 md:mb-6">
              {homeFeaturesSection.title || 'Why Choose Ramza\'s Chillas?'}
            </h2>
            <p className="text-base sm:text-lg md:text-xl text-gray-700 max-w-3xl mx-auto">
              {homeFeaturesSection.description || 'Chill atmosphere, hot food, cool service - we\'re committed to providing you with the best experience through quality, speed, and unmatched vibes.'}
            </p>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
            {/* Feature 1 */}
            <div className="group">
              <div className="bg-white rounded-3xl p-6 md:p-88 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
                <div className="w-12 h-12 md:w-16 md:h-16 bg-gradient-to-br from-secondary-400 to-secondary-600 rounded-2xl flex items-center justify-center mb-4 md:mb-6 group-hover:scale-110 transition-transform duration-300">
                  <i className="fas fa-clock text-white text-xl md:text-2xl"></i>
                </div>
                <h3 className="text-xl md:text-2xl font-bold text-gray-900 mb-3 md:mb-4">
                  {homeFeaturesSection.extra_text_1 || 'Chill Delivery'}
                </h3>
                <p className="text-gray-700 leading-relaxed text-sm md:text-base">
                  {homeFeaturesSection.button_text || 'Relaxed delivery in 25-30 minutes. We take our time to ensure your food arrives hot, fresh, and perfect - no rushing, just quality.'}
                </p>
                <div className="mt-4 md:mt-6">
                  <div className="flex items-center text-sm text-gray-600">
                    <i className="fas fa-check-circle text-green-500 mr-2"></i>
                    <span>Average 27min delivery</span>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Feature 2 */}
            <div className="group">
              <div className="bg-white rounded-3xl p-6 md:p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
                <div className="w-12 h-12 md:w-16 md:h-16 bg-gradient-to-br from-primary-400 to-primary-600 rounded-2xl flex items-center justify-center mb-4 md:mb-6 group-hover:scale-110 transition-transform duration-300">
                  <i className="fas fa-award text-white text-xl md:text-2xl"></i>
                </div>
                <h3 className="text-xl md:text-2xl font-bold text-gray-900 mb-3 md:mb-4">
                  {homeFeaturesSection.extra_text_2 || 'Quality Chillas'}
                </h3>
                <p className="text-gray-700 leading-relaxed text-sm md:text-base">
                  {homeFeaturesSection.button_url || 'Fresh ingredients with that chill factor. We source locally and prepare everything to order for the best taste and that laid-back island vibe.'}
                </p>
                <div className="mt-4 md:mt-6">
                  <div className="flex items-center text-sm text-gray-600">
                    <i className="fas fa-check-circle text-green-500 mr-2"></i>
                    <span>100% fresh ingredients</span>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Feature 3 */}
            <div className="group">
              <div className="bg-white rounded-3xl p-6 md:p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
                <div className="w-12 h-12 md:w-16 md:h-16 bg-gradient-to-br from-green-400 to-green-600 rounded-2xl flex items-center justify-center mb-4 md:mb-6 group-hover:scale-110 transition-transform duration-300">
                  <i className="fas fa-truck text-white text-xl md:text-2xl"></i>
                </div>
                <h3 className="text-xl md:text-2xl font-bold text-gray-900 mb-3 md:mb-4">
                  {homeFeaturesSection.extra_text_3 || 'Free Chill Zone'}
                </h3>
                <p className="text-gray-700 leading-relaxed text-sm md:text-base">
                  {homeFeaturesSection.subtitle || 'Free delivery within our chill radius. No minimum order required - we believe good food should be accessible to everyone in the neighborhood.'}
                </p>
                <div className="mt-4 md:mt-6">
                  <div className="flex items-center text-sm text-gray-600">
                    <i className="fas fa-check-circle text-green-500 mr-2"></i>
                    <span>5km radius coverage</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-12 sm:py-16 md:py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12 md:mb-16">
            <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-4 md:mb-6">
              Browse Our Chill Menu
            </h2>
            <p className="text-base sm:text-lg md:text-xl text-gray-700">
              Discover our delicious categories of fresh, made-to-order food with island vibes
            </p>
          </div>
          
          <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
            {categories.slice(0, 4).map((category, index) => (
              <Link 
                key={index} 
                to={`/menu?category=${category.name?.toLowerCase()}`} 
                className="group"
              >
                <div className="relative overflow-hidden rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:scale-105">
                  {category.image ? (
                    <div className="h-32 sm:h-40 md:h-48">
                      <img 
                        src={category.image} 
                        alt={category.name} 
                        className="w-full h-full object-cover"
                      />
                    </div>
                  ) : (
                    <div className={`h-32 sm:h-40 md:h-48 bg-gradient-to-br ${
                      index % 4 === 0 ? 'from-red-400 to-red-600' :
                      index % 4 === 1 ? 'from-red-400 to-red-600' :
                      index % 4 === 2 ? 'from-blue-400 to-blue-600' :
                      'from-green-400 to-green-600'
                    }`}>
                      <div className="w-full h-full flex items-center justify-center">
                        <i className="fas fa-utensils text-white text-3xl"></i>
                      </div>
                    </div>
                  )}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/75 to-transparent"></div>
                  <div className="absolute bottom-0 left-0 right-0 p-4 md:p-6 text-white">
                    <h3 className="text-base md:text-xl font-bold mb-1">{category.name}</h3>
                    <p className="text-sm opacity-90 line-clamp-1">{category.description || `Delicious ${category.name?.toLowerCase()}`}</p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Items Section */}
      <section className="py-12 sm:py-16 md:py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12 md:mb-16">
            <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-4 md:mb-6">
              Featured Chillas
            </h2>
            <p className="text-base sm:text-lg md:text-xl text-gray-700">
              Our most popular items that keep customers coming back for more
            </p>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
            {featuredItems.slice(0, 3).map((item, index) => (
              <div key={index} className="group">
                <div className="bg-white rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden group-hover:-translate-y-2 border border-gray-100">
                  <div className="relative overflow-hidden">
                    <div className="h-48 sm:h-56 md:h-64">
                      {item.image ? (
                        <img 
                          src={item.image} 
                          alt={item.name} 
                          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                        />
                      ) : (
                        <div className="bg-gray-200 border-2 border-dashed rounded-xl w-full h-full flex items-center justify-center">
                          <i className="fas fa-utensils text-gray-400 text-4xl"></i>
                        </div>
                      )}
                    </div>
                    <div className="absolute top-4 left-4">
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-white/95 backdrop-blur-sm text-gray-800 border border-gray-200">
                        <i className="fas fa-fire text-orange-500 mr-1"></i> Featured
                      </span>
                    </div>
                  </div>
                  <div className="p-6">
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="text-xl font-bold text-gray-900 group-hover:text-primary-500 transition-colors duration-200">
                        {item.name}
                      </h3>
                      <div className="flex items-center">
                        <span className="text-xl md:text-2xl font-bold text-primary-500">
                          R{item.price.toFixed(2)}
                        </span>
                      </div>
                    </div>
                    <p className="text-gray-700 text-sm mb-6 line-clamp-2">
                      {item.description}
                    </p>
                    <Link
                      to="/menu"
                      className="w-full bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-semibold py-3 px-6 rounded-2xl transition-all duration-300 transform hover:scale-105"
                    >
                      <i className="fas fa-shopping-cart mr-2"></i>
                      View Menu
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="text-center mt-10">
            <Link 
              to="/menu" 
              className="inline-flex items-center px-6 py-3 bg-primary-500 hover:bg-primary-600 text-white font-semibold rounded-2xl transition-all duration-300 transform hover:scale-105"
            >
              <span>View Full Menu</span>
              <i className="fas fa-arrow-right ml-2"></i>
            </Link>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      {testimonials.length > 0 && (
        <section className="py-12 sm:py-16 md:py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12 md:mb-16">
              <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-4 md:mb-6">
                What Our Customers Say
              </h2>
              <p className="text-base sm:text-lg md:text-xl text-gray-700 max-w-3xl mx-auto">
                Don't just take our word for it - hear from our satisfied customers
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
              {testimonials.slice(0, 3).map((testimonial) => (
                <div key={testimonial.id} className="bg-white rounded-3xl shadow-lg p-6 md:p-8 hover:shadow-xl transition-shadow duration-300">
                  <div className="flex items-center mb-4">
                    {[...Array(5)].map((_, i) => (
                      <i 
                        key={i} 
                        className={`fas fa-star ${i < testimonial.rating ? 'text-yellow-400' : 'text-gray-300'}`}
                      ></i>
                    ))}
                  </div>
                  <p className="text-gray-700 mb-6 italic">"{testimonial.review}"</p>
                  <div className="flex items-center">
                    {testimonial.image ? (
                      <img 
                        src={testimonial.image} 
                        alt={testimonial.customer_name} 
                        className="w-12 h-12 rounded-full object-cover mr-4"
                      />
                    ) : (
                      <div className="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center mr-4">
                        <i className="fas fa-user text-gray-500"></i>
                      </div>
                    )}
                    <div>
                      <h4 className="font-bold text-gray-900">{testimonial.customer_name}</h4>
                      {testimonial.customer_title && (
                        <p className="text-sm text-gray-600">{testimonial.customer_title}</p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className="py-16 md:py-24 bg-gradient-to-br from-primary-500 to-primary-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold mb-6">
            {homeCtaSection.title || 'Ready to Chill with Great Food?'}
          </h2>
          <p className="text-lg md:text-xl mb-10 max-w-3xl mx-auto opacity-90">
            {homeCtaSection.description || 'Join thousands of satisfied customers who enjoy our delicious chillas with that perfect chill vibe'}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/menu" 
              className="bg-white text-primary-500 hover:bg-gray-100 px-8 py-4 rounded-2xl font-bold text-lg transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              <i className="fas fa-utensils mr-2"></i>
              {homeCtaSection.button_text || 'Order Now'}
            </Link>
            <a 
              href={`tel:${siteSettings?.phone_number || '+5551232445'}`} 
              className="bg-white/20 backdrop-blur-sm hover:bg-white/30 text-white px-8 py-4 rounded-2xl font-bold text-lg transition-all duration-300 border border-white/30 flex items-center justify-center"
            >
              <i className="fas fa-phone-alt mr-2"></i>
              Call Us
            </a>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home