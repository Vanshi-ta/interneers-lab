import React, { useState } from "react";
import Product from "./Product";
import { Product as ProductType } from "../types/Product";

interface Props {
  products: ProductType[];
}

const ProductList: React.FC<Props> = ({ products }) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const handleClick = (id: string) => {
    setExpandedId((prev) => (prev === id ? null : id));
  };

  if (!products || products.length === 0) {
    return (
      <div style={{ textAlign: "center", color: "var(--text-muted)" }}>
        No products found matching your filters.
      </div>
    );
  }

  return (
    <div className="product-grid">
      {products.map((product) => (
        <Product
          key={product.id}
          product={product}
          isExpanded={expandedId === product.id}
          onClick={() => handleClick(product.id)}
        />
      ))}
    </div>
  );
};

export default ProductList;
