import React from 'react';

const ScanResults = ({ scanData, vulnerabilities, onVulnerabilitySelect }) => {
  if (!scanData) return <div>No scan selected</div>;

  const getSeverityClass = (severity) => {
    switch (severity) {
      case 'critical': return 'severity-critical';
      case 'high': return 'severity-high';
      case 'medium': return 'severity-medium';
      case 'low': return 'severity-low';
      default: return 'severity-none';
    }
  };

  const getStatusClass = (status) => {
    return `status-${status.toLowerCase().replace(' ', '-')}`;
  };

  return (
    <div className="scan-results">
      <div className="scan-header">
        <h2>{scanData.name}</h2>
        <div className="scan-meta">
          <span className={`status-badge ${getStatusClass(scanData.status)}`}>{scanData.status}</span>
          <span className="scan-date">{scanData.date}</span>
        </div>
      </div>
      <span className="scan-date"><b>Komenda: </b>{scanData.data?.find(x => x.cmd)?.cmd}</span>
      <div className="section">
        <h3>Vulnerabilities</h3>
        {vulnerabilities.length === 0 ? (
          <div className="empty-state">
            <p>No vulnerabilities detected in this scan.</p>
          </div>
        ) : (
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Severity</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {vulnerabilities.map(vuln => (
                  <tr key={vuln.id} onClick={() => onVulnerabilitySelect(vuln.id)}>
                    <td>{vuln.name}</td>
                    <td>
                      <span className={`severity-badge ${getSeverityClass(vuln.severity)}`}>
                        {vuln.severity || 'None'}
                      </span>
                    </td>
                    <td>
                      <span className={`status-badge ${getStatusClass(vuln.status)}`}>
                        {vuln.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="section">
        <h3>Active Hosts</h3>
        {scanData.data && scanData.data.length > 0 ? (
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>IP Address</th>
                  <th>MAC Address</th>
                  <th>Host Name</th>
                </tr>
              </thead>
              <tbody>
                {scanData.data
                .filter(x => x.ip)
                .map((data, index) => (
                  <tr key={index}>
                    <td>{data.ip}</td>
                    <td>{data.mac}</td>
                    <td>{data.name}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <p>No active hosts found in this scan.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ScanResults;