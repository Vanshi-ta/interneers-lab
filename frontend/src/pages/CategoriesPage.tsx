import React, { useState } from "react";
import Header from "../components/Header";
import Navbar from "../components/Navbar";
import { useCategories } from "../hooks/useCategories";
import { createCategory, updateCategory } from "../services/api";

const CategoriesPage: React.FC = () => {
  const { categories, loading, error, setCategories } = useCategories();

  const [formData, setFormData] = useState({ title: "", description: "" });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editCategoryId, setEditCategoryId] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);

  const handleEditClick = (category: any) => {
    setEditCategoryId(category.id);
    setFormData({
      title: category.title,
      description: category.description || "",
    });
    setFormError(null);
  };

  const handleCancelEdit = () => {
    setEditCategoryId(null);
    setFormData({ title: "", description: "" });
    setFormError(null);
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setFormError(null);

    try {
      if (editCategoryId) {
        // Update existing category
        const updatedCategory = await updateCategory(editCategoryId, formData);
        if (setCategories) {
          setCategories((prev) =>
            prev.map((c) => (c.id === editCategoryId ? updatedCategory : c)),
          );
        }
        setEditCategoryId(null);
      } else {
        // Create new category
        const newCategory = await createCategory(formData);
        if (setCategories) {
          setCategories((prev) => [...prev, newCategory]);
        }
      }
      setFormData({ title: "", description: "" });
    } catch (err: any) {
      setFormError(err.message || "Failed to submit category");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="homepage-wrapper">
      <Header />
      <Navbar />

      <main className="main-content">
        <h2 style={{ marginBottom: "20px" }}>Categories</h2>

        {error && <div className="error-message">{error}</div>}

        <div
          style={{
            marginBottom: "40px",
            background: "var(--surface-color)",
            padding: "24px",
            borderRadius: "var(--radius-lg)",
            boxShadow: "var(--shadow-sm)",
          }}
        >
          <h3>{editCategoryId ? "Edit Category" : "Add New Category"}</h3>
          {formError && (
            <div
              className="error-message"
              style={{ padding: "10px", marginTop: "10px" }}
            >
              {formError}
            </div>
          )}

          <form
            onSubmit={handleSubmit}
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "16px",
              marginTop: "16px",
            }}
          >
            <div>
              <label
                style={{
                  display: "block",
                  marginBottom: "8px",
                  fontWeight: "bold",
                }}
              >
                Title
              </label>
              <input
                type="text"
                name="title"
                value={formData.title}
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
                Description
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                className="filter-input"
                style={{
                  width: "100%",
                  minHeight: "80px",
                  fontFamily: "inherit",
                }}
              />
            </div>

            <div style={{ display: "flex", gap: "12px" }}>
              <button
                type="submit"
                className="btn-page"
                disabled={isSubmitting}
                style={{ background: "var(--primary-color)", color: "white" }}
              >
                {isSubmitting
                  ? "Saving..."
                  : editCategoryId
                    ? "Update Category"
                    : "Add Category"}
              </button>

              {editCategoryId && (
                <button
                  type="button"
                  className="btn-page"
                  onClick={handleCancelEdit}
                  disabled={isSubmitting}
                >
                  Cancel
                </button>
              )}
            </div>
          </form>
        </div>

        {loading ? (
          <div className="loader">Loading categories...</div>
        ) : categories.length === 0 ? (
          <div>No categories found.</div>
        ) : (
          <div className="product-grid">
            {categories.map((category) => (
              <div
                key={category.id}
                className="product-card"
                style={{ display: "flex", flexDirection: "column" }}
              >
                <div style={{ flex: 1 }}>
                  <h3 className="product-title">{category.title}</h3>
                  <p className="product-desc" style={{ marginBottom: "16px" }}>
                    {category.description || "No description available"}
                  </p>
                </div>
                <div
                  style={{
                    borderTop: "1px solid var(--border-color)",
                    paddingTop: "16px",
                  }}
                >
                  <button
                    className="btn-page"
                    style={{ padding: "6px 12px", fontSize: "0.85rem" }}
                    onClick={() => handleEditClick(category)}
                  >
                    Edit
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default CategoriesPage;
