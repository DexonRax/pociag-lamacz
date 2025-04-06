import React from 'react';
import { useNavigate } from 'react-router-dom';

const Sidebar = ({ activeView, onNavigate }) => {
  const navigate = useNavigate(); 

  const handleDashboardClick = () => {
    navigate('/');
    onNavigate('dashboard'); 
  };
  const handleScanClick = () => {
    navigate('/Scans');
    onNavigate('scans');
  };
  const handleTrashClick = () => {
    navigate('/Trash');
    onNavigate('trash');
  };
  const handleSettingsClick = () => {
    navigate('/Settings');
    onNavigate('settings');
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
          <li className={activeView === 'trash' ? 'active' : ''}>
            <button onClick={handleTrashClick}>
              <span className="icon">🗑️</span>
              <span>Trash</span>
            </button>
          </li>
          <li className={activeView === 'settings' ? 'active' : ''}>
            <button onClick={handleSettingsClick}>
              <span className="icon">⚙️</span>
              <span>Settings</span>
            </button>
          </li>
        </ul>
      </nav>
      <div className="sidebar-footer">
        <button className={activeView === 'Help' ? 'btn btn-help active' : 'btn btn-help'} onClick={handleHelpClick}>
          <span className="icon">❓</span>
          <span>Help & Support</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;