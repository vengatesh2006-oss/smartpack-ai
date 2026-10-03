import React, { useState, useEffect } from 'react';
import { getInspections, submitManualDecision } from '../services/api';

const ManualReview: React.FC = () => {
  const [reviews, setReviews] = useState<any[]>([]);
  const [selectedReview, setSelectedReview] = useState<any>(null);
  const [overrideReason, setOverrideReason] = useState('');
  const [hasReviewed, setHasReviewed] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    try {
      const all = await getInspections();
      const pending = all.filter((i: any) => i.decision === 'MANUAL_REVIEW' || i.decision === 'REVIEW');
      setReviews(pending);
      if (pending.length > 0 && !selectedReview) {
        setSelectedReview(pending[0]);
      } else if (pending.length === 0) {
        setSelectedReview(null);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleAction = async (action: 'PASS' | 'FAIL') => {
    if (!overrideReason.trim()) {
      alert('Please provide a reason for this decision.');
      return;
    }
    setIsSubmitting(true);
    try {
      await submitManualDecision(selectedReview.id, action, overrideReason);
      setOverrideReason('');
      fetchReviews();
      alert(`Decision recorded in audit log: ${action === 'PASS' ? 'READY TO DISPATCH' : 'DO NOT DISPATCH'}`);
    } catch (e) {
      console.error(e);
      alert('Failed to submit decision.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="p-6 bg-[#f4f4f5] min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-[#1c1c1e]">Human Review Required</h1>
      
      <div className="flex flex-col md:flex-row gap-6">
        <div className="w-full md:w-1/3 bg-white rounded-lg shadow-md border border-gray-200 p-4">
          <h2 className="text-xl font-semibold mb-4 text-[#1c1c1e]">Pending Reviews</h2>
          {reviews.length === 0 && <p className="text-gray-500 text-sm">No pending reviews.</p>}
          <ul className="space-y-2">
            {reviews.map((review) => (
              <li 
                key={review.id}
                onClick={() => setSelectedReview(review)}
                className={`p-3 border rounded cursor-pointer transition ${selectedReview?.id === review.id ? 'bg-[#e6f2ff] border-[#0a84ff]' : 'hover:bg-gray-50'}`}
              >
                <div className="flex justify-between items-center mb-1">
                  <span className="font-bold text-gray-800">INSP-{review.id}</span>
                  <span className="text-xs text-gray-500">{new Date(review.timestamp).toLocaleTimeString()}</span>
                </div>
                <div className="text-sm text-gray-600">Part: {review.part_id}</div>
                <div className="text-sm text-amber-500 font-medium">Confidence: {(review.confidence*100).toFixed(1)}%</div>
              </li>
            ))}
          </ul>
        </div>

        <div className="w-full md:w-2/3 bg-white rounded-lg shadow-md border border-gray-200 p-6">
          {!selectedReview ? (
             <div className="flex justify-center items-center h-full text-gray-500">Select a review from the left panel.</div>
          ) : (
            <>
              <h2 className="text-xl font-semibold mb-4 text-[#1c1c1e]">Review Details: INSP-{selectedReview.id}</h2>
              <div className="bg-gray-200 h-80 rounded mb-6 flex items-center justify-center border border-gray-300 relative overflow-hidden">
                {selectedReview.image_path || selectedReview.image_url ? (
                  <img src={selectedReview.image_path || selectedReview.image_url} alt="Review Image" className="object-cover w-full h-full" />
                ) : (
                  <span className="text-gray-500 font-medium">Image Highlighting Low Confidence Regions</span>
                )}
              </div>
              
              <div className="grid grid-cols-2 gap-4 mb-6 bg-gray-50 p-4 rounded border border-gray-100">
                <div>
                  <p className="text-gray-500 text-sm font-medium">Shipment ID</p>
                  <p className="font-bold text-gray-900">{selectedReview.shipment_id || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-gray-500 text-sm font-medium">Part ID</p>
                  <p className="font-bold text-gray-900">{selectedReview.part_id || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-gray-500 text-sm font-medium">System Confidence</p>
                  <p className="font-bold text-amber-600">{((selectedReview.confidence || 0)*100).toFixed(1)}%</p>
                </div>
                <div>
                  <p className="text-gray-500 text-sm font-medium">Automated Result</p>
                  <p className="font-bold text-gray-900">{selectedReview.decision || selectedReview.status || 'N/A'}</p>
                </div>
                <div className="col-span-2">
                  <p className="text-gray-500 text-sm font-medium">Image Path</p>
                  <p className="font-bold text-gray-900 break-all">{selectedReview.image_path || selectedReview.image_url || 'N/A'}</p>
                </div>
                <div className="col-span-2">
                  <p className="text-gray-500 text-sm font-medium">Triggered Rules / Detected Issue</p>
                  <p className="font-bold text-amber-600">{
                    (selectedReview.triggered_rules && selectedReview.triggered_rules.length > 0)
                      ? selectedReview.triggered_rules.join(', ')
                      : 'Human review flagged due to rule thresholds.'
                  }</p>
                </div>
              </div>

          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2">Manager Override / Decision Reason (Required for Audit)</label>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[#0a84ff]"
              rows={3}
              placeholder="Explain why you are overriding or confirming this result..."
              value={overrideReason}
              onChange={(e) => setOverrideReason(e.target.value)}
              required
            ></textarea>
          </div>

          <div className="mb-6 flex items-center">
            <input 
              type="checkbox" 
              id="reviewed-evidence"
              checked={hasReviewed}
              onChange={(e) => setHasReviewed(e.target.checked)}
              className="mr-2"
            />
            <label htmlFor="reviewed-evidence" className="text-sm text-gray-700 font-medium">
              I have reviewed the evidence
            </label>
          </div>

          <div className="flex space-x-4 border-t pt-4">
            <button 
              onClick={() => handleAction('PASS')}
              disabled={isSubmitting || !overrideReason.trim() || !hasReviewed}
              className="flex-1 bg-green-600 text-white py-3 rounded font-bold hover:bg-green-700 shadow-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Override: READY TO DISPATCH
            </button>
            <button 
              onClick={() => handleAction('FAIL')}
              disabled={isSubmitting || !overrideReason.trim() || !hasReviewed}
              className="flex-1 bg-red-600 text-white py-3 rounded font-bold hover:bg-red-700 shadow-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Confirm: DO NOT DISPATCH
            </button>
          </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ManualReview;
