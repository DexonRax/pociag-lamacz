import React from 'react';

const Sidebar = ({ activeView, onNavigate }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'scans', label: 'Scans', icon: '🔍' },
    { id: 'reports', label: 'Reports', icon: '📄' },
    { id: 'settings', label: 'Settings', icon: '⚙️' },
  ];

  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        <ul>
          {menuItems.map(item => (
            <li key={item.id} className={activeView === item.id ? 'active' : ''}>
              <button onClick={() => onNavigate(item.id)}>
                <span className="icon">{item.icon}</span>
                <span>{item.label}</span>
              </button>
            </li>
          ))}
        </ul>
      </nav>
      <div className="sidebar-footer">
        <button className="btn btn-help">
          <span className="icon">❓</span>
          <span>Help & Support</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;