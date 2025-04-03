import React from 'react';

const Header = () => {
  return (
    <header className="header">
      <div className="logo">
        <span className="logo-icon">🔒</span>
        <h1>VulnScanner</h1>
      </div>
      <div className="header-controls">
        <button className="btn btn-primary">New Scan</button>
        <div className="user-menu">
          <span className="user-icon">👤</span>
          <span>Admin</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
