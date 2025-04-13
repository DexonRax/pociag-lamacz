import { useNavigate } from 'react-router-dom';
import { FaNetworkWired, FaSearch, FaMicrochip } from 'react-icons/fa';
import '../ScanMenu.css'; // 👈 Upewnij się, że importujesz CSS

const ScanMenu = () => {
  const navigate = useNavigate();

  return (
    <div className="scan-menu-container">
      <h1 className="scan-title">Wybierz typ skanowania</h1>
      <div className="scan-grid">
        <div onClick={() => navigate(`/scans/hosts-scan`)} className="scan-box">
          <div className="scan-icon">
            <FaNetworkWired size={40} />
          </div>
          <h2 className="scan-heading">Odkrycie hostów</h2>
          <p className="scan-description">Skan do wykrycia aktywnych hostów.</p>
        </div>

        <div onClick={() => navigate(`/scans/basic-scan`)} className="scan-box">
          <div className="scan-icon">
            <FaSearch size={40} />
          </div>
          <h2 className="scan-heading">Podstawowy skan sieci</h2>
          <p className="scan-description">Pełny skan portów i usług.</p>
        </div>

        <div onClick={() => navigate(`/scans/modbus-scan`)} className="scan-box">
          <div className="scan-icon">
            <FaMicrochip size={40} />
          </div>
          <h2 className="scan-heading">Skan Modbus</h2>
          <p className="scan-description">Skan przemysłowego portu Modbus TCP.</p>
        </div>
      </div>
    </div>
  );
};

export default ScanMenu;
