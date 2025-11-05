import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import MenuCard from '../components/MenuCard'
import { useApp } from '../context/CartContext'
import { useCart } from '../context/CartContext'

const Menu = () => {
  const { menuItems, categories, contentSections, loading, error } = useApp()
  const { addToCart } = useCart()
  const [filteredItems, setFilteredItems] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')

  // Get menu hero section content
  const menuHeroSection = contentSections?.menu_hero || {}

  useEffect(() => {
    let filtered = menuItems

    // Filter by category
    if (selectedCategory !== 'All') {
      filtered = filtered.filter(item => item.category === selectedCategory)
    }

    // Filter by search term
    if (searchTerm && typeof searchTerm === 'string') {
      const term = searchTerm.toLowerCase()
      filtered = filtered.filter(item => {
        // Ensure item properties are strings before calling toLowerCase
        const itemName = typeof item.name === 'string' ? item.name : ''
        const itemDescription = typeof item.description === 'string' ? item.description : ''
        return itemName.toLowerCase().includes(term) || itemDescription.toLowerCase().includes(term)
      })
    }

    setFilteredItems(filtered)
  }, [menuItems, selectedCategory, searchTerm])

  const handleAddToCart = (item) => {
    addToCart(item)
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
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

  return (
    <div>
      {/* Hero Section */}
      <div className="relative bg-gradient-to-br from-gray-800 via-gray-900 to-black overflow-hidden">
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
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
          <div className="text-center">
            <div className="inline-flex items-center px-3 py-1.5 md:px-4 md:py-2 bg-white/25 backdrop-blur-sm rounded-full text-white text-sm font-medium mb-4 md:mb-6 border border-white/20">
              <i className="fas fa-fire mr-1.5 md:mr-2 text-orange-300"></i>
              {menuHeroSection.extra_text_1 || 'Fresh • Hot • Delicious'}
            </div>
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-4 md:mb-6 drop-shadow-lg">
              {menuHeroSection.title || 'Our'} <span className="text-gradient bg-gradient-to-r from-orange-300 to-yellow-300 bg-clip-text text-transparent drop-shadow-lg">
                {menuHeroSection.subtitle || 'Chill'}
              </span> Menu
            </h1>
            <p className="text-base sm:text-lg md:text-xl text-white max-w-2xl mx-auto mb-6 md:mb-8 drop-shadow-md">
              {menuHeroSection.description || 'Discover our signature chillas, crafted with the finest ingredients and served with unmatched flavor'}
            </p>
            
            {/* Search Bar */}
            <div className="max-w-md mx-auto relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i className="fas fa-search text-gray-500"></i>
              </div>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder={menuHeroSection.button_text || "Search our menu..."}
                className="w-full pl-10 pr-4 py-2.5 md:py-3 bg-white/95 backdrop-blur-sm border-0 rounded-2xl focus:ring-2 focus:ring-orange-400 focus:outline-none text-gray-800 placeholder-gray-600 text-sm md:text-base"
                aria-label="Search menu items"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Menu Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-16">
        {/* Category Filter */}
        <div className="mb-8 md:mb-12">
          <div className="flex flex-wrap justify-center gap-2 md:gap-3">
            {categories.map((category, index) => {
              // Ensure category is properly handled whether it's a string or object
              const categoryName = typeof category === 'string' ? category : (category?.name || '');
              
              return (
                <button
                  key={index}
                  onClick={() => setSelectedCategory(categoryName)}
                  className={`category-btn px-4 py-2 md:px-6 md:py-3 rounded-2xl font-semibold text-sm md:text-base transition-all duration-300 ${
                    selectedCategory === categoryName
                      ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg transform -translate-y-1'
                      : 'bg-gray-100 text-gray-800 hover:bg-primary-500 hover:text-white'
                  }`}
                >
                  {categoryName === 'All' ? (
                    <>
                      <i className="fas fa-th-large mr-1.5 md:mr-2"></i>All Items
                    </>
                  ) : categoryName === 'Burgers' ? (
                    <>
                      <i className="fas fa-hamburger mr-1.5 md:mr-2"></i>{categoryName}
                    </>
                  ) : categoryName === 'Pizzas' ? (
                    <>
                      <i className="fas fa-pizza-slice mr-1.5 md:mr-2"></i>{categoryName}
                    </>
                  ) : categoryName === 'Drinks' ? (
                    <>
                      <i className="fas fa-glass-cheers mr-1.5 md:mr-2"></i>{categoryName}
                    </>
                  ) : categoryName === 'Sides' ? (
                    <>
                      <i className="fas fa-cookie-bite mr-1.5 md:mr-2"></i>{categoryName}
                    </>
                  ) : (
                    <>
                      <i className="fas fa-utensils mr-1.5 md:mr-2"></i>{categoryName}
                    </>
                  )}
                </button>
              );
            })}
          </div>
        </div>

        {/* Menu Items Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 md:gap-8">
          <AnimatePresence>
            {filteredItems.length > 0 ? (
              filteredItems.map((item) => (
                <MenuCard
                  key={item.id}
                  item={item}
                  onAddToCart={handleAddToCart}
                />
              ))
            ) : (
              <div className="col-span-full text-center py-12">
                <div className="max-w-md mx-auto">
                  <div className="w-16 h-16 md:w-24 md:h-24 mx-auto bg-gray-100 rounded-full flex items-center justify-center mb-4 md:mb-6">
                    <i className="fas fa-search text-2xl md:text-3xl text-gray-500"></i>
                  </div>
                  <h3 className="text-lg md:text-xl font-semibold text-gray-900 mb-2">No items found</h3>
                  <p className="text-gray-700 text-sm md:text-base">
                    Try adjusting your search or filter to find what you're looking for.
                  </p>
                  <button
                    onClick={() => {
                      setSearchTerm('')
                      setSelectedCategory('All')
                    }}
                    className="mt-4 px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg transition-colors"
                  >
                    Clear Filters
                  </button>
                </div>
              </div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  )
}

export default Menu