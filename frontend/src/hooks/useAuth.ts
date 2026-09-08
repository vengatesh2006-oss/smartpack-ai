import { useState, useEffect } from 'react';
import { getUser, isAuthenticated, User } from '../services/auth';

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(getUser());
  const [isAuth, setIsAuth] = useState<boolean>(isAuthenticated());

  useEffect(() => {
    const handleStorageChange = () => {
      setUser(getUser());
      setIsAuth(isAuthenticated());
    };
    
    // Listen for storage events to sync across tabs, or custom events
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  return { user, isAuthenticated: isAuth };
};
