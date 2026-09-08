import React from 'react';
import { CheckCircle2, XCircle } from 'lucide-react';

interface Rule {
  id: string;
  description: string;
  passed: boolean;
}

interface RuleChecklistProps {
  rules: Rule[];
}

export const RuleChecklist: React.FC<RuleChecklistProps> = ({ rules }) => {
  return (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
      <h3 className="text-sm font-semibold text-gray-300 mb-3 uppercase tracking-wider">Verification Rules</h3>
      <ul className="space-y-3">
        {rules.map((rule) => (
          <li key={rule.id} className="flex items-start">
            {rule.passed ? (
              <CheckCircle2 className="w-5 h-5 text-green-500 mt-0.5 mr-3 flex-shrink-0" />
            ) : (
              <XCircle className="w-5 h-5 text-red-500 mt-0.5 mr-3 flex-shrink-0" />
            )}
            <span className={`text-sm ${rule.passed ? 'text-gray-300' : 'text-red-400 font-medium'}`}>
              {rule.description}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};
