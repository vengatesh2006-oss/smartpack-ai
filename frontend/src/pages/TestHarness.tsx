import React, { useState } from 'react';
import api from '../services/api';

const TestHarness: React.FC = () => {
  const [running, setRunning] = useState(false);
  
  const [results, setResults] = useState<any[]>([]);

  const runAllTests = async () => {
    setRunning(true);
    try {
      const response = await api.get('/experiment/test-harness');
      setResults(response.data);
    } catch (err) {
      console.error(err);
      alert('Failed to run test harness.');
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Test Harness</h1>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex justify-between items-center mb-6">
          <p className="text-gray-600">Run automated edge case scenarios to validate system robustness.</p>
          <button 
            onClick={runAllTests}
            disabled={running}
            className={`px-4 py-2 rounded font-medium text-white transition-colors ${running ? 'bg-purple-400 cursor-not-allowed' : 'bg-purple-600 hover:bg-purple-700'}`}
          >
            {running ? 'Executing Real Scenarios...' : 'Run All Tests'}
          </button>
        </div>

        {results.length > 0 ? (
          <div className="grid grid-cols-1 gap-4">
            <div className="border p-4 rounded flex items-center justify-between bg-gray-100 font-bold">
               <div className="w-1/2">Scenario / ID</div>
               <div className="w-1/4 text-center">Expected</div>
               <div className="w-1/4 text-center">Actual</div>
               <div className="w-16 text-center">Status</div>
            </div>
            {results.map((tc, idx) => (
              <div key={idx} className="border p-4 rounded flex items-center justify-between hover:bg-gray-50">
                <div className="w-1/2">
                  <div className="font-bold text-gray-700">{tc.id}</div>
                  <div className="text-gray-600 text-sm">{tc.description}</div>
                </div>
                <div className="w-1/4 text-center font-medium text-gray-700">{tc.expected}</div>
                <div className="w-1/4 text-center font-medium text-gray-700">{tc.actual}</div>
                <div className="w-16 text-center">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${tc.status === 'PASS' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {tc.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-10 text-gray-500 border border-dashed rounded bg-gray-50">
            Click "Run All Tests" to execute the test harness suite.
          </div>
        )}
      </div>
    </div>
  );
};

export default TestHarness;
