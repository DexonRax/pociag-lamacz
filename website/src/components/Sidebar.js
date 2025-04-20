import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaTrash } from "react-icons/fa";
import { MdOutlineDashboard } from "react-icons/md";
import { IoSettingsOutline, IoHelp  } from "react-icons/io5";
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
              <span className="icon"><MdOutlineDashboard /></span>
              <span>Panel główny</span>
            </button>
          </li>
          <li className={activeView === 'trash' ? 'active' : ''}>
            <button onClick={handleTrashClick}>
              <span className="icon"><FaTrash /></span>
              <span>Śmietnik</span>
            </button>
          </li>
          <li className={activeView === 'settings' ? 'active' : ''}>
            <button onClick={handleSettingsClick}>
              <span className="icon"><IoSettingsOutline /></span>
              <span>Ustawienia</span>
            </button>
          </li>
        </ul>
      </nav>
      <div className="sidebar-footer">
        <button className={activeView === 'Help' ? 'btn btn-help active' : 'btn btn-help'} onClick={handleHelpClick}>
          <span className="icon"><IoHelp /></span>
          <span>Pomoc</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;