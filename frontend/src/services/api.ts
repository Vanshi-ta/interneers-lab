import { ProductResponse, Category } from "../types/Product";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";
const CATEGORY_URL =
  process.env.REACT_APP_CATEGORY_URL || "http://127.0.0.1:8001";

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
