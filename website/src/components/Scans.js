import { useNavigate } from 'react-router-dom';

const ScanMenu = () => {
  const navigate = useNavigate();

  const handleNavigate = (scanType) => {
    navigate(`/scans/${scanType}`);
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Wybierz typ skanu</h1>
      <div className="space-y-2">
        <button onClick={() => handleNavigate('hosts-scan')} className="bg-blue-500 text-white px-4 py-2 rounded w-full">
          Odkrycie hostów
        </button>
        <button onClick={() => handleNavigate('basic-scan')} className="bg-blue-500 text-white px-4 py-2 rounded w-full">
          Podstawowy skan sieci
        </button>
        <button onClick={() => handleNavigate('modbus-scan')} className="bg-blue-500 text-white px-4 py-2 rounded w-full">
          Skan portu modbus
        </button>
      </div>
    </div>
  );
};

export default ScanMenu;
