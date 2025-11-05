import React, { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import CartItem from '../components/CartItem'
import { useApp } from '../context/CartContext'
import { useCart } from '../context/CartContext'

const Cart = () => {
  const { siteSettings } = useApp()
  const {
    cartItems,
    removeFromCart,
    updateQuantity,
    getCartTotal,
    getCartCount
  } = useCart()

  const subtotal = getCartTotal()
  const deliveryFee = subtotal > 0 ? 3.99 : 0
  const tax = subtotal * 0.0825
  const total = subtotal + deliveryFee + tax

  return (
    <div>
      {/* Cart Header */}
      <div className="relative bg-gradient-to-br from-gray-50 to-gray-100 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <div className="inline-flex items-center px-4 py-2 bg-primary-500/10 rounded-full text-primary-500 text-sm font-medium mb-4">
              <i className="fas fa-shopping-cart mr-2"></i>
              {getCartCount()} {getCartCount() === 1 ? 'Item' : 'Items'} in Cart
            </div>
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Your Chilla Cart</h1>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Review your items and proceed to checkout when you're ready
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
        {cartItems.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-24 h-24 mx-auto bg-gray-100 rounded-full flex items-center justify-center mb-6">
              <i className="fas fa-shopping-cart text-3xl text-gray-400"></i>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Your cart is empty</h2>
            <p className="text-gray-600 mb-8">Looks like you haven't added any chillas to your cart yet</p>
            <Link 
              to="/menu" 
              className="inline-flex items-center px-6 py-3 bg-primary-500 hover:bg-primary-600 text-white font-semibold rounded-2xl transition-all duration-300 transform hover:scale-105"
            >
              <i className="fas fa-utensils mr-2"></i>
              Browse Menu
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Cart Items */}
            <div className="lg:col-span-2">
              <div className="space-y-6">
                <AnimatePresence>
                  {cartItems.map((item) => (
                    <CartItem
                      key={item.id}
                      item={item}
                      onUpdateQuantity={updateQuantity}
                      onRemove={removeFromCart}
                    />
                  ))}
                </AnimatePresence>
              </div>
            </div>

            {/* Order Summary */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-3xl shadow-lg p-6 sticky top-24">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Order Summary</h2>
                
                <div className="space-y-4 mb-6">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Subtotal</span>
                    <span className="font-semibold">R{subtotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Delivery Fee</span>
                    <span className="font-semibold">
                      {deliveryFee > 0 ? `R${deliveryFee.toFixed(2)}` : 'Free'}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Tax</span>
                    <span className="font-semibold">R{tax.toFixed(2)}</span>
                  </div>
                  <div className="border-t border-gray-200 pt-4 flex justify-between text-lg font-bold">
                    <span>Total</span>
                    <span className="text-primary-600">R{total.toFixed(2)}</span>
                  </div>
                </div>
                
                <Link
                  to="/checkout"
                  className="w-full bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-bold py-4 px-6 rounded-2xl transition-all duration-300 transform hover:scale-[1.02] flex items-center justify-center space-x-2 shadow-lg"
                >
                  <span>Proceed to Checkout</span>
                  <i className="fas fa-arrow-right"></i>
                </Link>
                
                <Link
                  to="/menu"
                  className="w-full mt-4 text-center text-gray-600 hover:text-primary-600 font-semibold py-3 px-6 rounded-2xl transition-all duration-300 border border-gray-200 hover:border-primary-200 flex items-center justify-center space-x-2"
                >
                  <i className="fas fa-arrow-left"></i>
                  <span>Continue Shopping</span>
                </Link>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Cart