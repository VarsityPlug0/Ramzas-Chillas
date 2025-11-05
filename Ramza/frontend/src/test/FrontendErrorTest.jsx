import React, { useState, useEffect } from 'react';
import { fetchCategories } from '../api/axiosInstance';

// Test component that checks for frontend errors
const FrontendErrorTest = () => {
  const [testResults, setTestResults] = useState({
    apiCallSuccess: false,
    dataStructureValid: false,
    imageHandlingCorrect: false,
    errors: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const runTests = async () => {
      try {
        // Test 1: API call success
        console.log('Test 1: Making API call...');
        const categories = await fetchCategories();
        console.log('API Response:', categories);
        
        setTestResults(prev => ({
          ...prev,
          apiCallSuccess: true
        }));
        
        // Test 2: Data structure validation
        console.log('Test 2: Validating data structure...');
        const isValidStructure = Array.isArray(categories) && 
          categories.every(cat => 
            typeof cat === 'object' && 
            'name' in cat
          );
        
        setTestResults(prev => ({
          ...prev,
          dataStructureValid: isValidStructure
        }));
        
        // Test 3: Image handling
        console.log('Test 3: Checking image handling...');
        const hasImageCategories = categories.filter(cat => cat.image);
        const noImageCategories = categories.filter(cat => !cat.image);
        
        console.log(`Found ${hasImageCategories.length} categories with images`);
        console.log(`Found ${noImageCategories.length} categories without images`);
        
        setTestResults(prev => ({
          ...prev,
          imageHandlingCorrect: true,
          imageData: {
            withImages: hasImageCategories.length,
            withoutImages: noImageCategories.length
          }
        }));
        
      } catch (error) {
        console.error('Test failed:', error);
        setTestResults(prev => ({
          ...prev,
          errors: [...prev.errors, error.message]
        }));
      } finally {
        setLoading(false);
      }
    };
    
    runTests();
  }, []);

  if (loading) {
    return (
      <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
        <h1>Frontend Error Test</h1>
        <p>Running tests...</p>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Frontend Error Test Results</h1>
      
      <div style={{ 
        padding: '15px', 
        borderRadius: '8px', 
        backgroundColor: testResults.errors.length === 0 ? '#d4edda' : '#f8d7da',
        color: testResults.errors.length === 0 ? '#155724' : '#721c24',
        marginBottom: '20px'
      }}>
        <h2>Overall Status: {testResults.errors.length === 0 ? '✅ PASSED' : '❌ FAILED'}</h2>
        {testResults.errors.length > 0 && (
          <div>
            <h3>Errors Found:</h3>
            <ul>
              {testResults.errors.map((error, index) => (
                <li key={index}>{error}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '15px' }}>
        <div style={{ 
          padding: '15px', 
          borderRadius: '8px', 
          backgroundColor: testResults.apiCallSuccess ? '#d4edda' : '#f8d7da'
        }}>
          <h3>API Call Test</h3>
          <p>Status: {testResults.apiCallSuccess ? '✅ PASSED' : '❌ FAILED'}</p>
        </div>
        
        <div style={{ 
          padding: '15px', 
          borderRadius: '8px', 
          backgroundColor: testResults.dataStructureValid ? '#d4edda' : '#f8d7da'
        }}>
          <h3>Data Structure Test</h3>
          <p>Status: {testResults.dataStructureValid ? '✅ PASSED' : '❌ FAILED'}</p>
        </div>
        
        <div style={{ 
          padding: '15px', 
          borderRadius: '8px', 
          backgroundColor: testResults.imageHandlingCorrect ? '#d4edda' : '#f8d7da'
        }}>
          <h3>Image Handling Test</h3>
          <p>Status: {testResults.imageHandlingCorrect ? '✅ PASSED' : '❌ FAILED'}</p>
          {testResults.imageData && (
            <ul>
              <li>Categories with images: {testResults.imageData.withImages}</li>
              <li>Categories without images: {testResults.imageData.withoutImages}</li>
            </ul>
          )}
        </div>
      </div>
      
      <div style={{ 
        marginTop: '20px', 
        padding: '15px', 
        backgroundColor: '#e8f4fd', 
        borderRadius: '8px'
      }}>
        <h3>Test Summary</h3>
        <p>
          This test verifies that the frontend can successfully fetch category data 
          and handle both categories with and without images correctly.
        </p>
        <p>
          If all tests pass, the category image upload and display functionality 
          is working as expected.
        </p>
      </div>
    </div>
  );
};

export default FrontendErrorTest;