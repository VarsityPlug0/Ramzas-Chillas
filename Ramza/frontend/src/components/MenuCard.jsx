import React from 'react'
import { motion } from 'framer-motion'
import { useApp } from '../context/CartContext'

const MenuCard = ({ item, onAddToCart }) => {
  const { siteImages } = useApp()
  
  const getCategoryIcon = (category) => {
    const icons = {
      'Burgers': 'fas fa-hamburger',
      'Pizzas': 'fas fa-pizza-slice',
      'Drinks': 'fas fa-glass-cheers',
      'Sides': 'fas fa-cookie-bite'
    }
    return icons[category] || 'fas fa-utensils'
  }

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      whileHover={{ y: -5 }}
      className="group"
    >
      <div className="bg-white rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-500 overflow-hidden group-hover:-translate-y-2">
        {/* Image Container */}
        <div className="relative overflow-hidden">
          <div className="aspect-w-4 aspect-h-3">
            {item.image ? (
              <img 
                src={item.image} 
                alt={item.name} 
                className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-500"
              />
            ) : (
              <div className="bg-gray-200 border-2 border-dashed rounded-xl w-full h-full flex items-center justify-center">
                <i className={`${getCategoryIcon(item.category)} text-gray-400 text-4xl`}></i>
              </div>
            )}
          </div>
          <div className="absolute top-4 right-4">
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold bg-white/90 backdrop-blur-sm text-gray-800 border border-gray-200">
              {item.category}
            </span>
          </div>
        </div>
        
        {/* Content */}
        <div className="p-5">
          <div className="flex justify-between items-start mb-2">
            <h3 className="text-lg font-bold text-gray-900 group-hover:text-primary-600 transition-colors">
              {item.name}
            </h3>
            <span className="text-lg font-bold text-primary-600">
              R{item.price.toFixed(2)}
            </span>
          </div>
          
          <p className="text-gray-600 text-sm mb-4 line-clamp-2">
            {item.description}
          </p>
          
          <button
            onClick={() => onAddToCart(item)}
            className="w-full bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-semibold py-3 px-4 rounded-2xl transition-all duration-300 transform hover:scale-[1.02] flex items-center justify-center space-x-2"
          >
            <i className="fas fa-plus"></i>
            <span>Add to Cart</span>
          </button>
        </div>
      </div>
    </motion.div>
  )
}

export default MenuCard