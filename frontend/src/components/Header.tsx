import React from "react";

const Header: React.FC = () => {
  return (
    <header style={styles.header}>
      <h1>Product Dashboard</h1>
    </header>
  );
};

const styles = {
  header: {
    backgroundColor: "#240b36",
    color: "white",
    padding: "16px",
    textAlign: "center" as const,
  },
};

export default Header;
