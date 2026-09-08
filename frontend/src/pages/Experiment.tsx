import React, { useState } from 'react';
import api from '../services/api';

const Experiment: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleRun = async () => {
    setIsRunning(true);
    try {
      const res = await api.post('/experiment/run');
      setResults(res.data);
    } catch (err) {
      console.error(err);
      alert('Experiment run failed.');
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Experiment Mode</h1>
      <p className="text-gray-600 mb-6">Evaluate the current verification system against the full dataset to compute metrics like Accuracy, Precision, and Recall.</p>

      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-700">Model Evaluation</h2>
          <button 
            onClick={handleRun}
            disabled={isRunning}
            className={`px-6 py-2 rounded text-white font-medium ${isRunning ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
          >
            {isRunning ? 'Running Eval on Dataset...' : 'Run Experiment on Dataset'}
          </button>
        </div>

        {results && (
          <>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <div className="border p-4 rounded text-center">
                <h3 className="text-sm font-medium text-gray-500 uppercase">Accuracy</h3>
                <p className="text-2xl font-bold text-gray-900 mt-1">{(results.metrics.accuracy * 100).toFixed(2)}%</p>
              </div>
              <div className="border p-4 rounded text-center">
                <h3 className="text-sm font-medium text-gray-500 uppercase">Precision</h3>
                <p className="text-2xl font-bold text-gray-900 mt-1">{(results.metrics.precision * 100).toFixed(2)}%</p>
              </div>
              <div className="border p-4 rounded text-center">
                <h3 className="text-sm font-medium text-gray-500 uppercase">Recall</h3>
                <p className="text-2xl font-bold text-gray-900 mt-1">{(results.metrics.recall * 100).toFixed(2)}%</p>
              </div>
              <div className="border p-4 rounded text-center">
                <h3 className="text-sm font-medium text-gray-500 uppercase">F1 Score</h3>
                <p className="text-2xl font-bold text-gray-900 mt-1">{(results.metrics.f1 * 100).toFixed(2)}%</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                    <h3 className="font-semibold text-gray-700 mb-4 text-center">Confusion Matrix (Dataset)</h3>
                    <div className="max-w-md mx-auto">
                    <div className="grid grid-cols-3 gap-1 text-center text-sm">
                        <div className="p-2"></div>
                        <div className="p-2 font-medium">Pred: Pass</div>
                        <div className="p-2 font-medium">Pred: Fail</div>
                        
                        <div className="p-2 font-medium flex items-center justify-end">True: Pass</div>
                        <div className="p-4 bg-green-200 font-bold border border-white">{results.metrics.TN}</div>
                        <div className="p-4 bg-red-100 font-bold border border-white">{results.metrics.FP} (FP)</div>
                        
                        <div className="p-2 font-medium flex items-center justify-end">True: Fail</div>
                        <div className="p-4 bg-red-200 font-bold border border-white">{results.metrics.FN} (FN)</div>
                        <div className="p-4 bg-green-100 font-bold border border-white">{results.metrics.TP}</div>
                    </div>
                    </div>
                </div>
                <div>
                    <h3 className="font-semibold text-gray-700 mb-4">Additional Metrics</h3>
                    <ul className="space-y-4">
                        <li className="flex justify-between items-center border-b pb-2">
                            <span className="text-gray-600">Total Dataset Size</span>
                            <span className="font-bold">{results.dataset_size} cases</span>
                        </li>
                        <li className="flex justify-between items-center border-b pb-2">
                            <span className="text-gray-600">Pre-dispatch Detection Rate (PDDR)</span>
                            <span className="font-bold text-blue-600">{(results.metrics.pddr * 100).toFixed(2)}%</span>
                        </li>
                        <li className="flex justify-between items-center border-b pb-2">
                            <span className="text-gray-600">Manual Review Rate</span>
                            <span className="font-bold text-amber-600">{(results.metrics.manual_review_rate * 100).toFixed(2)}%</span>
                        </li>
                    </ul>
                </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Experiment;
