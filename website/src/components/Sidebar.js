import React from 'react';
import { useNavigate } from 'react-router-dom';

const Sidebar = ({ activeView, onNavigate }) => {
  const navigate = useNavigate(); // Hook do nawigacji

  const handleDashboardClick = () => {
    navigate('/'); // Przekierowanie na stronę główną
    onNavigate('dashboard'); // Zachowujemy zgodność z App.js
  };
  const handleHelpClick = () => {
    navigate('/Help');
    onNavigate('Help');
  };
  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        <ul>
          <li className={activeView === 'dashboard' ? 'active' : ''}>
            <button onClick={handleDashboardClick}>
              <span className="icon">📊</span>
              <span>Dashboard</span>
            </button>
          </li>
          <li className={activeView === 'scans' ? 'active' : ''}>
            <button onClick={() => onNavigate('scans')}>
              <span className="icon">🔍</span>
              <span>Scans</span>
            </button>
          </li>
          <li className={activeView === 'reports' ? 'active' : ''}>
            <button onClick={() => onNavigate('reports')}>
              <span className="icon">📄</span>
              <span>Reports</span>
            </button>
          </li>
          <li className={activeView === 'settings' ? 'active' : ''}>
            <button onClick={() => onNavigate('settings')}>
              <span className="icon">⚙️</span>
              <span>Settings</span>
            </button>
          </li>
        </ul>
      </nav>
      <div className="sidebar-footer">
        <button className="btn btn-help" onClick={handleHelpClick}>
          <span className="icon">❓</span>
          <span>Help & Support</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;