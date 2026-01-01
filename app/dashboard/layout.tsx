'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/auth-store';
import { useAppStore } from '@/store/app-store';
import { Header } from '@/components/header';
import { Sidebar } from '@/components/sidebar';
import { toast } from 'react-hot-toast';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { isAuthenticated, isLoading, fetchCurrentUser, logout } = useAuthStore();
  const { currentTab, setCurrentTab, activeAthlete, theme, toggleTheme } = useAppStore();

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/login');
        return;
      }

      if (!isAuthenticated) {
        try {
          await fetchCurrentUser();
        } catch {
          router.push('/login');
        }
      }
    };

    checkAuth();
  }, [isAuthenticated, router, fetchCurrentUser]);

  const handleToggleTheme = () => {
    toggleTheme();
  };

  const handleLogout = async () => {
    await logout();
    router.push('/login');
    toast.success('خروج با موفقیت انجام شد');
  };

  const handleBackup = () => {
    // TODO: Implement backup functionality
    toast.success('بکاپ در حال آماده‌سازی...');
  };

  const handleRestore = async (file: File) => {
    // TODO: Implement restore functionality
    toast.success('بازیابی در حال انجام...');
  };

  const handleReset = () => {
    if (confirm('آیا مطمئن هستید؟ تمام اطلاعات پاک خواهد شد!')) {
      localStorage.clear();
      window.location.reload();
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-sky-500"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <div className="bg-gradient-animated"></div>
      <div className="orb orb-1"></div>
      <div className="orb orb-2"></div>
      <div className="fixed inset-0 bg-[var(--bg-primary)]/80 z-[-1]"></div>

      <Header 
        toggleTheme={handleToggleTheme}
        isDark={theme === 'dark'}
        activeUser={activeAthlete}
        onLogout={handleLogout}
      />
      
      <div className="flex flex-1 overflow-hidden">
        <Sidebar 
          currentTab={currentTab}
          setTab={setCurrentTab}
          onBackup={handleBackup}
          onRestore={handleRestore}
          onReset={handleReset}
        />
        <main className="flex-1 overflow-y-auto p-4 lg:p-8 relative scroll-smooth">
          {children}
        </main>
      </div>
    </div>
  );
}

