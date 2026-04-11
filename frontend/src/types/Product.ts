export interface Category {
  id: string;
  title: string;
}

export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  brand: string;
  category?: Category | null;
}

export interface ProductResponse {
  page: number;
  limit: number;
  total: number;
  data: Product[];
}

export interface CategoryResponse {
  id: string;
  title: string;
}
