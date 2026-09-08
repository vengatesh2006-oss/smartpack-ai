import React from 'react';

const Validation: React.FC = () => {
  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Stakeholder Validation</h1>
      
      <div className="bg-white p-8 rounded-lg shadow max-w-2xl">
        <p className="mb-6 text-gray-600">Please provide your sign-off for the current deployment candidate of the packaging verification model.</p>
        
        <form>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">Stakeholder Name</label>
            <input type="text" className="w-full px-3 py-2 border rounded" placeholder="John Doe" />
          </div>
          
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">Department</label>
            <select className="w-full px-3 py-2 border rounded">
              <option>Quality Assurance</option>
              <option>Operations</option>
              <option>Engineering</option>
            </select>
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2">Validation Decision</label>
            <div className="flex space-x-4">
              <label className="flex items-center">
                <input type="radio" name="decision" value="approve" className="mr-2" />
                Approve for Production
              </label>
              <label className="flex items-center">
                <input type="radio" name="decision" value="reject" className="mr-2" />
                Reject / Needs Work
              </label>
            </div>
          </div>
          
          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2">Comments</label>
            <textarea className="w-full px-3 py-2 border rounded" rows={4} placeholder="Enter any specific observations or requirements..."></textarea>
          </div>

          <button type="button" className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 font-medium">
            Submit Validation
          </button>
        </form>
      </div>
    </div>
  );
};

export default Validation;
