import React from 'react';

// Mock test component to verify category data handling
const CategoryDataTest = () => {
  // Sample data that matches our API response
  const mockCategories = [
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
  ];

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Category Data Test</h1>
      <p>This component tests the new category data structure.</p>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
        {mockCategories.map((category, index) => (
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
    </div>
  );
};

export default CategoryDataTest;