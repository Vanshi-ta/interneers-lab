import React, { useState } from "react";
import Product from "./Product";
import { Product as ProductType } from "../types/Product";

interface Props {
  products: ProductType[];
}

const ProductList: React.FC<Props> = ({ products }) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const handleClick = (id: string) => {
    setExpandedId((prev: string | null) => (prev === id ? null : id));
  };

  return (
    <div style={styles.container}>
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

const styles = {
  container: {
    display: "flex",
    gap: "16px",
    flexWrap: "wrap" as const,
  },
};

export default ProductList;
