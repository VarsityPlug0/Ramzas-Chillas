# Ramza's Chillas - Modern React Frontend

This is a modern React frontend for the Ramza's Chillas restaurant web application, built with React, Tailwind CSS, and Vite.

## 🚀 Features

- **Modern React Architecture**: Component-based structure with React Router
- **State Management**: React Context API for cart management
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Animations**: Smooth transitions with Framer Motion
- **Performance**: Fast loading with Vite bundler
- **Toast Notifications**: User feedback with react-hot-toast

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── Footer.jsx
│   │   ├── MenuCard.jsx
│   │   └── CartItem.jsx
│   │
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Menu.jsx
│   │   ├── Cart.jsx
│   │   └── Checkout.jsx
│   │
│   ├── api/
│   │   └── axiosInstance.js
│   │
│   ├── context/
│   │   └── CartContext.jsx
│   │
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
├── public/
│   └── favicon.ico
│
├── index.html
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── package.json
```

## 🛠️ Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Build for production:**
   ```bash
   npm run build
   ```

5. **Preview production build:**
   ```bash
   npm run preview
   ```

## 🌐 Development

The frontend runs on `http://localhost:3000` and proxies API requests to the Django backend at `http://localhost:8000`.

## 🎨 Design System

- **Colors**: 
  - Primary: `#f59e0b` (Orange)
  - Secondary: `#06b6d4` (Teal)
  - Accent: `#ef4444` (Red)

- **Typography**: Inter font family
- **Spacing**: Consistent 8px grid system
- **Components**: Reusable, accessible components

## 🔧 API Integration

The frontend uses axios for API requests with a proxy setup to communicate with the Django backend. All API calls should be made through the `axiosInstance.js` service.

## 📱 Responsive Features

- Mobile-first design approach
- Flexible grid layouts
- Touch-friendly components
- Adaptive typography
- Smooth animations and transitions

## 🚀 Performance Optimizations

- Code splitting with React.lazy
- Efficient state management
- Optimized images and assets
- Minimal bundle size
- Fast refresh development experience