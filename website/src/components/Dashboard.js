import React from 'react';

const Dashboard = ({ scanData, onScanSelect }) => {
  // Calculate summary stats
  const completedScans = scanData.filter(scan => scan.status === 'Complete').length;
  const inProgressScans = scanData.filter(scan => scan.status === 'In Progress').length;
  const totalVulnerabilities = scanData.reduce((sum, scan) => sum + scan.vulnerabilities, 0);
  
  const getSeverityClass = (severity) => {
    switch(severity) {
      case 'critical': return 'severity-critical';
      case 'high': return 'severity-high';
      case 'medium': return 'severity-medium';
      case 'low': return 'severity-low';
      default: return 'severity-none';
    }
  };

  return (
    <div className="dashboard">
      <h2>Security Dashboard</h2>
      
      <div className="stat-cards">
        <div className="stat-card">
          <h3>Total Scans</h3>
          <div className="stat-value">{scanData.length}</div>
        </div>
        <div className="stat-card">
          <h3>Completed</h3>
          <div className="stat-value">{completedScans}</div>
        </div>
        <div className="stat-card">
          <h3>In Progress</h3>
          <div className="stat-value">{inProgressScans}</div>
        </div>
        <div className="stat-card">
          <h3>Vulnerabilities</h3>
          <div className="stat-value">{totalVulnerabilities}</div>
        </div>
      </div>

      <div className="section">
        <h3>Recent Scans</h3>
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Date</th>
                <th>Status</th>
                <th>Vulnerabilities</th>
                <th>Severity</th>
              </tr>
            </thead>
            <tbody>
              {scanData.map(scan => (
                <tr key={scan.id} onClick={() => onScanSelect(scan.id)}>
                  <td>{scan.name}</td>
                  <td>{scan.date}</td>
                  <td>
                    <span className={`status-badge status-${scan.status.toLowerCase().replace(' ', '-')}`}>
                      {scan.status}
                    </span>
                  </td>
                  <td>{scan.vulnerabilities}</td>
                  <td>
                    <span className={`severity-badge ${getSeverityClass(scan.severity)}`}>
                      {scan.severity}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
