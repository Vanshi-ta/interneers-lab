import React from "react";

const Navbar: React.FC = () => {
  return (
    <nav style={styles.nav}>
      <a href="/" style={styles.link}>
        Home
      </a>
      <a href="/products" style={styles.link}>
        Products
      </a>
      <a href="/categories" style={styles.link}>
        Categories
      </a>
    </nav>
  );
};

const styles = {
  nav: {
    display: "flex",
    gap: "20px",
    padding: "10px 20px",
    backgroundColor: "#eee",
  },
  link: {
    textDecoration: "none",
    color: "#240b36",
    fontWeight: "bold",
  },
};

export default Navbar;
