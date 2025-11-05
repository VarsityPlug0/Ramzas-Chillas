import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Test component that simulates the actual API integration
const ApiIntegrationTest = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Simulate the actual API call that the frontend makes
    const fetchCategories = async () => {
      try {
        setLoading(true);
        // In a real app, this would be: await axios.get('/api/v1/categories/')
        // For this test, we'll simulate the response structure
        const response = {
          data: {
            categories: [
              {
                name: "vunandzi",
                description: "",
                image: "/media/categories/Screenshot_2025-09-08_200942.png"
              },
              {
                name: "Pizzas",
                description: "",
                image: null
              },
              {
                name: "Drinks",
                description: "",
                image: null
              },
              {
                name: "Sides",
                description: "",
                image: null
              }
            ]
          }
        };
        
        setCategories(response.data.categories);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch categories: ' + err.message);
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  if (loading) {
    return <div>Loading categories...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>API Integration Test</h1>
      <p>This component tests the actual API data handling in the frontend.</p>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
        {categories.map((category, index) => (
          <div key={index} style={{ border: '1px solid #ccc', borderRadius: '8px', padding: '15px' }}>
            <h2>{category.name}</h2>
            <p>{category.description || 'No description'}</p>
            {category.image ? (
              <div>
                <p>Image URL: {category.image}</p>
                <img 
                  src={category.image} 
                  alt={category.name} 
                  style={{ maxWidth: '100%', height: 'auto', borderRadius: '4px' }}
                  onError={(e) => {
                    console.log('Image failed to load:', category.image);
                    e.target.style.display = 'none';
                  }}
                />
              </div>
            ) : (
              <div style={{ 
                backgroundColor: '#f0f0f0', 
                height: '150px', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                borderRadius: '4px'
              }}>
                <span>No Image Available</span>
              </div>
            )}
          </div>
        ))}
      </div>
      
      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#e8f4fd', borderRadius: '8px' }}>
        <h3>Test Results:</h3>
        <ul>
          <li>Total categories: {categories.length}</li>
          <li>Categories with images: {categories.filter(cat => cat.image).length}</li>
          <li>Categories without images: {categories.filter(cat => !cat.image).length}</li>
        </ul>
      </div>
    </div>
  );
};

export default ApiIntegrationTest;