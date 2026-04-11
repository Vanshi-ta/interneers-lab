import React from "react";
import { Link } from "react-router-dom";

const Navbar: React.FC = () => {
  return (
    <nav className="app-navbar">
      <Link to="/" className="nav-link">
        Home
      </Link>
      <Link to="/products" className="nav-link">
        Products
      </Link>
      <Link to="/about" className="nav-link">
        About
      </Link>
      <Link to="/contact" className="nav-link">
        Contact
      </Link>
    </nav>
  );
};

export default Navbar;
