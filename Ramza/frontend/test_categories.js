// Test script to verify category data handling in frontend
const testCategoriesData = [
  {
    name: "Burgers",
    description: "Juicy burgers with fresh ingredients",
    image: "/media/categories/burgers.jpg"
  },
  {
    name: "Pizzas",
    description: "Wood-fired pizzas with authentic flavors",
    image: null
  },
  {
    name: "Drinks",
    description: "Refreshing beverages to cool you down",
    image: "/media/categories/drinks.jpg"
  },
  {
    name: "Sides",
    description: "Perfect accompaniments to your main dish",
    image: null
  }
];

console.log("Testing category data structure:");
console.log("Categories data:", testCategoriesData);

// Test the mapping function that would be used in Home.jsx
console.log("\nTesting Home page category mapping:");
testCategoriesData.slice(0, 4).forEach((category, index) => {
  console.log(`Category ${index + 1}:`, {
    name: category.name,
    description: category.description,
    hasImage: !!category.image,
    imageUrl: category.image || "No image"
  });
});

// Test the mapping function that would be used in Menu.jsx
console.log("\nTesting Menu page category mapping:");
testCategoriesData.forEach((category, index) => {
  console.log(`Category ${index + 1}:`, {
    name: category.name,
    hasImage: !!category.image,
    imageUrl: category.image || "No image"
  });
});

console.log("\nTest completed successfully!");