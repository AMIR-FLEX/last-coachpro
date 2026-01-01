'use client';

import { useEffect, useState } from 'react';
import { Sun, Moon, LogOut } from 'lucide-react';
import type { Athlete } from '@/types';

interface HeaderProps {
  toggleTheme: () => void;
  isDark: boolean;
  activeUser: Athlete | null;
  onLogout: () => void;
}

export function Header({ toggleTheme, isDark, activeUser, onLogout }: HeaderProps) {
  const [currentDate, setCurrentDate] = useState('');

  useEffect(() => {
    const date = new Date().toLocaleDateString('fa-IR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    setCurrentDate(date);
  }, []);

  return (
    <header className="h-20 glass-panel border-b border-white/10 flex items-center justify-between px-8 z-40 shrink-0 !bg-opacity-80 !rounded-none !border-x-0 !border-t-0">
      <div className="flex items-center gap-4">
        <div className="relative group cursor-pointer">
          <div className="absolute inset-0 bg-sky-500 rounded-full blur opacity-40 group-hover:opacity-60 transition-opacity"></div>
          <img 
            src="https://placehold.co/100x100/38bdf8/white?text=FLEX" 
            alt="Logo" 
            className="h-11 w-11 rounded-full object-cover relative z-10 border-2 border-white/20" 
          />
        </div>
        <div>
          <h1 className="text-2xl font-black text-[var(--text-primary)] tracking-tighter italic drop-shadow-sm">
            FLEX <span className="text-sky-500 dark:text-sky-400">PRO</span>
          </h1>
          <div className="flex items-center gap-2">
            <span className="text-[10px] text-[var(--text-secondary)] font-medium tracking-widest uppercase">V12.0 Ultra</span>
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]"></span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-5">
        <span className="text-xs font-bold text-[var(--text-secondary)] hidden md:block bg-[var(--glass-bg)] px-3 py-1.5 rounded-full border border-[var(--glass-border)]">
          {currentDate}
        </span>
        
        <button onClick={toggleTheme} className="btn-glass bg-[var(--glass-bg)] hover:bg-black/5 dark:hover:bg-white/10 text-[var(--text-primary)] !p-2 rounded-full border border-[var(--glass-border)]">
          {isDark ? <Sun size={20} className="text-yellow-400"/> : <Moon size={20} className="text-slate-600"/>}
        </button>

        {activeUser && (
          <div className="flex items-center gap-3 bg-gradient-to-r from-sky-600 to-blue-600 text-white px-5 py-2 rounded-xl shadow-lg shadow-sky-500/20 border border-white/10 animate-fade-in">
            <div className="flex flex-col items-end leading-none">
              <span className="text-[9px] opacity-80 font-bold uppercase tracking-wider mb-0.5">ورزشکار فعال</span>
              <span className="font-bold text-sm">{activeUser.name}</span>
            </div>
            <button 
              onClick={onLogout} 
              className="bg-white/20 hover:bg-white/30 text-white rounded-full p-1 w-6 h-6 flex items-center justify-center transition backdrop-blur-sm"
            >
              <LogOut size={12}/>
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
