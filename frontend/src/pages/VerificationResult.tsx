import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const VerificationResult: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const result = location.state?.result;
  const rawStatus = result?.status || 'UNKNOWN';

  const getUIStatus = (status: string) => {
    switch (status.toUpperCase()) {
      case 'PASS': return 'READY TO DISPATCH';
      case 'FAIL': return 'DO NOT DISPATCH';
      case 'MANUAL_REVIEW': 
      case 'REVIEW': return 'HUMAN REVIEW REQUIRED';
      default: return status.toUpperCase();
    }
  };

  const uiStatus = getUIStatus(rawStatus);

  const getBannerColor = (status: string) => {
    switch (status) {
      case 'READY TO DISPATCH': return 'bg-green-100 border-green-500 text-green-800';
      case 'DO NOT DISPATCH': return 'bg-red-100 border-red-500 text-red-800';
      case 'HUMAN REVIEW REQUIRED': return 'bg-amber-100 border-amber-500 text-amber-800';
      default: return 'bg-gray-100 border-gray-500 text-gray-800';
    }
  };

  return (
    <div className="p-6 bg-[#f4f4f5] min-h-screen">
      <div className={`mb-6 p-4 border-l-4 rounded shadow-sm flex items-center ${getBannerColor(uiStatus)}`}>
        <div className="flex-1">
          <h1 className="text-2xl font-bold uppercase tracking-wider">{uiStatus}</h1>
          <p className="text-sm mt-1">
            {uiStatus === 'READY TO DISPATCH' && 'The package meets all quality standards.'}
            {uiStatus === 'DO NOT DISPATCH' && 'The package failed the quality check. Please rectify issues.'}
            {uiStatus === 'HUMAN REVIEW REQUIRED' && 'Manual review required by a supervisor.'}
          </p>
        </div>
      </div>
      
      <div className="max-w-5xl grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <h2 className="text-xl font-semibold mb-4 text-[#1c1c1e]">Captured Image</h2>
          <div className="bg-gray-200 h-64 rounded flex items-center justify-center relative overflow-hidden">
            {result?.image_url ? (
              <img src={result.image_url} alt="Captured package" className="object-cover w-full h-full" />
            ) : (
              <span className="text-gray-500">Image Output</span>
            )}
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200 overflow-y-auto" style={{ maxHeight: 'calc(100vh - 200px)' }}>
          <h2 className="text-xl font-semibold mb-4 text-[#1c1c1e]">Quality Check Results</h2>
          <div className="mb-6 grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded border border-gray-100">
            <div>
              <p className="text-gray-500 text-sm font-medium">Quality Decision</p>
              <p className={`font-bold text-lg ${uiStatus === 'READY TO DISPATCH' ? 'text-green-600' : uiStatus === 'DO NOT DISPATCH' ? 'text-red-600' : 'text-amber-600'}`}>
                {uiStatus}
              </p>
            </div>
            <div>
              <p className="text-gray-500 text-sm font-medium">Confidence Score</p>
              <p className="font-bold text-[#0a84ff] text-lg">
                {result?.confidence ? `${(result.confidence * 100).toFixed(1)}%` : 'N/A'}
              </p>
            </div>
            <div className="col-span-2">
              <p className="text-gray-500 text-sm font-medium">Inspection ID</p>
              <p className="text-gray-900 font-medium">{result?.id || result?.inspection_id || 'N/A'}</p>
            </div>
          </div>

          <h3 className="font-semibold text-gray-700 mb-3 border-b pb-2">Explainable Checklist</h3>
          <ul className="space-y-4 mb-8">
            {result?.rules?.map((rule: any, i: number) => (
              <li key={i} className="bg-gray-50 p-4 rounded border border-gray-200">
                <div className="flex items-start mb-2">
                  <div className={`mt-0.5 rounded-full p-1 mr-3 ${rule.passed ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}`}>
                    {rule.passed ? (
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" /></svg>
                    ) : (
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" /></svg>
                    )}
                  </div>
                  <div>
                    <p className="text-gray-900 font-bold">{rule.rule_name || rule.name}</p>
                    <p className="text-sm font-medium text-gray-500">Severity: <span className={rule.severity === 'HIGH' ? 'text-red-500' : rule.severity === 'MEDIUM' ? 'text-amber-500' : 'text-gray-500'}>{rule.severity || 'N/A'}</span></p>
                  </div>
                </div>
                <div className="pl-9 space-y-1 text-sm">
                  <p><span className="font-semibold text-gray-700">Expected:</span> {rule.expected}</p>
                  <p><span className="font-semibold text-gray-700">Observed:</span> {rule.observed}</p>
                  {rule.explanation && <p><span className="font-semibold text-gray-700">Explanation:</span> {rule.explanation}</p>}
                  {rule.recommended_action && <p><span className="font-semibold text-[#0a84ff]">Recommended Action:</span> {rule.recommended_action}</p>}
                </div>
              </li>
            ))}
            {(!result?.rules || result.rules.length === 0) && (
              <p className="text-gray-500 italic">No checklist details available.</p>
            )}
          </ul>

          <div className="flex space-x-4">
            {uiStatus === 'HUMAN REVIEW REQUIRED' ? (
              <button
                onClick={() => {
                  alert('Inspection flagged and sent to Manager Queue for Manual Review.');
                  navigate('/');
                }}
                className="flex-1 py-3 bg-amber-500 text-white rounded font-bold hover:bg-amber-600 shadow-sm transition-colors"
              >
                Submit to Manager Queue
              </button>
            ) : (
              <button
                onClick={() => navigate('/verify')}
                className="flex-1 py-3 bg-[#0a84ff] text-white rounded font-bold hover:bg-[#007aff] shadow-sm transition-colors"
              >
                Start Next Inspection
              </button>
            )}
            <button
              onClick={() => navigate('/')}
              className="px-6 py-3 border border-gray-300 text-gray-700 rounded hover:bg-gray-50 font-bold transition-colors"
            >
              Dashboard
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VerificationResult;
