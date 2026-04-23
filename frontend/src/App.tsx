import React from "react";
import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import CategoriesPage from "./pages/CategoriesPage";
import ProductsPage from "./pages/ProductPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/categories" element={<CategoriesPage />} />
      <Route path="/products" element={<HomePage />} />
      <Route path="/products/:id" element={<ProductsPage />} />
      {/* You can add more routes here, e.g., <Route path="/about" element={<About />} /> */}
    </Routes>
  );
}

export default App;
