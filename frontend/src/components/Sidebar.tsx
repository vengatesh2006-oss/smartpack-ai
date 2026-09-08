import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Package, Activity, Settings, Users } from 'lucide-react';

export const Sidebar: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/', icon: Home },
    { name: 'Start Inspection', path: '/verify', icon: Activity },
    { name: 'History', path: '/history', icon: Package },
    { name: 'Operators', path: '/operators', icon: Users },
    { name: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-[#1c1c1e] border-r border-[#2c2c2e] flex flex-col shadow-xl">
      <div className="h-16 flex items-center px-6 border-b border-[#2c2c2e]">
        <span className="text-xl font-bold text-gray-100 tracking-wider uppercase">SmartPack AI</span>
      </div>
      <nav className="flex-1 py-4">
        <ul className="space-y-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path || (item.name === 'Start Inspection' && location.pathname.startsWith('/verification'));
            const Icon = item.icon;
            return (
              <li key={item.name}>
                <Link
                  to={item.path}
                  className={`flex items-center px-6 py-3 text-sm font-medium transition-colors ${
                    isActive
                      ? 'text-[#0a84ff] bg-[#2c2c2e] border-r-4 border-[#0a84ff]'
                      : 'text-gray-400 hover:text-gray-200 hover:bg-[#2c2c2e]'
                  }`}
                >
                  <Icon className="w-5 h-5 mr-3" />
                  {item.name}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
      <div className="p-4 border-t border-[#2c2c2e]">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-full bg-[#0a84ff] flex items-center justify-center text-white font-bold">
            O
          </div>
          <div>
            <p className="text-sm font-medium text-gray-200">Operator 1</p>
            <p className="text-xs text-gray-500">Station A</p>
          </div>
        </div>
      </div>
    </aside>
  );
};
