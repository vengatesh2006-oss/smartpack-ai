import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { getDashboardMetrics } from '../services/api';

const COLORS = ['#00C49F', '#FF8042', '#FFBB28'];

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboardMetrics()
      .then(data => {
        setMetrics(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="p-6 flex justify-center items-center h-full"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#0a84ff]"></div></div>;
  }

  // Fallback data if API fails
  const safeMetrics = metrics || {
    total_inspections: 0,
    passed: 0,
    failed: 0,
    daily_stats: []
  };

  const total = safeMetrics?.total_inspections ?? 0;
  const passed = safeMetrics?.passed ?? 0;
  const failed = safeMetrics?.failed ?? 0;

  const pieData = [
    { name: 'Ready to Dispatch', value: passed },
    { name: 'Do Not Dispatch', value: failed },
    { name: 'Human Review', value: Math.max(0, total - passed - failed) },
  ];

  const passRate = total > 0 
    ? ((passed / total) * 100).toFixed(1)
    : '0.0';

  const barData = safeMetrics?.daily_stats?.length > 0 ? safeMetrics.daily_stats : [
    { name: 'Mon', passed: 0, failed: 0 },
    { name: 'Tue', passed: 0, failed: 0 },
    { name: 'Wed', passed: 0, failed: 0 },
    { name: 'Thu', passed: 0, failed: 0 },
    { name: 'Fri', passed: 0, failed: 0 },
    { name: 'Sat', passed: 0, failed: 0 },
    { name: 'Sun', passed: 0, failed: 0 },
  ];

  const hasPieData = pieData.some(d => d.value > 0);

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow border border-gray-100">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Weekly Inspection Volume</h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="passed" name="Ready" fill="#00C49F" />
                <Bar dataKey="failed" name="Failed/Review" fill="#FF8042" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border border-gray-100">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Status Distribution</h2>
          <div className="h-72">
            {hasPieData ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    fill="#8884d8"
                    paddingAngle={5}
                    dataKey="value"
                    label
                  >
                    {pieData.map((_entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex justify-center items-center h-full text-gray-400">
                No data available
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow border border-gray-100 text-center">
          <p className="text-gray-500 text-sm font-medium uppercase tracking-wide">Total Inspections</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{total}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow border border-gray-100 text-center">
          <p className="text-gray-500 text-sm font-medium uppercase tracking-wide">Ready to Dispatch Rate</p>
          <p className="text-3xl font-bold text-green-600 mt-2">{passRate}%</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow border border-gray-100 text-center">
          <p className="text-gray-500 text-sm font-medium uppercase tracking-wide">Pending Reviews</p>
          <p className="text-3xl font-bold text-amber-500 mt-2">{Math.max(0, total - passed - failed)}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow border border-gray-100 text-center">
          <p className="text-gray-500 text-sm font-medium uppercase tracking-wide">Avg Processing Time</p>
          <p className="text-3xl font-bold text-[#0a84ff] mt-2">1.2s</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
