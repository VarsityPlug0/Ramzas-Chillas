import React, { createContext, useContext, useState, useEffect } from 'react'
import toast from 'react-hot-toast'
import { fetchMenuItems, fetchCategories, fetchFeaturedItems, fetchSiteSettings, fetchContentSections, fetchSiteImages, fetchTestimonials } from '../api/axiosInstance'

const AppContext = createContext()

export function AppProvider({ children }) {
  const [menuItems, setMenuItems] = useState([])
  const [categories, setCategories] = useState([])
  const [featuredItems, setFeaturedItems] = useState([])
  const [siteSettings, setSiteSettings] = useState(null)
  const [contentSections, setContentSections] = useState(null)
  const [siteImages, setSiteImages] = useState(null)
  const [testimonials, setTestimonials] = useState([])
  const [cartItems, setCartItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Load cart from localStorage on initial render
  useEffect(() => {
    const savedCart = localStorage.getItem('ramza_cart')
    if (savedCart) {
      try {
        setCartItems(JSON.parse(savedCart))
      } catch (error) {
        console.error('Failed to parse cart data:', error)
        setCartItems([])
      }
    }
  }, [])

  // Save cart to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('ramza_cart', JSON.stringify(cartItems))
  }, [cartItems])

  // Fetch data from API on initial render
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        
        // Fetch each API endpoint individually to handle errors gracefully
        try {
          const items = await fetchMenuItems()
          setMenuItems(items)
        } catch (err) {
          console.error('Error fetching menu items:', err)
        }
        
        try {
          const cats = await fetchCategories()
          setCategories(cats)
        } catch (err) {
          console.error('Error fetching categories:', err)
        }
        
        try {
          const featured = await fetchFeaturedItems()
          setFeaturedItems(featured)
        } catch (err) {
          console.error('Error fetching featured items:', err)
        }
        
        try {
          const settings = await fetchSiteSettings()
          setSiteSettings(settings)
        } catch (err) {
          console.error('Error fetching site settings:', err)
        }
        
        try {
          const content = await fetchContentSections()
          setContentSections(content)
        } catch (err) {
          console.error('Error fetching content sections:', err)
        }
        
        try {
          const images = await fetchSiteImages()
          setSiteImages(images)
        } catch (err) {
          console.error('Error fetching site images:', err)
        }
        
        try {
          const testimonialsData = await fetchTestimonials()
          setTestimonials(testimonialsData)
        } catch (err) {
          console.error('Error fetching testimonials:', err)
          // Set empty array if testimonials fail to load
          setTestimonials([])
        }
        
        setError(null)
      } catch (err) {
        console.error('Error fetching data:', err)
        setError('Failed to load data from server')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const addToCart = (item) => {
    setCartItems(prevItems => {
      const existingItem = prevItems.find(cartItem => cartItem.id === item.id)
      
      if (existingItem) {
        toast.success(`${item.name} quantity updated!`)
        return prevItems.map(cartItem =>
          cartItem.id === item.id
            ? { ...cartItem, quantity: cartItem.quantity + 1 }
            : cartItem
        )
      } else {
        toast.success(`${item.name} added to cart!`)
        return [...prevItems, { ...item, quantity: 1 }]
      }
    })
  }

  const removeFromCart = (itemId) => {
    setCartItems(prevItems => {
      const itemToRemove = prevItems.find(item => item.id === itemId)
      if (itemToRemove) {
        toast.success(`${itemToRemove.name} removed from cart!`)
      }
      return prevItems.filter(item => item.id !== itemId)
    })
  }

  const updateQuantity = (itemId, quantity) => {
    if (quantity <= 0) {
      removeFromCart(itemId)
      return
    }

    setCartItems(prevItems =>
      prevItems.map(item =>
        item.id === itemId ? { ...item, quantity } : item
      )
    )
  }

  const clearCart = () => {
    setCartItems([])
    toast.success('Cart cleared!')
  }

  const getCartTotal = () => {
    return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0)
  }

  const getCartCount = () => {
    return cartItems.reduce((count, item) => count + item.quantity, 0)
  }

  const value = {
    menuItems,
    categories,
    featuredItems,
    siteSettings,
    contentSections,
    siteImages,
    testimonials,
    cartItems,
    loading,
    error,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    getCartTotal,
    getCartCount
  }

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useApp must be used within an AppProvider')
  }
  return context
}

export function useCart() {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useCart must be used within an AppProvider')
  }
  return context
}
