import { ProductResponse, Category, Product } from "../types/Product";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";
const CATEGORY_URL =
  process.env.REACT_APP_CATEGORY_URL || "http://127.0.0.1:8000";

export interface FetchProductsParams {
  page?: number;
  limit?: number;
  search?: string;
  brand?: string;
  category?: string;
}

export const fetchProducts = async (
  params: FetchProductsParams,
): Promise<ProductResponse> => {
  const queryParams = new URLSearchParams();

  if (params.page) queryParams.append("page", params.page.toString());
  if (params.limit) queryParams.append("limit", params.limit.toString());
  if (params.search) queryParams.append("name", params.search);
  if (params.brand) queryParams.append("brand", params.brand);
  if (params.category) queryParams.append("category", params.category);

  const response = await fetch(
    `${API_URL}/products/?${queryParams.toString()}`,
  );
  if (!response.ok) {
    throw new Error("Failed to fetch products");
  }

  return response.json();
};

export const fetchCategories = async (): Promise<Category[]> => {
  const response = await fetch(`${CATEGORY_URL}/categories/`);
  if (!response.ok) {
    throw new Error("Failed to fetch categories");
  }

  return response.json();
};

export const fetchProductById = async (id: string): Promise<Product> => {
  const response = await fetch(`${API_URL}/products/${id}/`);

  if (!response.ok) {
    throw new Error("Failed to fetch");
  }

  const data = await response.json();
  return data; // IMPORTANT: return directly, not data.data
};

export const updateProduct = async (
  id: string,
  data: Partial<Product>,
): Promise<Product> => {
  const response = await fetch(`${API_URL}/products/${id}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error("Failed to update product");
  }
  return response.json();
};

export const createCategory = async (
  data: Partial<Category>,
): Promise<Category> => {
  const response = await fetch(`${CATEGORY_URL}/categories/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error("Failed to create category");
  }
  return response.json();
};

export const updateCategory = async (
  id: string,
  data: Partial<Category>,
): Promise<Category> => {
  const response = await fetch(`${CATEGORY_URL}/categories/${id}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error("Failed to update category");
  }
  return response.json();
};
