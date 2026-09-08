import React, { useState, useEffect } from 'react';
import { Bell, Wifi, WifiOff } from 'lucide-react';

export const Topbar: React.FC = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return (
    <header className="h-16 bg-gray-800 border-b border-gray-700 flex items-center justify-between px-6">
      <div className="flex items-center">
        <h1 className="text-lg font-semibold text-white">Station Overview</h1>
      </div>
      <div className="flex items-center space-x-4">
        {isOnline ? (
          <div className="flex items-center text-green-400 text-sm font-medium bg-green-400/10 px-3 py-1 rounded-full">
            <Wifi className="w-4 h-4 mr-2" />
            Online
          </div>
        ) : (
          <div className="flex items-center text-red-400 text-sm font-medium bg-red-400/10 px-3 py-1 rounded-full">
            <WifiOff className="w-4 h-4 mr-2" />
            Offline Mode
          </div>
        )}
        <button className="text-gray-400 hover:text-white relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-500 ring-2 ring-gray-800"></span>
        </button>
      </div>
    </header>
  );
};
