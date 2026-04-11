import React, { useEffect, useState } from "react";
import Header from "./components/Header";
import Navbar from "./components/Navbar";
import ProductList from "./components/ProductList";
import { Product, ProductResponse } from "./types/Product";

function App() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);

        const response = await fetch("http://127.0.0.1:8000/products/");

        if (!response.ok) {
          throw new Error("Failed to fetch products");
        }

        const data: ProductResponse = await response.json();

        setProducts(data.data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return (
    <div>
      <Header />
      <Navbar />

      <main style={{ padding: "20px" }}>
        {loading && <p>Loading products...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}
        {!loading && !error && <ProductList products={products} />}
      </main>
    </div>
  );
}

export default App;
