import React, { createContext, useContext, useState, useEffect } from 'react'

const OrderTrackingContext = createContext()

export function OrderTrackingProvider({ children }) {
  const [orders, setOrders] = useState([])
  const [selectedOrder, setSelectedOrder] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Load orders from localStorage on initial render
  useEffect(() => {
    console.log('OrderTrackingProvider: Initializing context')
    try {
      const savedOrders = localStorage.getItem('ramza_orders')
      console.log('OrderTrackingProvider: Found saved orders in localStorage:', savedOrders)
      if (savedOrders) {
        const parsedOrders = JSON.parse(savedOrders)
        setOrders(parsedOrders)
        console.log('OrderTrackingProvider: Loaded orders from localStorage:', parsedOrders.length)
      } else {
        console.log('OrderTrackingProvider: No saved orders found in localStorage')
      }
    } catch (error) {
      console.error('OrderTrackingProvider: Failed to parse orders data from localStorage:', error)
      setOrders([])
    }
    
    try {
      const savedSelectedOrder = localStorage.getItem('ramza_selected_order')
      console.log('OrderTrackingProvider: Found saved selected order in localStorage:', savedSelectedOrder)
      if (savedSelectedOrder) {
        const parsedOrder = JSON.parse(savedSelectedOrder)
        setSelectedOrder(parsedOrder)
        console.log('OrderTrackingProvider: Loaded selected order from localStorage')
      } else {
        console.log('OrderTrackingProvider: No saved selected order found in localStorage')
      }
    } catch (error) {
      console.error('OrderTrackingProvider: Failed to parse selected order data from localStorage:', error)
    }
    
    setLoading(false)
    console.log('OrderTrackingProvider: Finished initialization')
  }, [])

  // Save orders to localStorage whenever they change
  useEffect(() => {
    console.log('OrderTrackingProvider: Orders changed, saving to localStorage:', orders.length)
    try {
      if (orders.length > 0) {
        localStorage.setItem('ramza_orders', JSON.stringify(orders))
        console.log('OrderTrackingProvider: Saved orders to localStorage:', orders.length)
      } else {
        console.log('OrderTrackingProvider: No orders to save to localStorage')
      }
    } catch (error) {
      console.error('OrderTrackingProvider: Failed to save orders to localStorage:', error)
    }
  }, [orders])

  // Save selected order to localStorage
  useEffect(() => {
    console.log('OrderTrackingProvider: Selected order changed, saving to localStorage:', selectedOrder)
    try {
      if (selectedOrder) {
        localStorage.setItem('ramza_selected_order', JSON.stringify(selectedOrder))
        console.log('OrderTrackingProvider: Saved selected order to localStorage')
      } else {
        localStorage.removeItem('ramza_selected_order')
        console.log('OrderTrackingProvider: Removed selected order from localStorage')
      }
    } catch (error) {
      console.error('OrderTrackingProvider: Failed to save selected order to localStorage:', error)
    }
  }, [selectedOrder])

  const updateOrders = (newOrders) => {
    // Merge new orders with existing ones to prevent data loss
    setOrders(prevOrders => {
      // Create a map of existing orders for quick lookup
      const existingOrdersMap = new Map(prevOrders.map(order => [order.id, order]))
      
      // Process new orders and update existing ones
      const updatedOrders = newOrders.map(newOrder => {
        const existingOrder = existingOrdersMap.get(newOrder.id)
        if (existingOrder) {
          // Merge new data with existing data
          return { ...existingOrder, ...newOrder }
        }
        return newOrder
      })
      
      // Add any existing orders that weren't in the new data
      const newOrdersMap = new Map(newOrders.map(order => [order.id, order]))
      const additionalOrders = prevOrders.filter(order => !newOrdersMap.has(order.id))
      
      // Combine updated orders with additional orders and sort by creation date
      const mergedOrders = [...updatedOrders, ...additionalOrders].sort((a, b) => 
        new Date(b.created_at) - new Date(a.created_at)
      )
      
      console.log('OrderTrackingProvider: Updated orders in context:', mergedOrders.length)
      return mergedOrders
    })
  }

  const addOrder = (order) => {
    setOrders(prevOrders => {
      // Check if order already exists
      const existingOrderIndex = prevOrders.findIndex(o => o.id === order.id)
      if (existingOrderIndex >= 0) {
        // Update existing order
        const updatedOrders = [...prevOrders]
        updatedOrders[existingOrderIndex] = order
        const sortedOrders = updatedOrders.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        console.log('OrderTrackingProvider: Updated existing order in context')
        return sortedOrders
      } else {
        // Add new order
        const newOrders = [order, ...prevOrders]
        console.log('OrderTrackingProvider: Added new order to context')
        return newOrders
      }
    })
  }

  const clearOrders = () => {
    setOrders([])
    try {
      localStorage.removeItem('ramza_orders')
      console.log('OrderTrackingProvider: Cleared orders from localStorage')
    } catch (error) {
      console.error('OrderTrackingProvider: Failed to clear orders from localStorage:', error)
    }
  }

  const clearSelectedOrder = () => {
    setSelectedOrder(null)
    try {
      localStorage.removeItem('ramza_selected_order')
      console.log('OrderTrackingProvider: Cleared selected order from localStorage')
    } catch (error) {
      console.error('OrderTrackingProvider: Failed to clear selected order from localStorage:', error)
    }
  }

  const value = {
    orders,
    selectedOrder,
    loading,
    error,
    updateOrders,
    addOrder,
    setSelectedOrder,
    clearOrders,
    clearSelectedOrder,
    setError,
    setLoading
  }

  return (
    <OrderTrackingContext.Provider value={value}>
      {children}
    </OrderTrackingContext.Provider>
  )
}

export function useOrderTracking() {
  const context = useContext(OrderTrackingContext)
  if (!context) {
    throw new Error('useOrderTracking must be used within an OrderTrackingProvider')
  }
  return context
}