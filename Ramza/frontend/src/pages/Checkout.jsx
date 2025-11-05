import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useApp } from '../context/CartContext'
import { useCart } from '../context/CartContext'

const Checkout = () => {
  const [deliveryMethod, setDeliveryMethod] = useState('delivery')
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zip: ''
  })
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState('')
  const { siteSettings } = useApp()
  const { cartItems, getCartTotal, clearCart } = useCart()
  const navigate = useNavigate()

  const subtotal = getCartTotal()
  const deliveryFee = deliveryMethod === 'delivery' ? 3.99 : 0
  const tax = subtotal * 0.0825
  const total = subtotal + deliveryFee + tax

  useEffect(() => {
    if (cartItems.length === 0) {
      navigate('/cart')
    }
  }, [cartItems, navigate])

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsProcessing(true)
    setError('')
    
    try {
      // Prepare order data
      const orderData = {
        customer_name: `${formData.firstName} ${formData.lastName}`,
        customer_phone: formData.phone,
        customer_email: formData.email,
        delivery_method: deliveryMethod,
        delivery_address: deliveryMethod === 'delivery' 
          ? `${formData.address}, ${formData.city}, ${formData.state} ${formData.zip}`
          : '',
        cart_items: cartItems,
        subtotal: subtotal,
        delivery_fee: deliveryFee,
        total: total
      }

      // Send order to backend
      const response = await fetch('/api/v1/orders/create-order-whatsapp/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData)
      })

      const result = await response.json()

      if (result.success) {
        // Clear cart
        clearCart()
        
        // Redirect to WhatsApp with order details
        window.location.href = result.whatsapp_url
      } else {
        setError(result.error || 'Failed to process order')
        setIsProcessing(false)
      }
    } catch (err) {
      setError('Failed to process order. Please try again.')
      setIsProcessing(false)
    }
  }

  return (
    <div>
      {/* Checkout Header */}
      <div className="relative bg-gradient-to-br from-gray-50 to-gray-100 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <div className="inline-flex items-center px-4 py-2 bg-primary-500/10 rounded-full text-primary-500 text-sm font-medium mb-4">
              <i className="fas fa-lock mr-2"></i>
              Secure Checkout
            </div>
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Complete Your Order</h1>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Review your order and provide your delivery information
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-2xl text-red-700">
            {error}
          </div>
        )}
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Checkout Form */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-3xl shadow-lg p-6 md:p-8">
              <form onSubmit={handleSubmit}>
                {/* Delivery Method */}
                <div className="mb-8">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Delivery Method</h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <button
                      type="button"
                      onClick={() => setDeliveryMethod('delivery')}
                      className={`p-4 rounded-2xl border-2 transition-all duration-300 ${
                        deliveryMethod === 'delivery'
                          ? 'border-primary-500 bg-primary-50'
                          : 'border-gray-200 hover:border-primary-300'
                      }`}
                    >
                      <div className="flex items-center">
                        <div className={`w-5 h-5 rounded-full border-2 mr-3 flex items-center justify-center ${
                          deliveryMethod === 'delivery'
                            ? 'border-primary-500 bg-primary-500'
                            : 'border-gray-300'
                        }`}>
                          {deliveryMethod === 'delivery' && (
                            <i className="fas fa-check text-white text-xs"></i>
                          )}
                        </div>
                        <div className="text-left">
                          <div className="font-semibold text-gray-900">Delivery</div>
                          <div className="text-sm text-gray-600">
                            {siteSettings?.delivery_time_text || '25-30 minutes'}
                          </div>
                        </div>
                      </div>
                    </button>
                    
                    <button
                      type="button"
                      onClick={() => setDeliveryMethod('pickup')}
                      className={`p-4 rounded-2xl border-2 transition-all duration-300 ${
                        deliveryMethod === 'pickup'
                          ? 'border-primary-500 bg-primary-50'
                          : 'border-gray-200 hover:border-primary-300'
                      }`}
                    >
                      <div className="flex items-center">
                        <div className={`w-5 h-5 rounded-full border-2 mr-3 flex items-center justify-center ${
                          deliveryMethod === 'pickup'
                            ? 'border-primary-500 bg-primary-500'
                            : 'border-gray-300'
                        }`}>
                          {deliveryMethod === 'pickup' && (
                            <i className="fas fa-check text-white text-xs"></i>
                          )}
                        </div>
                        <div className="text-left">
                          <div className="font-semibold text-gray-900">Pickup</div>
                          <div className="text-sm text-gray-600">Skip the line</div>
                        </div>
                      </div>
                    </button>
                  </div>
                </div>

                {/* Contact Information */}
                <div className="mb-8">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Contact Information</h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-1">
                        First Name
                      </label>
                      <input
                        type="text"
                        id="firstName"
                        name="firstName"
                        value={formData.firstName}
                        onChange={handleInputChange}
                        required
                        className="w-full px-4 py-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                      />
                    </div>
                    <div>
                      <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-1">
                        Last Name
                      </label>
                      <input
                        type="text"
                        id="lastName"
                        name="lastName"
                        value={formData.lastName}
                        onChange={handleInputChange}
                        required
                        className="w-full px-4 py-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                      />
                    </div>
                    <div>
                      <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                        Email
                      </label>
                      <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        required
                        className="w-full px-4 py-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                      />
                    </div>
                    <div>
                      <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">
                        Phone
                      </label>
                      <input
                        type="tel"
                        id="phone"
                        name="phone"
                        value={formData.phone}
                        onChange={handleInputChange}
                        required
                        className="w-full px-4 py-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                      />
                    </div>
                  </div>
                </div>

                {/* Delivery Address */}
                {deliveryMethod === 'delivery' && (
                  <div className="mb-8">
                    <h2 className="text-xl font-bold text-gray-900 mb-4">Delivery Address</h2>
                    <div className="space-y-4">
                      <div>
                        <label htmlFor="address" className="block text-sm font-medium text-gray-700 mb-1">
                          Address
                        </label>
                        <input
                          type="text"
                          id="address"
                          name="address"
                          value={formData.address}
                          onChange={handleInputChange}
                          required
                          className="w-full px-4 py-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                        />
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <div className="sm:col-span-2">
                          <label htmlFor="city" className="block text-sm font-medium text-gray-700 mb-1">
                            City
                          </label>
                          <input
                            type="text"
                            id="city"
                            name="city"
                            value={formData.city}
                            onChange={handleInputChange}
                            required
                            className="w-full px-4 py-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                          />
                        </div>
                        <div>
                          <label htmlFor="state" className="block text-sm font-medium text-gray-700 mb-1">
                            State
                          </label>
                          <input
                            type="text"
                            id="state"
                            name="state"
                            value={formData.state}
                            onChange={handleInputChange}
                            required
                            className="w-full px-4 py-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                          />
                        </div>
                        <div>
                          <label htmlFor="zip" className="block text-sm font-medium text-gray-700 mb-1">
                            ZIP Code
                          </label>
                          <input
                            type="text"
                            id="zip"
                            name="zip"
                            value={formData.zip}
                            onChange={handleInputChange}
                            required
                            className="w-full px-4 py-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Payment Method */}
                <div className="mb-8">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Payment Method</h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <button
                      type="button"
                      className="p-4 rounded-2xl border-2 border-gray-200 hover:border-primary-300 transition-all duration-300 flex items-center"
                    >
                      <div className="w-10 h-6 bg-gray-200 rounded mr-3"></div>
                      <div className="text-left">
                        <div className="font-semibold text-gray-900">Credit Card</div>
                        <div className="text-sm text-gray-600">Visa, Mastercard, etc.</div>
                      </div>
                    </button>
                    
                    <button
                      type="button"
                      className="p-4 rounded-2xl border-2 border-primary-500 bg-primary-50 transition-all duration-300 flex items-center"
                    >
                      <div className="w-10 h-6 bg-gray-200 rounded mr-3"></div>
                      <div className="text-left">
                        <div className="font-semibold text-gray-900">Cash</div>
                        <div className="text-sm text-gray-600">Pay on delivery</div>
                      </div>
                    </button>
                  </div>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={isProcessing}
                  className="w-full bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-bold py-4 px-6 rounded-2xl transition-all duration-300 transform hover:scale-[1.02] flex items-center justify-center space-x-2 shadow-lg disabled:opacity-70 disabled:cursor-not-allowed"
                >
                  {isProcessing ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                      <span>Processing Order...</span>
                    </>
                  ) : (
                    <>
                      <span>Place Order - R{total.toFixed(2)}</span>
                      <i className="fas fa-arrow-right"></i>
                    </>
                  )}
                </button>
              </form>
            </div>
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-3xl shadow-lg p-6 sticky top-24">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Order Summary</h2>
              
              <div className="space-y-4 mb-6 max-h-96 overflow-y-auto">
                {cartItems.map((item) => (
                  <div key={item.id} className="flex items-center justify-between py-3 border-b border-gray-100">
                    <div className="flex items-center">
                      <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mr-3">
                        <i className="fas fa-utensils text-gray-400"></i>
                      </div>
                      <div>
                        <div className="font-medium text-gray-900">{item.name}</div>
                        <div className="text-sm text-gray-600">Qty: {item.quantity}</div>
                      </div>
                    </div>
                    <div className="font-semibold">R{(item.price * item.quantity).toFixed(2)}</div>
                  </div>
                ))}
              </div>
              
              <div className="space-y-3 mb-6">
                <div className="flex justify-between">
                  <span className="text-gray-600">Subtotal</span>
                  <span className="font-semibold">R{subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">
                    {deliveryMethod === 'delivery' ? 'Delivery Fee' : 'Pickup'}
                  </span>
                  <span className="font-semibold">
                    {deliveryFee > 0 ? `R${deliveryFee.toFixed(2)}` : 'Free'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Tax</span>
                  <span className="font-semibold">R{tax.toFixed(2)}</span>
                </div>
                <div className="border-t border-gray-200 pt-3 flex justify-between text-lg font-bold">
                  <span>Total</span>
                  <span className="text-primary-600">R{total.toFixed(2)}</span>
                </div>
              </div>
              
              <Link
                to="/cart"
                className="w-full text-center text-gray-600 hover:text-primary-600 font-semibold py-3 px-6 rounded-2xl transition-all duration-300 border border-gray-200 hover:border-primary-200 flex items-center justify-center space-x-2"
              >
                <i className="fas fa-arrow-left"></i>
                <span>Back to Cart</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Checkout