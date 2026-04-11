import { useState, useEffect } from "react";
import { Product } from "../types/Product";
import { fetchProducts, FetchProductsParams } from "../services/api";

export const useProducts = (params: FetchProductsParams) => {
  const [products, setProducts] = useState<Product[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Derive primitive dependencies from the object for useEffect
  const { page, limit, search, brand, category } = params;

  useEffect(() => {
    let active = true;

    const loadProducts = async () => {
      try {
        setLoading(true);
        const data = await fetchProducts({
          page,
          limit,
          search,
          brand,
          category,
        });
        if (active) {
          setProducts(data.data);
          setTotal(data.total);
          setError(null);
        }
      } catch (err) {
        if (active) {
          setError(
            err instanceof Error ? err.message : "An unknown error occurred",
          );
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };

    loadProducts();

    return () => {
      active = false;
    };
  }, [page, limit, search, brand, category]);

  return { products, total, loading, error };
};
