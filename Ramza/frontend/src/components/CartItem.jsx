import React from 'react'
import { motion } from 'framer-motion'
import { useApp } from '../context/CartContext'

const CartItem = ({ item, onUpdateQuantity, onRemove }) => {
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
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 20 }}
      className="cart-item bg-white rounded-2xl shadow-lg p-4 md:p-6 transition-all duration-300 hover:shadow-xl"
    >
      <div className="flex items-center space-x-4 md:space-x-6">
        {/* Item Image */}
        <div className="flex-shrink-0">
          <div className="w-16 h-16 md:w-20 md:h-20 bg-gradient-to-br from-orange-100 to-orange-200 rounded-xl flex items-center justify-center">
            {item.image ? (
              <img 
                src={item.image} 
                alt={item.name} 
                className="w-full h-full object-cover rounded-xl"
              />
            ) : (
              <i className={`${getCategoryIcon(item.category)} text-orange-500 text-xl`}></i>
            )}
          </div>
        </div>
        
        {/* Item Details */}
        <div className="flex-grow">
          <div className="flex justify-between items-start">
            <div>
              <h3 className="font-bold text-gray-900 text-base md:text-lg">{item.name}</h3>
              <p className="text-primary-600 font-semibold text-base md:text-lg">R{item.price.toFixed(2)}</p>
            </div>
            <button 
              onClick={() => onRemove(item.id)}
              className="text-gray-400 hover:text-red-500 transition-colors"
              aria-label={`Remove ${item.name} from cart`}
            >
              <i className="fas fa-times"></i>
            </button>
          </div>
          
          {/* Quantity Controls */}
          <div className="flex items-center mt-3 space-x-3">
            <button
              onClick={() => onUpdateQuantity(item.id, item.quantity - 1)}
              className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-600 hover:bg-gray-200 transition-colors"
              aria-label={`Decrease quantity of ${item.name}`}
            >
              <i className="fas fa-minus"></i>
            </button>
            
            <span className="w-10 text-center font-semibold text-gray-900">{item.quantity}</span>
            
            <button
              onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
              className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-600 hover:bg-gray-200 transition-colors"
              aria-label={`Increase quantity of ${item.name}`}
            >
              <i className="fas fa-plus"></i>
            </button>
          </div>
        </div>
      </div>
      
      {/* Item Total */}
      <div className="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center">
        <span className="text-gray-600 text-sm">Total</span>
        <span className="font-bold text-gray-900">R{(item.price * item.quantity).toFixed(2)}</span>
      </div>
    </motion.div>
  )
}

export default CartItem