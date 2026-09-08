import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { verifyPacking } from '../services/api';

const VerifyPacking: React.FC = () => {
  const [partId, setPartId] = useState('');
  const [shipmentId, setShipmentId] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [loadingText, setLoadingText] = useState('');
  const navigate = useNavigate();

  const loadingSequence = [
    "Analyzing packing image...",
    "Checking packaging requirements...",
    "Evaluating quality...",
    "Generating decision..."
  ];

  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    if (isUploading) {
      let step = 0;
      setLoadingText(loadingSequence[0]);
      interval = setInterval(() => {
        step += 1;
        if (step < loadingSequence.length) {
          setLoadingText(loadingSequence[step]);
        }
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isUploading]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !partId || !shipmentId) return;
    
    setIsUploading(true);
    try {
      const response = await verifyPacking(partId, file);
      // Wait a bit to show the full sequence for demo purposes if it was too fast
      setTimeout(() => {
        navigate(`/result/${response.id || response.inspection_id || 'result'}`, { state: { result: response } });
      }, 500);
    } catch (err) {
      console.error(err);
      alert('Verification failed. See console.');
      setIsUploading(false);
    }
  };

  return (
    <div className="p-6 bg-[#f4f4f5] min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-[#1c1c1e]">Start Inspection</h1>
      <div className="max-w-2xl bg-white rounded-lg shadow-md border border-gray-200 p-8">
        <form onSubmit={handleUpload}>
          <div className="mb-6 bg-gray-50 p-4 rounded border border-gray-200">
            <h2 className="text-lg font-semibold text-gray-700 mb-4">Step 1: Select Part & Shipment</h2>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">Part Category</label>
              <select
                value={partId}
                onChange={(e) => setPartId(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[#0a84ff]"
                required
              >
                <option value="">Select a part...</option>
                <option value="1">BRK-1025 Brake Pad</option>
                <option value="2">ENG-2040 Engine Valve</option>
              </select>
            </div>
            
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2">Shipment ID (Scan Barcode)</label>
              <input
                type="text"
                value={shipmentId}
                onChange={(e) => setShipmentId(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[#0a84ff]"
                placeholder="e.g. SHP-2023-001"
                required
              />
            </div>
          </div>

          <div className="mb-6 bg-gray-50 p-4 rounded border border-gray-200">
            <h2 className="text-lg font-semibold text-gray-700 mb-4">Step 2: Capture / Upload Image</h2>
            <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md bg-white hover:bg-gray-50 transition-colors">
              <div className="space-y-1 text-center">
                <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                <div className="flex text-sm text-gray-600 justify-center">
                  <label className="relative cursor-pointer rounded-md font-medium text-[#0a84ff] hover:text-blue-700 focus-within:outline-none">
                    <span>Click to browse</span>
                    <input type="file" className="sr-only" onChange={handleFileChange} accept="image/*" required />
                  </label>
                </div>
                <p className="text-xs text-gray-500">PNG, JPG up to 10MB</p>
                {file && <p className="text-sm text-green-600 mt-2 font-medium">Selected: {file.name}</p>}
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={isUploading}
            className={`w-full text-white font-bold py-3 px-4 rounded shadow-sm text-lg flex items-center justify-center space-x-2 ${isUploading ? 'bg-[#5ac8fa]' : 'bg-[#0a84ff] hover:bg-[#007aff]'}`}
          >
            {isUploading && (
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            )}
            <span>{isUploading ? loadingText : 'Run Quality Check'}</span>
          </button>
        </form>
      </div>
    </div>
  );
};

export default VerifyPacking;
