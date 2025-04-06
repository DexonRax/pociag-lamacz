import React from 'react';

const Dashboard = ({ scanData, onScanSelect }) => {
  const completedScans = scanData.filter(scan => scan.status === 'Complete').length;
  const inProgressScans = scanData.filter(scan => scan.status === 'In Progress').length;
  const totalVulnerabilities = scanData.reduce((sum, scan) => sum + (scan.vulnerabilities || 0), 0);

  const getSeverityClass = (severity) => {
    switch (severity) {
      case 'critical': return 'severity-critical';
      case 'high': return 'severity-high';
      case 'medium': return 'severity-medium';
      case 'low': return 'severity-low';
      default: return 'severity-none';
    }
  };

  if (scanData.length === 0) {
    return (
      <div className="dashboard empty-dashboard">
        <h2>Panel zabezpieczeń</h2>
        <div className="empty-state">
          <p>Brak skanów. Kliknij "Nowy skan".</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <h2>Panel zabezpieczeń</h2>

      <div className="stat-cards">
        <div className="stat-card">
          <h3>Wszystkie skany</h3>
          <div className="stat-value">{scanData.length}</div>
        </div>
        <div className="stat-card">
          <h3>Ukończone</h3>
          <div className="stat-value">{completedScans}</div>
        </div>
        <div className="stat-card">
          <h3>W trakcie</h3>
          <div className="stat-value">{inProgressScans}</div>
        </div>
        <div className="stat-card">
          <h3>Podatności</h3>
          <div className="stat-value">{totalVulnerabilities}</div>
        </div>
      </div>

      <div className="section">
        <h3>Wszystkie skany</h3>
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Nazwa</th>
                <th>Data</th>
                <th>Status</th>
                <th>Podatności</th>
                <th>Powaga</th>
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
                  <td>{scan.vulnerabilities || 0}</td>
                  <td>
                    <span className={`severity-badge ${getSeverityClass(scan.severity)}`}>
                      {scan.severity || 'None'}
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