import React from "react";
import { useNavigate } from "react-router-dom";
import { Product as ProductType } from "../types/Product";

interface Props {
  product: ProductType;
  isExpanded: boolean;
  onClick: () => void;
}

const Product: React.FC<Props> = ({ product, isExpanded, onClick }) => {
  const navigate = useNavigate();

  return (
    <div
      className={`product-card ${isExpanded ? "expanded" : ""}`}
      onClick={onClick}
    >
      <div className="product-content">
        <div className="product-brand">{product.brand}</div>
        <h3 className="product-title">{product.name}</h3>
        {isExpanded && <p className="product-desc">{product.description}</p>}
      </div>

      <div className="product-footer">
        <span className="product-price">
          ${Number(product.price).toFixed(2)}
        </span>
        <span className="product-category">
          {product.category ? product.category.title : "Uncategorized"}
        </span>
        <button
          className="btn-page"
          style={{ padding: "6px 12px", fontSize: "0.85rem" }}
          onClick={(e) => {
            e.stopPropagation();
            navigate(`/products/${product.id}`);
          }}
        >
          View Details
        </button>
      </div>
    </div>
  );
};

export default Product;
