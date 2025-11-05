import React, { useState, useEffect } from 'react';
import { fetchCategories } from '../api/axiosInstance';

const CompleteCategoryTest = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [imageLoadStatus, setImageLoadStatus] = useState({});

  useEffect(() => {
    const loadCategories = async () => {
      try {
        setLoading(true);
        const data = await fetchCategories();
        setCategories(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadCategories();
  }, []);

  const handleImageLoad = (categoryName) => {
    setImageLoadStatus(prev => ({
      ...prev,
      [categoryName]: 'loaded'
    }));
  };

  const handleImageError = (categoryName) => {
    setImageLoadStatus(prev => ({
      ...prev,
      [categoryName]: 'error'
    }));
  };

  if (loading) {
    return (
      <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
        <h1>Complete Category Test</h1>
        <p>Loading categories...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
        <h1>Complete Category Test</h1>
        <p style={{ color: 'red' }}>Error: {error}</p>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Complete Category Test</h1>
      <p>Testing the complete category image flow with the updated proxy configuration.</p>
      
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', 
        gap: '20px',
        marginTop: '20px'
      }}>
        {categories.map((category, index) => (
          <div 
            key={index} 
            style={{ 
              border: '1px solid #ccc', 
              borderRadius: '8px', 
              padding: '15px',
              backgroundColor: '#f9f9f9'
            }}
          >
            <h2>{category.name}</h2>
            <p>{category.description || 'No description'}</p>
            
            {category.image ? (
              <div>
                <p>Image URL: <code>{category.image}</code></p>
                <p>Load Status: <strong>{imageLoadStatus[category.name] || 'pending'}</strong></p>
                <img 
                  src={category.image} 
                  alt={category.name} 
                  style={{ 
                    maxWidth: '100%', 
                    height: '200px', 
                    objectFit: 'cover',
                    border: '1px solid #ddd', 
                    borderRadius: '4px',
                    marginTop: '10px'
                  }}
                  onLoad={() => handleImageLoad(category.name)}
                  onError={() => handleImageError(category.name)}
                />
                {imageLoadStatus[category.name] === 'error' && (
                  <p style={{ color: 'red', marginTop: '5px' }}>❌ Failed to load image</p>
                )}
                {imageLoadStatus[category.name] === 'loaded' && (
                  <p style={{ color: 'green', marginTop: '5px' }}>✅ Image loaded successfully</p>
                )}
              </div>
            ) : (
              <div style={{ 
                backgroundColor: '#f0f0f0', 
                height: '200px', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                borderRadius: '4px',
                marginTop: '10px'
              }}>
                <span>No Image Available</span>
              </div>
            )}
          </div>
        ))}
      </div>
      
      <div style={{ 
        marginTop: '30px', 
        padding: '15px', 
        backgroundColor: '#e8f4fd', 
        borderRadius: '8px'
      }}>
        <h3>Test Results Summary:</h3>
        <ul>
          <li>Total categories: {categories.length}</li>
          <li>Categories with images: {categories.filter(cat => cat.image).length}</li>
          <li>Categories without images: {categories.filter(cat => !cat.image).length}</li>
          <li>Images loaded successfully: {Object.values(imageLoadStatus).filter(status => status === 'loaded').length}</li>
          <li>Images failed to load: {Object.values(imageLoadStatus).filter(status => status === 'error').length}</li>
        </ul>
        
        <h3>Proxy Configuration:</h3>
        <p>
          The Vite proxy has been updated to forward requests to <code>/media</code> paths to the Django server.
          This should resolve the issue with category images not displaying.
        </p>
      </div>
    </div>
  );
};

export default CompleteCategoryTest;