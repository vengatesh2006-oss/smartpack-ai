import React from 'react';
import { Routes, Route, Link, useNavigate, useLocation, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import { clearAuth } from './services/auth';

import Dashboard from './pages/Dashboard';
import VerifyPacking from './pages/VerifyPacking';
import VerificationResult from './pages/VerificationResult';
import ManualReview from './pages/ManualReview';
import InspectionHistory from './pages/InspectionHistory';
import InspectionDetails from './pages/InspectionDetails';
import PartsRules from './pages/PartsRules';
import Experiment from './pages/Experiment';
import TestHarness from './pages/TestHarness';
import SystemStatus from './pages/SystemStatus';
import Validation from './pages/Validation';
import Login from './pages/Login';
import Register from './pages/Register';
import Settings from './pages/Settings';

const ProtectedRoute = ({ children, allowedRoles }: { children: React.ReactNode, allowedRoles?: string[] }) => {
  const { isAuthenticated, user } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  if (allowedRoles && user && !allowedRoles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }
  
  return <>{children}</>;
};

const Layout = ({ children }: { children: React.ReactNode }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  if (location.pathname === '/login' || location.pathname === '/register') return <>{children}</>;

  const handleLogout = () => {
    clearAuth();
    navigate('/login');
  };

  const isManager = user?.role === 'manager';

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-900 text-white flex flex-col">
        <div className="p-4 border-b border-gray-800">
          <h1 className="text-xl font-bold uppercase tracking-wider text-blue-400">SmartPack AI</h1>
          <p className="text-xs text-gray-400 mt-1">Quality Verification</p>
        </div>
        <nav className="flex-1 overflow-y-auto py-4 space-y-1">
          <Link to="/" className={`block px-4 py-2 hover:bg-gray-800 ${location.pathname === '/' ? 'bg-gray-800 text-blue-400 border-l-4 border-blue-400' : ''}`}>Dashboard</Link>
          <Link to="/verify" className={`block px-4 py-2 hover:bg-gray-800 ${location.pathname === '/verify' ? 'bg-gray-800 text-blue-400 border-l-4 border-blue-400' : ''}`}>Verify Packing</Link>
          
          {isManager && (
            <>
              <Link to="/review" className={`block px-4 py-2 hover:bg-gray-800 ${location.pathname === '/review' ? 'bg-gray-800 text-blue-400 border-l-4 border-blue-400' : ''}`}>Manual Review</Link>
              <Link to="/history" className={`block px-4 py-2 hover:bg-gray-800 ${location.pathname.startsWith('/history') ? 'bg-gray-800 text-blue-400 border-l-4 border-blue-400' : ''}`}>Inspection History</Link>
              <Link to="/rules" className={`block px-4 py-2 hover:bg-gray-800 ${location.pathname === '/rules' ? 'bg-gray-800 text-blue-400 border-l-4 border-blue-400' : ''}`}>Parts & Rules</Link>
              <div className="px-4 py-2 mt-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">System</div>
              <Link to="/experiment" className={`block px-4 py-2 hover:bg-gray-800 ${location.pathname === '/experiment' ? 'bg-gray-800 text-blue-400 border-l-4 border-blue-400' : ''}`}>Experiment</Link>
              <Link to="/test" className={`block px-4 py-2 hover:bg-gray-800 ${location.pathname === '/test' ? 'bg-gray-800 text-blue-400 border-l-4 border-blue-400' : ''}`}>Test Harness</Link>
              <Link to="/status" className={`block px-4 py-2 hover:bg-gray-800 ${location.pathname === '/status' ? 'bg-gray-800 text-blue-400 border-l-4 border-blue-400' : ''}`}>System Status</Link>
              <Link to="/validation" className={`block px-4 py-2 hover:bg-gray-800 ${location.pathname === '/validation' ? 'bg-gray-800 text-blue-400 border-l-4 border-blue-400' : ''}`}>Validation</Link>
              <Link to="/settings" className={`block px-4 py-2 hover:bg-gray-800 ${location.pathname === '/settings' ? 'bg-gray-800 text-blue-400 border-l-4 border-blue-400' : ''}`}>Settings</Link>
            </>
          )}
        </nav>
        <div className="p-4 border-t border-gray-800 text-sm">
          <p className="text-gray-400">User: <span className="text-white">{user?.name || 'Unknown'}</span></p>
          <p className="text-gray-400">Role: <span className="text-white capitalize">{user?.role || 'User'}</span></p>
          <p className="text-green-400 mt-2 flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-green-500"></span> ONLINE</p>
        </div>
      </aside>
      
      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white shadow-sm z-10 p-4 flex justify-between items-center">
          <h2 className="text-xl font-semibold text-gray-800">
            {location.pathname === '/' ? 'Dashboard' : 
             location.pathname === '/verify' ? 'Verify Packing' :
             location.pathname === '/review' ? 'Manual Review' :
             location.pathname.startsWith('/history') ? 'Inspection History' :
             location.pathname === '/rules' ? 'Parts & Rules' :
             location.pathname === '/experiment' ? 'Experiment' :
             location.pathname === '/test' ? 'Test Harness' :
             location.pathname === '/status' ? 'System Status' :
             location.pathname === '/validation' ? 'Validation' :
             location.pathname === '/settings' ? 'Settings' : 'SmartPack AI'}
          </h2>
          <div className="flex items-center gap-4">
            <button onClick={handleLogout} className="text-sm text-gray-600 hover:text-gray-900 cursor-pointer">Logout</button>
          </div>
        </header>
        <div className="flex-1 overflow-y-auto p-6">
          {children}
        </div>
      </main>
    </div>
  );
};

const App = () => {
  return (
    <Layout>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* Protected Routes */}
        <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/verify" element={<ProtectedRoute><VerifyPacking /></ProtectedRoute>} />
        <Route path="/result/:id" element={<ProtectedRoute><VerificationResult /></ProtectedRoute>} />
        
        {/* Manager Only Routes */}
        <Route path="/review" element={<ProtectedRoute allowedRoles={['manager']}><ManualReview /></ProtectedRoute>} />
        <Route path="/history" element={<ProtectedRoute allowedRoles={['manager']}><InspectionHistory /></ProtectedRoute>} />
        <Route path="/history/:id" element={<ProtectedRoute allowedRoles={['manager']}><InspectionDetails /></ProtectedRoute>} />
        <Route path="/rules" element={<ProtectedRoute allowedRoles={['manager']}><PartsRules /></ProtectedRoute>} />
        <Route path="/experiment" element={<ProtectedRoute allowedRoles={['manager']}><Experiment /></ProtectedRoute>} />
        <Route path="/test" element={<ProtectedRoute allowedRoles={['manager']}><TestHarness /></ProtectedRoute>} />
        <Route path="/status" element={<ProtectedRoute allowedRoles={['manager']}><SystemStatus /></ProtectedRoute>} />
        <Route path="/validation" element={<ProtectedRoute allowedRoles={['manager']}><Validation /></ProtectedRoute>} />
        <Route path="/settings" element={<ProtectedRoute allowedRoles={['manager']}><Settings /></ProtectedRoute>} />
      </Routes>
    </Layout>
  );
};

export default App;
