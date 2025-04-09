import React, { useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';
import { Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import ScanResults from './components/ScanResults';
import Header from './components/Header';
import ScanForm from './components/ScanForm';
import Help from './components/Help';
import axios from 'axios';

function App() {
  const [activeView, setActiveView] = useState('dashboard');
  const [activeScan, setActiveScan] = useState(null);
  const [scanData, setScanData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleNavigation = (view) => {
    setActiveView(view);
    setActiveScan(null);
  };

  const handleScanSelect = (scanId) => {
    setActiveScan(scanId);
    setActiveView('scanResults');
  };

  const handleNewScan = async (scanInput) => {
    toast.success("Scan executing...");
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:5000/scan-active-hosts', scanInput);
      const newScan = {
        id: Date.now(),
        name: `Scan ${scanData.length + 1}`,
        status: 'Complete',
        date: new Date().toISOString().split('T')[0],
        hosts: response.data.hosts || [],
      };
      setScanData([...scanData, newScan]);
      setActiveScan(newScan.id);
      setActiveView('scanResults');
    } catch (err) {
      const message = err.response?.data?.error || 'Failed to start scan';
      toast.error(message);
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  const renderMainView = () => {
    switch (activeView) {
      case 'dashboard':
        return <Dashboard scanData={scanData} onScanSelect={handleScanSelect} />;
      case 'scanResults':
        const selectedScan = scanData.find((scan) => scan.id === activeScan);
        return (
          <ScanResults
            scanData={selectedScan || { name: 'No Scan Selected', hosts: [] }}
            vulnerabilities={[]}
          />
        );
      default:
        return <Dashboard scanData={scanData} onScanSelect={handleScanSelect} />;
    }
  };

  return (
    <div className="app">
      <ToastContainer position="top-right" autoClose={3000} hideProgressBar />
      <Header />
      <div className="main-container">
        <Sidebar activeView={activeView} onNavigate={handleNavigation} />
        <main className="content">
          <Routes>
            <Route path="/" element={renderMainView()} />
            <Route path="/scan-form" element={<ScanForm onScanSubmit={handleNewScan} />} />
            <Route path="/help" element={<Help />} /> {}
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default App;