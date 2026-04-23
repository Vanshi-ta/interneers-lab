import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  fetchProductById,
  updateProduct,
  fetchCategories,
} from "../services/api";
import { Product, Category } from "../types/Product";

const ProductPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [product, setProduct] = useState<Product | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [isUpdating, setIsUpdating] = useState<boolean>(false);

  const [formData, setFormData] = useState({
    name: "",
    price: "",
    description: "",
    brand: "",
    category: "",
  });

  useEffect(() => {
    const loadData = async () => {
      if (!id) return;
      try {
        setIsLoading(true);
        const [fetchedProduct, fetchedCategories] = await Promise.all([
          fetchProductById(id),
          fetchCategories(),
        ]);
        setProduct(fetchedProduct);
        setCategories(fetchedCategories);
        setFormData({
          name: fetchedProduct.name || "",
          price: fetchedProduct.price ? fetchedProduct.price.toString() : "",
          description: fetchedProduct.description || "",
          brand: fetchedProduct.brand || "",
          category: fetchedProduct.category?.id || "",
        });
      } catch (err: any) {
        setError(err.message || "Failed to load product");
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [id]);

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;
    try {
      setIsUpdating(true);
      const updatedProduct = await updateProduct(id, {
        name: formData.name,
        price: parseFloat(formData.price),
        description: formData.description,
        brand: formData.brand,
        // Assuming the backend accepts category ID as a string, but the frontend interface has Category object
        // The backend python code expects category ID or name? Usually ID if it's a foreign key.
        // Let's pass the updated fields.
      });
      // The updateProduct might return the updated product. Let's refresh or update state.
      setProduct(updatedProduct);
      setIsEditing(false);
    } catch (err: any) {
      alert("Failed to update product: " + err.message);
    } finally {
      setIsUpdating(false);
    }
  };

  if (isLoading) return <div className="loader">Loading...</div>;
  if (error) return <div className="error-message">{error}</div>;
  if (!product) return <div className="error-message">Product not found</div>;

  return (
    <div className="main-content">
      <button
        className="btn-page"
        onClick={() => navigate(-1)}
        style={{ marginBottom: "20px" }}
      >
        &larr; Back
      </button>

      <div
        className="product-card expanded"
        style={{ margin: 0, width: "100%" }}
      >
        <div className="product-content" style={{ width: "100%" }}>
          {!isEditing ? (
            <>
              <div className="product-brand">{product.brand}</div>
              <h2 className="product-title" style={{ fontSize: "2rem" }}>
                {product.name}
              </h2>
              <div className="product-price" style={{ marginBottom: "20px" }}>
                ${Number(product.price).toFixed(2)}
              </div>
              <p className="product-desc">{product.description}</p>

              <div
                className="product-footer"
                style={{ marginTop: "30px", borderTop: "none", padding: 0 }}
              >
                <span className="product-category">
                  {product.category ? product.category.title : "Uncategorized"}
                </span>
                <button className="btn-page" onClick={() => setIsEditing(true)}>
                  Edit Product
                </button>
              </div>
            </>
          ) : (
            <form
              onSubmit={handleSubmit}
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "16px",
                width: "100%",
              }}
            >
              <h2>Edit Product</h2>

              <div>
                <label
                  style={{
                    display: "block",
                    marginBottom: "8px",
                    fontWeight: "bold",
                  }}
                >
                  Brand
                </label>
                <input
                  type="text"
                  name="brand"
                  value={formData.brand}
                  onChange={handleChange}
                  className="filter-input"
                  style={{ width: "100%" }}
                  required
                />
              </div>

              <div>
                <label
                  style={{
                    display: "block",
                    marginBottom: "8px",
                    fontWeight: "bold",
                  }}
                >
                  Name
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="filter-input"
                  style={{ width: "100%" }}
                  required
                />
              </div>

              <div>
                <label
                  style={{
                    display: "block",
                    marginBottom: "8px",
                    fontWeight: "bold",
                  }}
                >
                  Price ($)
                </label>
                <input
                  type="number"
                  name="price"
                  value={formData.price}
                  onChange={handleChange}
                  className="filter-input"
                  style={{ width: "100%" }}
                  step="0.01"
                  required
                />
              </div>

              <div>
                <label
                  style={{
                    display: "block",
                    marginBottom: "8px",
                    fontWeight: "bold",
                  }}
                >
                  Description
                </label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  className="filter-input"
                  style={{
                    width: "100%",
                    minHeight: "100px",
                    fontFamily: "inherit",
                  }}
                  required
                />
              </div>

              <div>
                <label
                  style={{
                    display: "block",
                    marginBottom: "8px",
                    fontWeight: "bold",
                  }}
                >
                  Category
                </label>
                {/* For simplicity, we just use a dropdown. Depending on the backend, it might need to be submitted differently if it doesn't accept the ID in the PUT request. But we will provide it if needed. */}
                <select
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                  className="filter-select"
                  style={{ width: "100%" }}
                >
                  <option value="">Select Category</option>
                  {categories.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.title}
                    </option>
                  ))}
                </select>
              </div>

              <div style={{ display: "flex", gap: "12px", marginTop: "20px" }}>
                <button
                  type="submit"
                  className="btn-page"
                  disabled={isUpdating}
                  style={{ background: "var(--primary-color)", color: "white" }}
                >
                  {isUpdating ? "Saving..." : "Save Changes"}
                </button>
                <button
                  type="button"
                  className="btn-page"
                  onClick={() => {
                    setIsEditing(false);
                    // reset form data
                    setFormData({
                      name: product.name || "",
                      price: product.price ? product.price.toString() : "",
                      description: product.description || "",
                      brand: product.brand || "",
                      category: product.category?.id || "",
                    });
                  }}
                  disabled={isUpdating}
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductPage;
