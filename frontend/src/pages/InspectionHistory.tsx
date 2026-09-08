import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getInspections } from '../services/api';

const InspectionHistory: React.FC = () => {
  const [filterStatus, setFilterStatus] = useState('All');
  const [history, setHistory] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const fetchHistory = () => {
    setIsLoading(true);
    setError(null);
    getInspections()
      .then(data => {
        // Handle various possible backend response formats
        const records = Array.isArray(data) ? data : (data?.items || data?.inspections || []);
        setHistory(records);
      })
      .catch(err => {
        console.error("Failed to load inspection history:", err);
        setError("Unable to load inspection history.");
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const getUIStatus = (status?: string | null) => {
    if (!status) return 'UNKNOWN';
    switch (status.toUpperCase()) {
      case 'PASS': return 'READY TO DISPATCH';
      case 'FAIL': return 'DO NOT DISPATCH';
      case 'MANUAL_REVIEW': 
      case 'REVIEW': return 'HUMAN REVIEW REQUIRED';
      default: return status.toUpperCase();
    }
  };

  // The backend uses 'decision', so we safely extract and map it
  const safeHistory = Array.isArray(history) ? history : [];
  const filteredHistory = filterStatus === 'All' 
    ? safeHistory 
    : safeHistory.filter(h => getUIStatus(h.decision) === filterStatus);

  if (isLoading) {
    return (
      <div className="p-6 bg-gray-50 min-h-screen flex items-center justify-center">
        <div className="text-gray-500 font-medium">Loading inspection history...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-gray-50 min-h-screen flex flex-col items-center justify-center">
        <div className="bg-red-50 text-red-700 p-4 rounded-lg mb-4 shadow">
          {error}
        </div>
        <button 
          onClick={fetchHistory}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Inspection History</h1>
        <p className="text-gray-600">Review previous packing quality verification inspections.</p>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-4 border-b flex justify-between items-center bg-gray-50">
          <input type="text" placeholder="Search ID or Part..." className="px-3 py-2 border rounded w-64 shadow-sm" />
          <select 
            value={filterStatus} 
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-3 py-2 border rounded shadow-sm bg-white"
          >
            <option value="All">All Statuses</option>
            <option value="READY TO DISPATCH">Ready to Dispatch</option>
            <option value="DO NOT DISPATCH">Do Not Dispatch</option>
            <option value="HUMAN REVIEW REQUIRED">Human Review Required</option>
          </select>
        </div>

        {safeHistory.length === 0 ? (
          <div className="p-12 text-center flex flex-col items-center">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">No inspection records yet.</h3>
            <p className="text-gray-500 mb-6">Complete a packing verification to create the first inspection record.</p>
            <button 
              onClick={() => navigate('/verify')}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium"
            >
              Start Verification
            </button>
          </div>
        ) : (
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Part</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Confidence</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredHistory.map((row) => {
                const uiStatus = getUIStatus(row.decision);
                return (
                  <tr key={row.id || Math.random()} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">
                      INSP-{row.id ?? "—"}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {row.timestamp ? new Date(row.timestamp).toLocaleString() : "—"}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {row.part_id ?? "—"}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-3 py-1 inline-flex text-xs leading-5 font-bold rounded-full border ${uiStatus === 'READY TO DISPATCH' ? 'bg-green-50 text-green-800 border-green-200' : uiStatus === 'DO NOT DISPATCH' ? 'bg-red-50 text-red-800 border-red-200' : 'bg-amber-50 text-amber-800 border-amber-200'}`}>
                        {uiStatus}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-medium">
                      {row.confidence != null ? `${(row.confidence * 100).toFixed(1)}%` : "—"}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button 
                        onClick={() => navigate(`/history/${row.id}`)}
                        className="text-blue-600 hover:text-blue-900 font-semibold"
                        disabled={!row.id}
                      >
                        View
                      </button>
                    </td>
                  </tr>
                );
              })}
              {filteredHistory.length === 0 && safeHistory.length > 0 && (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                    No inspections match the selected filter.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default InspectionHistory;
