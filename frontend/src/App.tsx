import React from "react";
import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      {/* You can add more routes here, e.g., <Route path="/about" element={<About />} /> */}
    </Routes>
  );
}

export default App;
