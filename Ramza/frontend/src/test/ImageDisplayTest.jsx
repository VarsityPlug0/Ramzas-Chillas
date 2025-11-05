import React, { useState, useEffect } from 'react';

const ImageDisplayTest = () => {
  const [imageUrl, setImageUrl] = useState('');
  const [imageStatus, setImageStatus] = useState('loading');

  useEffect(() => {
    // Use the actual image URL from our media directory
    const url = '/media/categories/Screenshot_2025-09-18_234901.png';
    setImageUrl(url);
  }, []);

  const handleImageLoad = () => {
    setImageStatus('loaded');
  };

  const handleImageError = () => {
    setImageStatus('error');
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Image Display Test</h1>
      <p>Testing if category images are now displaying correctly with the updated proxy configuration.</p>
      
      <div style={{ marginTop: '20px' }}>
        <h2>Image Test:</h2>
        <p>Image Status: <strong>{imageStatus}</strong></p>
        <p>Image URL: <code>{imageUrl}</code></p>
        
        {imageUrl && (
          <div style={{ marginTop: '20px' }}>
            <img 
              src={imageUrl} 
              alt="Test Category" 
              style={{ maxWidth: '100%', height: 'auto', border: '1px solid #ccc', borderRadius: '8px' }}
              onLoad={handleImageLoad}
              onError={handleImageError}
            />
            {imageStatus === 'error' && (
              <p style={{ color: 'red' }}>❌ Failed to load image. Check the console for errors.</p>
            )}
            {imageStatus === 'loaded' && (
              <p style={{ color: 'green' }}>✅ Image loaded successfully!</p>
            )}
          </div>
        )}
      </div>
      
      <div style={{ 
        marginTop: '20px', 
        padding: '15px', 
        backgroundColor: '#e8f4fd', 
        borderRadius: '8px'
      }}>
        <h3>Test Information:</h3>
        <p>
          This test verifies that images from the Django media directory can now be loaded 
          through the Vite development server with the updated proxy configuration.
        </p>
        <p>
          If the image loads successfully, the category images should now display correctly 
          in the main application.
        </p>
      </div>
    </div>
  );
};

export default ImageDisplayTest;