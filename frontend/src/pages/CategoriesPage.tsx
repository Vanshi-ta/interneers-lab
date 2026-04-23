import React from "react";
import Header from "../components/Header";
import Navbar from "../components/Navbar";
import { useCategories } from "../hooks/useCategories";

const CategoriesPage: React.FC = () => {
  const { categories, loading, error } = useCategories();

  return (
    <div className="homepage-wrapper">
      <Header />
      <Navbar />

      <main className="main-content">
        <h2 style={{ marginBottom: "20px" }}>Categories</h2>

        {error && <div className="error-message">{error}</div>}

        {loading ? (
          <div className="loader">Loading categories...</div>
        ) : categories.length === 0 ? (
          <div>No categories found.</div>
        ) : (
          <div className="product-grid">
            {categories.map((category) => (
              <div key={category.id} className="product-card">
                <h3 className="product-title">{category.title}</h3>
                <p className="product-desc">
                  {/*{category.description || "No description available"}*/}
                </p>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default CategoriesPage;
