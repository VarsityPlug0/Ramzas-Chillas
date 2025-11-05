import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useOrderTracking } from '../context/OrderTrackingContext'

const OrderTracking = () => {
  const { orderId } = useParams()
  const navigate = useNavigate()
  const { selectedOrder, setSelectedOrder, orders, addOrder, clearSelectedOrder } = useOrderTracking()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (orderId) {
      fetchOrderStatus()
    } else {
      setError('No order ID provided')
      setLoading(false)
    }
    
    // Cleanup function to clear selected order when component unmounts
    return () => {
      // Don't clear immediately, but we could if needed
    }
  }, [orderId])

  const fetchOrderStatus = async () => {
    try {
      setLoading(true)
      setError('')
      
      // Check if we already have this order in our global state
      const existingOrder = orders.find(order => order.order_number === orderId)
      if (existingOrder && !selectedOrder) {
        setSelectedOrder(existingOrder)
        setLoading(false)
        return
      }
      
      // Make sure we're using the correct API endpoint
      const response = await fetch(`/api/v1/orders/${orderId}/status/`)
      const data = await response.json()
      
      if (data.success) {
        setSelectedOrder(data.order)
        // Also add to global orders list
        addOrder(data.order)
      } else {
        setError(data.error || 'Failed to fetch order status')
      }
    } catch (err) {
      console.error('Error fetching order status:', err)
      setError('Failed to fetch order status. Please check your connection and try again.')
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      'pending': 'bg-yellow-100 text-yellow-800',
      'sent_to_whatsapp': 'bg-blue-100 text-blue-800',
      'confirmed': 'bg-blue-100 text-blue-800',
      'preparing': 'bg-blue-100 text-blue-800',
      'ready': 'bg-green-100 text-green-800',
      'out_for_delivery': 'bg-purple-100 text-purple-800',
      'delivered': 'bg-gray-100 text-gray-800',
      'completed': 'bg-gray-100 text-gray-800',
      'cancelled': 'bg-red-100 text-red-800'
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  const getStatusSteps = (currentStatus) => {
    const steps = [
      { id: 'sent_to_whatsapp', label: 'Sent to Admin', completed: true },
      { id: 'confirmed', label: 'Confirmed', completed: ['confirmed', 'preparing', 'ready', 'out_for_delivery', 'delivered', 'completed'].includes(currentStatus) },
      { id: 'preparing', label: 'Preparing', completed: ['preparing', 'ready', 'out_for_delivery', 'delivered', 'completed'].includes(currentStatus) },
      { id: 'ready', label: 'Ready', completed: ['ready', 'out_for_delivery', 'delivered', 'completed'].includes(currentStatus) },
      { id: 'out_for_delivery', label: 'Out for Delivery', completed: ['out_for_delivery', 'delivered', 'completed'].includes(currentStatus) },
      { id: 'delivered', label: 'Delivered', completed: ['delivered', 'completed'].includes(currentStatus) }
    ]
    return steps
  }

  // Format date safely
  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) {
        return 'Invalid Date';
      }
      return date.toLocaleDateString();
    } catch (e) {
      return 'Invalid Date';
    }
  }

  // Format time safely
  const formatTime = (dateString) => {
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) {
        return '';
      }
      return date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    } catch (e) {
      return '';
    }
  }

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading order details...</p>
          </div>
        </div>
      </div>
    )
  }

  // Error state
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-3xl shadow-lg p-8 text-center">
            <div className="text-red-500 mb-4">
              <i className="fas fa-exclamation-circle text-4xl"></i>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Error</h2>
            <p className="text-gray-600 mb-6">{error}</p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <button 
                onClick={fetchOrderStatus}
                className="bg-primary text-white px-6 py-3 rounded-2xl font-semibold hover:bg-primary-dark transition-colors"
              >
                Try Again
              </button>
              <button 
                onClick={() => navigate('/orders')}
                className="bg-gray-200 text-gray-800 px-6 py-3 rounded-2xl font-semibold hover:bg-gray-300 transition-colors"
              >
                Back to Orders
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Use selectedOrder from context or local state
  const orderToDisplay = selectedOrder || null

  // No order found
  if (!orderToDisplay) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-3xl shadow-lg p-8 text-center">
            <div className="text-gray-400 mb-4">
              <i className="fas fa-shopping-cart text-4xl"></i>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Order Not Found</h2>
            <p className="text-gray-600">We couldn't find an order with ID: {orderId}</p>
            <div className="mt-6">
              <button 
                onClick={() => navigate('/orders')}
                className="bg-primary text-white px-6 py-3 rounded-2xl font-semibold hover:bg-primary-dark transition-colors"
              >
                Back to Orders
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  const statusSteps = getStatusSteps(orderToDisplay.status)

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-3">Track Your Order</h1>
          <p className="text-gray-600">Order #{orderToDisplay.order_number}</p>
        </div>

        {/* Order Status Card */}
        <div className="bg-white rounded-3xl shadow-lg p-6 md:p-8 mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900">Order Status</h2>
              <p className="text-gray-600">Placed on {formatDate(orderToDisplay.created_at)} at {formatTime(orderToDisplay.created_at)}</p>
            </div>
            <span className={`px-4 py-2 rounded-full text-sm font-semibold ${getStatusColor(orderToDisplay.status)}`}>
              {orderToDisplay.status_display}
            </span>
          </div>

          {/* Progress Steps */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Order Progress</h3>
            <div className="flex flex-col space-y-4">
              {statusSteps.map((step, index) => (
                <div key={step.id} className="flex items-center">
                  <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                    step.completed ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-500'
                  }`}>
                    {step.completed ? (
                      <i className="fas fa-check"></i>
                    ) : (
                      <span className="text-sm font-medium">{index + 1}</span>
                    )}
                  </div>
                  <div className="ml-4 flex-1">
                    <p className={`text-sm font-medium ${
                      step.completed ? 'text-gray-900' : 'text-gray-500'
                    }`}>
                      {step.label}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Order Details */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Order Details</h3>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-gray-600">Customer</span>
                <span className="font-medium">{orderToDisplay.customer_name || 'N/A'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">WhatsApp Number</span>
                <span className="font-medium">{orderToDisplay.customer_phone || 'N/A'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Order Type</span>
                <span className="font-medium capitalize">{orderToDisplay.order_type || 'N/A'}</span>
              </div>
              {orderToDisplay.delivery_address && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Delivery Address</span>
                  <span className="font-medium text-right">{orderToDisplay.delivery_address}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Order Items */}
        <div className="bg-white rounded-3xl shadow-lg p-6 md:p-8 mb-8">
          <h3 className="text-xl font-bold text-gray-900 mb-6">Order Items</h3>
          <div className="space-y-4">
            {orderToDisplay.items && orderToDisplay.items.length > 0 ? (
              orderToDisplay.items.map((item, index) => (
                <div key={index} className="flex items-center justify-between py-3 border-b border-gray-100">
                  <div className="flex items-center">
                    <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mr-4">
                      <i className="fas fa-utensils text-gray-400"></i>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900">{item.name || 'Unknown Item'}</h4>
                      <p className="text-sm text-gray-600">Qty: {item.quantity || 0}</p>
                    </div>
                  </div>
                  <div className="font-semibold">R{(item.total || 0).toFixed(2)}</div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-4">No items found for this order</p>
            )}
          </div>
          
          <div className="mt-6 pt-4 border-t border-gray-200">
            <div className="flex justify-between mb-2">
              <span className="text-gray-600">Subtotal</span>
              <span className="font-medium">R{(orderToDisplay.subtotal || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between mb-2">
              <span className="text-gray-600">Delivery Fee</span>
              <span className="font-medium">R{(orderToDisplay.delivery_fee || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-lg font-bold mt-2">
              <span>Total</span>
              <span>R{(orderToDisplay.total || 0).toFixed(2)}</span>
            </div>
          </div>
        </div>

        {/* Refresh Button */}
        <div className="text-center">
          <button 
            onClick={fetchOrderStatus}
            className="bg-primary text-white px-6 py-3 rounded-2xl font-semibold hover:bg-primary-dark transition-colors flex items-center mx-auto"
          >
            <i className="fas fa-sync-alt mr-2"></i>
            Refresh Status
          </button>
        </div>
      </div>
    </div>
  )
}

export default OrderTracking