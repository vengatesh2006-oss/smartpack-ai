import React, { useState } from 'react';
import { X, Check, XCircle } from 'lucide-react';

interface ManualReviewModalProps {
  isOpen: boolean;
  onClose: () => void;
  packId: string;
  onSubmit: (status: 'Pass' | 'Fail', reason: string) => void;
}

export const ManualReviewModal: React.FC<ManualReviewModalProps> = ({
  isOpen,
  onClose,
  packId,
  onSubmit,
}) => {
  const [reason, setReason] = useState('');
  
  if (!isOpen) return null;

  const handleAction = (status: 'Pass' | 'Fail') => {
    onSubmit(status, reason);
    setReason('');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div className="bg-gray-800 rounded-xl border border-gray-700 shadow-2xl w-full max-w-lg overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        <div className="flex justify-between items-center p-4 border-b border-gray-700">
          <h2 className="text-lg font-bold text-white">Manual Review - Pack #{packId}</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <div className="p-6">
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Reason for Override (Optional)
          </label>
          <textarea
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[100px] resize-none mb-6"
            placeholder="Enter reason for this manual decision..."
          />
          
          <div className="flex gap-4">
            <button
              onClick={() => handleAction('Pass')}
              className="flex-1 flex items-center justify-center py-3 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors"
            >
              <Check className="w-5 h-5 mr-2" />
              Force Pass
            </button>
            <button
              onClick={() => handleAction('Fail')}
              className="flex-1 flex items-center justify-center py-3 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg transition-colors"
            >
              <XCircle className="w-5 h-5 mr-2" />
              Force Fail
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
