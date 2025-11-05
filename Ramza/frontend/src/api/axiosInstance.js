import axios from 'axios'

// Create an axios instance with default configuration
const apiClient = axios.create({
  baseURL: '/api/v1', // Updated to use the new API version
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // You can add auth tokens here if needed
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Handle unauthorized access
      console.error('Unauthorized access - redirecting to login')
    } else if (error.response?.status === 500) {
      console.error('Server error occurred')
    }
    
    return Promise.reject(error)
  }
)

// API service functions
export const fetchMenuItems = async () => {
  try {
    const response = await apiClient.get('/menu-items/')
    return response.data.menu_items
  } catch (error) {
    console.error('Error fetching menu items:', error)
    throw error
  }
}

export const fetchCategories = async () => {
  try {
    const response = await apiClient.get('/categories/')
    return response.data.categories
  } catch (error) {
    console.error('Error fetching categories:', error)
    throw error
  }
}

export const fetchFeaturedItems = async () => {
  try {
    const response = await apiClient.get('/featured-items/')
    return response.data.featured_items
  } catch (error) {
    console.error('Error fetching featured items:', error)
    throw error
  }
}

export const fetchSiteSettings = async () => {
  try {
    const response = await apiClient.get('/site-settings/')
    return response.data.site_settings
  } catch (error) {
    console.error('Error fetching site settings:', error)
    throw error
  }
}

export const fetchContentSections = async () => {
  try {
    const response = await apiClient.get('/content-sections/')
    return response.data.content_sections
  } catch (error) {
    console.error('Error fetching content sections:', error)
    throw error
  }
}

export const fetchSiteImages = async () => {
  try {
    const response = await apiClient.get('/site-images/')
    return response.data.site_images
  } catch (error) {
    console.error('Error fetching site images:', error)
    throw error
  }
}

export const fetchTestimonials = async () => {
  try {
    const response = await apiClient.get('/testimonials/')
    return response.data.testimonials
  } catch (error) {
    console.error('Error fetching testimonials:', error)
    throw error
  }
}

export default apiClient