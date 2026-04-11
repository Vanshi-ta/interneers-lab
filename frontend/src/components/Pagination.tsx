import React from "react";

interface Props {
  page: number;
  total: number;
  limit: number;
  onPageChange: (newPage: number) => void;
}

const Pagination: React.FC<Props> = ({ page, total, limit, onPageChange }) => {
  const totalPages = Math.ceil(total / limit);

  if (totalPages <= 1) return null;

  return (
    <div className="pagination-container">
      <button
        className="btn-page"
        disabled={page <= 1}
        onClick={() => onPageChange(page - 1)}
      >
        Previous
      </button>

      <span className="page-info">
        Page {page} of {totalPages}
      </span>

      <button
        className="btn-page"
        disabled={page >= totalPages}
        onClick={() => onPageChange(page + 1)}
      >
        Next
      </button>
    </div>
  );
};

export default Pagination;
