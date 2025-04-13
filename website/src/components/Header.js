import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="header">
      <div className="logo">
        <h1>nuln</h1>
      </div>
      <div className="header-controls">
        <Link to="/scans">
          <button className="btn btn-primary">Nowy skan</button>
        </Link>
      </div>
    </header>
  );
};

export default Header;