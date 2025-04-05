import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ScanForm = ({ onScanSubmit }) => {
  const [subnet, setSubnet] = useState('192.168.1');
  const [rangeStart, setRangeStart] = useState('1');
  const [rangeEnd, setRangeEnd] = useState('254');
  const [sudoPassword, setSudoPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const scanInput = {
      subnet,
      range_start: rangeStart,
      range_end: rangeEnd,
      sudo_password: sudoPassword
    };
    onScanSubmit(scanInput);
    navigate('/');
  };

  return (
    <div className="scan-form">
      <h2>New Network Scan</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Subnet</label>
          <input 
            type="text" 
            value={subnet} 
            onChange={(e) => setSubnet(e.target.value)}
            placeholder="e.g. 192.168.1"
          />
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Range Start</label>
            <input 
              type="text" 
              value={rangeStart} 
              onChange={(e) => setRangeStart(e.target.value)}
              placeholder="e.g. 1"
            />
          </div>
          <div className="form-group">
            <label>Range End</label>
            <input 
              type="text" 
              value={rangeEnd} 
              onChange={(e) => setRangeEnd(e.target.value)}
              placeholder="e.g. 254"
            />
          </div>
        </div>
        <div className="form-group">
          <label>Sudo Password (required for nmap)</label>
          <div className="password-input">
            <input
              type={showPassword ? "text" : "password"}
              value={sudoPassword}
              onChange={(e) => setSudoPassword(e.target.value)}
              placeholder="Enter your sudo password"
            />
            <button 
              type="button" 
              className="toggle-password"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>
          <small className="form-text">
            Your password is only used locally to execute scan commands and is never stored.
          </small>
        </div>
        <button type="submit" className="btn btn-primary">Start Scan</button>
      </form>
    </div>
  );
};

export default ScanForm;