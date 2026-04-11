import React from "react";
import { Category } from "../types/Product";

interface Props {
  search: string;
  brand: string;
  category: string;
  categories: Category[];

  onSearchChange: (val: string) => void;
  onBrandChange: (val: string) => void;
  onCategoryChange: (val: string) => void;
  onReset: () => void;
}

const Filters: React.FC<Props> = ({
  search,
  brand,
  category,
  categories,
  onSearchChange,
  onBrandChange,
  onCategoryChange,
  onReset,
}) => {
  return (
    <div className="filters-container">
      <input
        className="filter-input"
        type="text"
        placeholder="Search product..."
        value={search}
        onChange={(e) => onSearchChange(e.target.value)}
      />

      <input
        className="filter-input"
        type="text"
        placeholder="Filter by brand..."
        value={brand}
        onChange={(e) => onBrandChange(e.target.value)}
      />

      <select
        className="filter-select"
        value={category}
        onChange={(e) => onCategoryChange(e.target.value)}
      >
        <option value="">All Categories</option>
        {categories.map((c) => (
          <option key={c.id} value={c.id}>
            {c.title}
          </option>
        ))}
      </select>

      <button className="btn-reset" onClick={onReset}>
        Reset
      </button>
    </div>
  );
};

export default Filters;
