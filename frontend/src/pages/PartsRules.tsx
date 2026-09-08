import React from 'react';

const rules = [
  { id: 'RUL-1', part: 'Engine Block', materials: ['Foam Padding', 'VCI Bag', 'Desiccant (x2)'], lastUpdated: '2023-09-15' },
  { id: 'RUL-2', part: 'Brake Pads', materials: ['Cardboard Divider', 'Shrink Wrap'], lastUpdated: '2023-09-10' },
  { id: 'RUL-3', part: 'Transmission Gear', materials: ['Bubble Wrap', 'Foam Padding'], lastUpdated: '2023-08-22' },
];

const PartsRules: React.FC = () => {
  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Parts & Rules Configuration</h1>
        <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 font-medium">
          + Add New Rule
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rule ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Part Category</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Required Packaging Materials</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Updated</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {rules.map((rule) => (
              <tr key={rule.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{rule.id}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{rule.part}</td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  <div className="flex flex-wrap gap-1">
                    {rule.materials.map(mat => (
                      <span key={mat} className="px-2 py-1 bg-gray-100 rounded text-xs">{mat}</span>
                    ))}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{rule.lastUpdated}</td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button className="text-indigo-600 hover:text-indigo-900 mr-3">Edit</button>
                  <button className="text-red-600 hover:text-red-900">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PartsRules;
