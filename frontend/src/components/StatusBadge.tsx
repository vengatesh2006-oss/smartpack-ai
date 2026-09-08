import React from 'react';

type StatusType = 'Pass' | 'Fail' | 'Review';

interface StatusBadgeProps {
  status: StatusType;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const getStyles = () => {
    switch (status) {
      case 'Pass':
        return 'bg-green-500/10 text-green-400 border border-green-500/20';
      case 'Fail':
        return 'bg-red-500/10 text-red-400 border border-red-500/20';
      case 'Review':
        return 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20';
      default:
        return 'bg-gray-500/10 text-gray-400 border border-gray-500/20';
    }
  };

  return (
    <span className={`px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider ${getStyles()}`}>
      {status}
    </span>
  );
};
