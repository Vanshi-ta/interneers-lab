import React from "react";
import { Product as ProductType } from "../types/Product";

interface Props {
  product: ProductType;
  isExpanded: boolean;
  onClick: () => void;
}

const Product: React.FC<Props> = ({ product, isExpanded, onClick }) => {
  return (
    <div
      className={`product-card ${isExpanded ? "expanded" : ""}`}
      onClick={onClick}
    >
      <div className="product-content">
        <div className="product-brand">{product.brand}</div>
        <h3 className="product-title">{product.name}</h3>
        <p className="product-desc">
          Premium quality product out of the box with extensive specifications
          and beautiful finish.
        </p>
      </div>

      <div className="product-footer">
        <span className="product-price">
          ${Number(product.price).toFixed(2)}
        </span>
        <span className="product-category">
          {product.category ? product.category.title : "Uncategorized"}
        </span>
      </div>
    </div>
  );
};

export default Product;
