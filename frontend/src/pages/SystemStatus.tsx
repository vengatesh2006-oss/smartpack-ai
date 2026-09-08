import React, { useState } from 'react';

const SystemStatus: React.FC = () => {
  const [cameraOnline, setCameraOnline] = useState(true);
  const [dbOnline, setDbOnline] = useState(true);

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">System Status</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow flex flex-col items-center">
          <div className={`w-4 h-4 rounded-full mb-2 ${cameraOnline ? 'bg-green-500' : 'bg-red-500'}`}></div>
          <h2 className="text-lg font-semibold">Camera Subsystem</h2>
          <p className="text-sm text-gray-500 mt-1">{cameraOnline ? 'Operational' : 'Offline'}</p>
          <button 
            onClick={() => setCameraOnline(!cameraOnline)}
            className="mt-4 text-sm text-blue-600 underline"
          >
            Toggle State (Simulate)
          </button>
        </div>

        <div className="bg-white p-6 rounded-lg shadow flex flex-col items-center">
          <div className={`w-4 h-4 rounded-full mb-2 ${dbOnline ? 'bg-green-500' : 'bg-red-500'}`}></div>
          <h2 className="text-lg font-semibold">Database</h2>
          <p className="text-sm text-gray-500 mt-1">{dbOnline ? 'Operational' : 'Connection Error'}</p>
          <button 
            onClick={() => setDbOnline(!dbOnline)}
            className="mt-4 text-sm text-blue-600 underline"
          >
            Toggle State (Simulate)
          </button>
        </div>

        <div className="bg-white p-6 rounded-lg shadow flex flex-col items-center">
          <div className="w-4 h-4 rounded-full mb-2 bg-green-500"></div>
          <h2 className="text-lg font-semibold">Inference Engine</h2>
          <p className="text-sm text-gray-500 mt-1">Operational (Latency: 45ms)</p>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">System Logs</h2>
        <div className="bg-gray-900 text-green-400 p-4 rounded h-64 overflow-y-auto font-mono text-sm">
          <p>[10:05:22] INFERENCE: Processed image id=1902 in 42ms</p>
          <p>[10:05:25] DB: Saved record INSP-1005</p>
          {!cameraOnline && <p className="text-red-400">[10:06:01] ERROR: Camera CAM-04 connection lost</p>}
          {!dbOnline && <p className="text-red-400">[10:06:15] ERROR: Database timeout</p>}
          <p>[10:06:30] HEARTBEAT: System OK</p>
        </div>
      </div>
    </div>
  );
};

export default SystemStatus;
