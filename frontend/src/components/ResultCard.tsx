import React from 'react';
import { StatusBadge } from './StatusBadge';
import { ConfidenceBar } from './ConfidenceBar';
import { RuleChecklist } from './RuleChecklist';
import { AlertTriangle, Clock } from 'lucide-react';

interface ResultCardProps {
  id: string;
  status: 'Pass' | 'Fail' | 'Review';
  confidence: number;
  timestamp: string;
  packId: string;
  rules: { id: string; description: string; passed: boolean }[];
  onReviewClick?: () => void;
}

export const ResultCard: React.FC<ResultCardProps> = ({
  status,
  confidence,
  timestamp,
  packId,
  rules,
  onReviewClick,
}) => {
  return (
    <div className="bg-gray-800 rounded-xl border border-gray-700 shadow-lg overflow-hidden flex flex-col">
      <div className="p-5 border-b border-gray-700 flex justify-between items-start bg-gray-800/50">
        <div>
          <h2 className="text-lg font-bold text-white mb-1">Pack #{packId}</h2>
          <div className="flex items-center text-xs text-gray-400">
            <Clock className="w-3.5 h-3.5 mr-1" />
            {new Date(timestamp).toLocaleString()}
          </div>
        </div>
        <StatusBadge status={status} />
      </div>
      
      <div className="p-5 flex-1 flex flex-col gap-5">
        <div>
          <ConfidenceBar score={confidence} />
        </div>
        
        <RuleChecklist rules={rules} />
      </div>
      
      {status === 'Review' && onReviewClick && (
        <div className="p-4 border-t border-gray-700 bg-yellow-500/5">
          <div className="flex items-center justify-between">
            <div className="flex items-center text-sm text-yellow-400 font-medium">
              <AlertTriangle className="w-4 h-4 mr-2" />
              Manual review required
            </div>
            <button
              onClick={onReviewClick}
              className="px-4 py-2 bg-yellow-500 hover:bg-yellow-600 text-gray-900 text-sm font-bold rounded-lg transition-colors"
            >
              Review Now
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
