'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/auth-store';

export default function HomePage() {
  const router = useRouter();
  const { isAuthenticated, fetchCurrentUser, isLoading } = useAuthStore();

  useEffect(() => {
    const init = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          await fetchCurrentUser();
          router.push('/dashboard');
        } catch {
          router.push('/login');
        }
      } else {
        router.push('/login');
      }
    };
    init();
  }, [router, fetchCurrentUser]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-sky-500"></div>
      </div>
    );
  }

  return null;
}

