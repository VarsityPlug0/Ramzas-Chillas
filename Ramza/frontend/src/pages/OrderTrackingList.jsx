import React, { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useOrderTracking } from '../context/OrderTrackingContext'

const OrderTrackingList = () => {
  const { orders, updateOrders, loading, setLoading, error, setError } = useOrderTracking()
  const [polling, setPolling] = useState(false)
  const navigate = useNavigate()

  // Use useCallback to memoize the fetch function
  const fetchOrders = useCallback(async (isPolling = false) => {
    try {
      if (!isPolling) {
        // Only set loading state for initial load, not for polling
        if (orders.length === 0) {
          setLoading(true)
        }
        setError('')
      }
      
      const response = await fetch('/api/v1/orders/')
      const data = await response.json()
      
      if (data.success) {
        // Update orders in global context
        updateOrders(data.orders)
      } else {
        // Only set error if we don't have existing orders to show
        if (orders.length === 0) {
          setError(data.error || 'Failed to fetch orders')
        } else {
          // For polling, just log the error but don't show it to user
          console.warn('Polling error (continuing with cached data):', data.error || 'Failed to fetch orders')
        }
      }
    } catch (err) {
      console.error('Error fetching orders:', err)
      // Only set error if we don't have existing orders to show
      if (orders.length === 0 && !isPolling) {
        setError('Failed to fetch orders. Please check your connection and try again.')
      } else if (!isPolling) {
        // For polling, just log the error but don't show it to user
        console.warn('Polling error (continuing with cached data):', err.message)
      }
    } finally {
      setLoading(false)
      setPolling(false)
    }
  }, [orders.length, updateOrders, setError, setLoading])

  useEffect(() => {
    // Only fetch orders if we don't have any orders yet
    if (orders.length === 0) {
      fetchOrders()
    }
    
    // Set up polling every 30 seconds (less frequent to reduce server load)
    const interval = setInterval(() => {
      setPolling(true)
      fetchOrders(true)
    }, 30000)
    
    return () => clearInterval(interval)
  }, [fetchOrders, orders.length])

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

  const handleOrderClick = (orderId) => {
    navigate(`/order/${orderId}`)
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

  if (loading && orders.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading your orders...</p>
          </div>
        </div>
      </div>
    )
  }

  // Show error only if we have no orders to display
  if (error && orders.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-3xl shadow-lg p-8 text-center">
            <div className="text-red-500 mb-4">
              <i className="fas fa-exclamation-circle text-4xl"></i>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Error</h2>
            <p className="text-gray-600 mb-6">{error}</p>
            <button 
              onClick={() => fetchOrders()}
              className="bg-primary text-white px-6 py-3 rounded-2xl font-semibold hover:bg-primary-dark transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-3">Your Orders</h1>
          <p className="text-gray-600">Track all your orders in one place</p>
        </div>

        {/* Refresh Button */}
        <div className="flex justify-end mb-6">
          <button 
            onClick={() => fetchOrders()}
            disabled={polling}
            className="flex items-center bg-white text-gray-700 px-4 py-2 rounded-lg font-semibold hover:bg-gray-50 transition-colors border border-gray-200 disabled:opacity-50"
          >
            {polling ? (
              <>
                <i className="fas fa-sync-alt fa-spin mr-2"></i>
                Updating...
              </>
            ) : (
              <>
                <i className="fas fa-sync-alt mr-2"></i>
                Refresh
              </>
            )}
          </button>
        </div>

        {/* Orders List */}
        {orders.length > 0 ? (
          <div className="space-y-4">
            {orders.map((order) => (
              <motion.div
                key={order.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-3xl shadow-lg p-6 cursor-pointer hover:shadow-xl transition-shadow duration-300"
                onClick={() => handleOrderClick(order.order_number)}
              >
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">Order #{order.order_number}</h3>
                    <p className="text-sm text-gray-600">
                      {order.customer_name} • {order.customer_phone}
                    </p>
                    <p className="text-xs text-gray-500">
                      Placed on {formatDate(order.created_at)} at {formatTime(order.created_at)}
                    </p>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(order.status)}`}>
                      {order.status_display}
                    </span>
                    <div className="text-right">
                      <p className="font-bold text-gray-900">R{order.total.toFixed(2)}</p>
                    </div>
                  </div>
                </div>
                
                {/* Progress Indicator */}
                <div className="mt-4">
                  <div className="flex justify-between text-xs text-gray-500 mb-1">
                    <span>Progress</span>
                    <span>{Math.round(getStatusSteps(order.status).filter(step => step.completed).length / getStatusSteps(order.status).length * 100)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-primary h-2 rounded-full" 
                      style={{ width: `${Math.round(getStatusSteps(order.status).filter(step => step.completed).length / getStatusSteps(order.status).length * 100)}%` }}
                    ></div>
                  </div>
                </div>
                
                <div className="mt-4 flex items-center text-primary-600 text-sm font-medium">
                  <span>View details</span>
                  <i className="fas fa-arrow-right ml-2"></i>
                </div>
              </motion.div>
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-3xl shadow-lg p-12 text-center">
            <div className="text-gray-400 mb-4">
              <i className="fas fa-shopping-bag text-4xl"></i>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">No Orders Yet</h2>
            <p className="text-gray-600 mb-6">You haven't placed any orders yet.</p>
            <button 
              onClick={() => navigate('/menu')}
              className="bg-primary text-white px-6 py-3 rounded-2xl font-semibold hover:bg-primary-dark transition-colors"
            >
              Browse Menu
            </button>
          </div>
        )}

        {/* Error Message (when there are orders but we have an error) */}
        {error && orders.length > 0 && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-2xl text-red-700 text-center">
            {error}
          </div>
        )}
      </div>
    </div>
  )
}

export default OrderTrackingList