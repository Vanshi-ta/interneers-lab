import React from "react";
import { Product as ProductType } from "../types/Product";

interface Props {
  product: ProductType;
  isExpanded: boolean;
  onClick: () => void;
}

const Product: React.FC<Props> = ({ product, isExpanded, onClick }) => {
  return (
    <div style={styles.card} onClick={onClick}>
      <h3>{product.name}</h3>
      <p>₹{product.price}</p>
      <p>{product.brand}</p>

      {isExpanded && (
        <div style={styles.details}>
          <p>Category: {product.category?.title || "No Category"}</p>
          <p>Product ID: {product.id}</p>
          <p>More details coming soon...</p>
        </div>
      )}
    </div>
  );
};

const styles = {
  card: {
    border: "1px solid #ccc",
    padding: "12px",
    borderRadius: "8px",
    width: "250px",
    cursor: "pointer",
  },
  details: {
    marginTop: "10px",
    background: "#f5f5f5",
    padding: "8px",
    borderRadius: "6px",
  },
};

export default Product;
