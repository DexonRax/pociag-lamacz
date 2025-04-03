import React, { useState } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import ScanResults from './components/ScanResults';
import VulnerabilityDetails from './components/VulnerabilityDetails';
import Header from './components/Header';

function App() {
  const [activeView, setActiveView] = useState('dashboard');
  const [activeScan, setActiveScan] = useState(null);
  const [activeVulnerability, setActiveVulnerability] = useState(null);

  // Mock scan data
  const scanData = [
    { id: 1, name: 'Web Server Scan', status: 'Complete', vulnerabilities: 14, date: '2025-04-01', severity: 'high' },
    { id: 2, name: 'Database Server Scan', status: 'In Progress', vulnerabilities: 7, date: '2025-04-02', severity: 'medium' },
    { id: 3, name: 'Network Devices Scan', status: 'Scheduled', vulnerabilities: 0, date: '2025-04-03', severity: 'none' },
  ];

  // Mock vulnerability data for the selected scan
  const vulnerabilityData = [
    { id: 101, scanId: 1, name: 'SQL Injection', severity: 'critical', status: 'Open', description: 'SQL injection vulnerability detected in login form' },
    { id: 102, scanId: 1, name: 'Cross-Site Scripting (XSS)', severity: 'high', status: 'Open', description: 'Reflected XSS found in search functionality' },
    { id: 103, scanId: 1, name: 'Outdated SSL Certificate', severity: 'medium', status: 'In Review', description: 'Server uses outdated SSL certificate' },
    { id: 104, scanId: 2, name: 'Default Database Credentials', severity: 'critical', status: 'Open', description: 'Database using default credentials' },
  ];

  const handleNavigation = (view) => {
    setActiveView(view);
    setActiveScan(null);
    setActiveVulnerability(null);
  };

  const handleScanSelect = (scanId) => {
    setActiveScan(scanId);
    setActiveView('scanResults');
  };

  const handleVulnerabilitySelect = (vulnId) => {
    setActiveVulnerability(vulnId);
    setActiveView('vulnerabilityDetails');
  };

  // Render the current view
  const renderView = () => {
    switch (activeView) {
      case 'dashboard':
        return <Dashboard scanData={scanData} onScanSelect={handleScanSelect} />;
      case 'scanResults':
        return (
          <ScanResults 
            scanData={scanData.find(scan => scan.id === activeScan)} 
            vulnerabilities={vulnerabilityData.filter(vuln => vuln.scanId === activeScan)}
            onVulnerabilitySelect={handleVulnerabilitySelect}
          />
        );
      case 'vulnerabilityDetails':
        return (
          <VulnerabilityDetails 
            vulnerability={vulnerabilityData.find(vuln => vuln.id === activeVulnerability)}
          />
        );
      default:
        return <Dashboard scanData={scanData} onScanSelect={handleScanSelect} />;
    }
  };

  return (
    <div className="app">
      <Header />
      <div className="main-container">
        <Sidebar activeView={activeView} onNavigate={handleNavigation} />
        <main className="content">
          {renderView()}
        </main>
      </div>
    </div>
  );
}

export default App;