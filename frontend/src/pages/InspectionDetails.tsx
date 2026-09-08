import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getInspection } from '../services/api';

const InspectionDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [inspection, setInspection] = useState<any>(null);

  useEffect(() => {
    if (id) {
      getInspection(id).then(setInspection).catch(console.error);
    }
  }, [id]);

  if (!inspection) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <button 
        onClick={() => navigate(-1)}
        className="mb-4 text-blue-600 hover:underline flex items-center"
      >
        ← Back to History
      </button>
      
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Inspection Details: {id || 'INSP-XXXX'}</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Capture Image</h2>
          <div className="bg-gray-200 h-80 rounded flex items-center justify-center">
            <span className="text-gray-500">High-res Image View</span>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow space-y-6">
          <div>
            <h2 className="text-xl font-semibold mb-2 text-gray-700">Metadata</h2>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div><span className="font-medium text-gray-600">Timestamp:</span> {new Date(inspection.timestamp).toLocaleString()}</div>
              <div><span className="font-medium text-gray-600">Part ID:</span> {inspection.part_id}</div>
              <div><span className="font-medium text-gray-600">Operator ID:</span> {inspection.operator_id || 'Auto'}</div>
              <div><span className="font-medium text-gray-600">Shipment ID:</span> {inspection.shipment_id || 'N/A'}</div>
            </div>
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-2 text-gray-700">AI Analysis</h2>
            <div className="mb-2">
              <span className="font-medium text-gray-600">Overall Status:</span> 
              <span className={`ml-2 px-2 py-1 rounded font-bold text-sm ${inspection.status === 'PASS' ? 'bg-green-100 text-green-800' : inspection.status === 'FAIL' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>{inspection.status}</span>
            </div>
            <div className="mb-2 mt-4">
              <span className="font-medium text-gray-600">Confidence:</span> 
              <span className="ml-2 text-blue-600 font-bold">{(inspection.confidence * 100).toFixed(1)}%</span>
            </div>
            
            {inspection.manual_review_required && (
                <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded">
                    <p className="font-bold text-yellow-800">Manual Review Required</p>
                    {inspection.manual_decision && (
                        <p className="text-sm mt-1">Decision: <strong>{inspection.manual_decision}</strong> ({inspection.manual_reason})</p>
                    )}
                </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default InspectionDetails;
