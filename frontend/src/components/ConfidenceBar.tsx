import React from 'react';

interface ConfidenceBarProps {
  score: number; // 0 to 100
}

export const ConfidenceBar: React.FC<ConfidenceBarProps> = ({ score }) => {
  const getColor = () => {
    if (score >= 90) return 'bg-green-500';
    if (score >= 75) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="w-full">
      <div className="flex justify-between mb-1">
        <span className="text-xs font-medium text-gray-400">AI Confidence</span>
        <span className="text-xs font-medium text-gray-300">{score.toFixed(1)}%</span>
      </div>
      <div className="w-full bg-gray-700 rounded-full h-2">
        <div
          className={`h-2 rounded-full ${getColor()}`}
          style={{ width: `${Math.min(Math.max(score, 0), 100)}%` }}
        ></div>
      </div>
    </div>
  );
};
