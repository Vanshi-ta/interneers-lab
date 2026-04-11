import React from "react";

const Header: React.FC = () => {
  return (
    <header className="app-header">
      <h1 className="app-title">Inventory</h1>
      <div>
        <span style={{ fontWeight: 600, color: "var(--text-muted)" }}>
          SignUp Login
        </span>
      </div>
    </header>
  );
};

export default Header;
