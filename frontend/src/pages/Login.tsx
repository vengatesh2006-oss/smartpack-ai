import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { login } from '../services/api';
import { setAuth } from '../services/auth';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const data = await login({ username: email, password });
      setAuth(data.access_token, {
        id: data.sub || email,
        name: data.name,
        role: data.role
      });
      navigate('/');
      window.location.reload(); // refresh to update auth state
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Invalid credentials. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Branding Side */}
      <div className="hidden lg:flex w-1/2 bg-[#1c1c1e] text-white flex-col justify-center px-16 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-blue-900/30 to-transparent"></div>
        <div className="z-10">
          <h1 className="text-5xl font-bold mb-4 tracking-tight">SmartPack AI</h1>
          <p className="text-xl text-gray-300 mb-12">Automotive Packing Quality Verification</p>
          
          <div className="space-y-8">
            <h2 className="text-2xl font-semibold">Verify every packed part before it leaves the warehouse.</h2>
            <ul className="space-y-4">
              <li className="flex items-center text-lg">
                <span className="text-blue-500 mr-3">✓</span> Check packaging requirements
              </li>
              <li className="flex items-center text-lg">
                <span className="text-blue-500 mr-3">✓</span> Detect packing issues before dispatch
              </li>
              <li className="flex items-center text-lg">
                <span className="text-blue-500 mr-3">✓</span> Keep every decision traceable
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Right Auth Side */}
      <div className="w-full lg:w-1/2 flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full px-8 py-10 bg-white shadow-xl rounded-xl border border-gray-100">
          <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">Login</h2>
          
          {error && (
            <div className="bg-red-50 text-red-700 p-3 rounded mb-6 text-sm border border-red-200">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email or Username</label>
              <input
                type="text"
                required
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="operator@example.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
              <input
                type="password"
                required
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className={`w-full py-3 px-4 rounded-lg text-white font-semibold transition-colors shadow-md
                ${isLoading ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
            >
              {isLoading ? 'Signing In...' : 'SIGN IN'}
            </button>
          </form>

          <p className="mt-8 text-center text-sm text-gray-600">
            Don't have an account?{' '}
            <Link to="/register" className="text-blue-600 hover:text-blue-800 font-semibold transition-colors">
              Create one
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
