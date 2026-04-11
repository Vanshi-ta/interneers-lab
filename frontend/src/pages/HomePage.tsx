import React, { useCallback } from "react";
import { useSearchParams } from "react-router-dom";
import Header from "../components/Header";
import Navbar from "../components/Navbar";
import ProductList from "../components/ProductList";
import Filters from "../components/Filters";
import Pagination from "../components/Pagination";
import { useProducts } from "../hooks/useProducts";
import { useCategories } from "../hooks/useCategories";

const HomePage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  // Read state from URL
  const search = searchParams.get("search") || "";
  const brand = searchParams.get("brand") || "";
  const category = searchParams.get("category") || "";
  const page = parseInt(searchParams.get("page") || "1", 10);
  const limit = 6; // Hardcoded limit per page

  // Fetch data via custom hooks
  const { categories } = useCategories();
  const { products, total, loading, error } = useProducts({
    page,
    limit,
    search,
    brand,
    category,
  });

  // State update handlers
  const updateParams = useCallback(
    (key: string, value: string) => {
      setSearchParams((prev) => {
        const newParams = new URLSearchParams(prev);
        if (value) {
          newParams.set(key, value);
        } else {
          newParams.delete(key);
        }
        // When changing filters, reset to page 1
        if (key !== "page") {
          newParams.set("page", "1");
        }
        return newParams;
      });
    },
    [setSearchParams],
  );

  const handleReset = () => {
    setSearchParams(new URLSearchParams());
  };

  return (
    <div className="homepage-wrapper">
      <Header />
      <Navbar />

      <main className="main-content">
        <Filters
          search={search}
          brand={brand}
          category={category}
          categories={categories}
          onSearchChange={(val) => updateParams("search", val)}
          onBrandChange={(val) => updateParams("brand", val)}
          onCategoryChange={(val) => updateParams("category", val)}
          onReset={handleReset}
        />

        {error && <div className="error-message">{error}</div>}

        {loading ? (
          <div className="loader">Loading products...</div>
        ) : (
          <>
            <ProductList products={products} />
            <Pagination
              page={page}
              total={total}
              limit={limit}
              onPageChange={(p) => updateParams("page", p.toString())}
            />
          </>
        )}
      </main>
    </div>
  );
};

export default HomePage;
