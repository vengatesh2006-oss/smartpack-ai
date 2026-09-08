import React from 'react';

const Settings: React.FC = () => {
  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Settings</h1>
      
      <div className="bg-white p-6 rounded-lg shadow max-w-3xl space-y-8">
        <div>
          <h2 className="text-xl font-semibold mb-4 border-b pb-2">General</h2>
          <div className="flex items-center justify-between mb-4">
            <div>
              <p className="font-medium text-gray-700">Dark Mode</p>
              <p className="text-sm text-gray-500">Toggle dark theme for the dashboard</p>
            </div>
            <input type="checkbox" className="w-5 h-5" />
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4 border-b pb-2">Notifications</h2>
          <div className="flex items-center justify-between mb-4">
            <div>
              <p className="font-medium text-gray-700">Email Alerts on Failure</p>
              <p className="text-sm text-gray-500">Send an email when a manual review is required</p>
            </div>
            <input type="checkbox" defaultChecked className="w-5 h-5" />
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4 border-b pb-2">AI Configuration</h2>
          <div className="mb-4">
            <label className="block font-medium text-gray-700 mb-1">Confidence Threshold</label>
            <p className="text-sm text-gray-500 mb-2">Inspections below this confidence % will be sent to manual review.</p>
            <input type="range" min="50" max="99" defaultValue="85" className="w-full" />
            <div className="text-right text-sm text-gray-600 mt-1">Current: 85%</div>
          </div>
        </div>

        <button className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 font-medium">
          Save Changes
        </button>
      </div>
    </div>
  );
};

export default Settings;
