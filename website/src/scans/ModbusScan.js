import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaEye, FaEyeSlash } from 'react-icons/fa';

const ModbusScan = ({ onScanSubmit }) => {
  const [target, setTarget] = useState('192.168.1');
  const [flags, setFlags] = useState('-T3 -sS');
  const [sudoPassword, setSudoPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const scanInput = {
      target,
      flags, 
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
          <label>Targets</label>
          <input 
            type="text" 
            value={target} 
            onChange={(e) => setTarget(e.target.value)}
            placeholder="e.g. 192.168.1.0"
          />
        </div>
        <div className="form-group">
          <label>Flags</label>
          <input 
            type="text" 
            value={flags} 
            onChange={(e) => setFlags(e.flags.value)}
            placeholder="e.g. -T3 -sS"
          />
        </div>
        <div className="form-group">
          <label>Sudo Password (required for nmap)</label>
          <div className="password-input">
        <input
          type={showPassword ? 'text' : 'password'}
          value={sudoPassword}
          onChange={(e) => setSudoPassword(e.target.value)}
          placeholder="Enter your sudo password"
        />
        <button
          type="button"
          className="toggle-password"
          onClick={() => setShowPassword(!showPassword)}
          aria-label={showPassword ? 'Hide password' : 'Show password'}
        >
          {showPassword ? <FaEye /> : <FaEyeSlash /> }
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
  
  export default ModbusScan;