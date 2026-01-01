'use client';

import type { TabType } from '@/types';

interface SidebarProps {
  currentTab: TabType;
  setTab: (tab: TabType) => void;
  onBackup: () => void;
  onRestore: (file: File) => void;
  onReset: () => void;
}

export function Sidebar({ currentTab, setTab, onBackup, onRestore, onReset }: SidebarProps) {
  
  const renderButton = (id: TabType, label: string, icon: string) => (
    <button 
      onClick={() => setTab(id)} 
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group relative overflow-hidden ${
        currentTab === id 
        ? 'bg-sky-600 text-white shadow-lg shadow-sky-500/30' 
        : 'text-[var(--text-secondary)] hover:bg-[var(--text-primary)]/5 hover:text-[var(--text-primary)]'
      }`}
    >
      <span className="text-xl relative z-10">{icon}</span>
      <span className="font-medium text-sm relative z-10">{label}</span>
    </button>
  );

  return (
    <aside className="w-72 glass-panel !rounded-none !border-y-0 !border-r-0 flex flex-col h-full z-30">
      <div className="p-5 space-y-6 overflow-y-auto flex-1 custom-scrollbar">
        <nav className="space-y-2">
          
          <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-4 mt-2 mb-2">داشبورد</div>
          {renderButton('users', 'مدیریت شاگردان', '👥')}

          <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-4 mt-6 mb-2">طراحی برنامه</div>
          {renderButton('training', 'برنامه تمرینی', '🏋️')}
          {renderButton('nutrition', 'رژیم غذایی', '🥗')}
          {renderButton('supplements', 'مکمل‌ها و داروها', '💊')}

          <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-4 mt-6 mb-2">گزارشات</div>
          {renderButton('progress', 'کارتابل و پیشرفت شاگرد', '📈')}
        
        </nav>
      </div>

      <div className="p-5 border-t border-[var(--glass-border)] bg-[var(--glass-bg)]">
        <div className="grid grid-cols-2 gap-3 mb-4">
          <button onClick={onBackup} className="bg-sky-500/10 hover:bg-sky-500/20 text-sky-600 dark:text-sky-400 border border-sky-500/20 py-2.5 rounded-xl text-xs transition flex justify-center items-center gap-2 font-bold">
            <span>⬇️</span> بکاپ
          </button>
          <label className="bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 py-2.5 rounded-xl text-xs transition flex justify-center items-center gap-2 cursor-pointer font-bold">
            <span>⬆️</span> بازیابی
            <input 
              type="file" 
              className="hidden" 
              accept=".json" 
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) onRestore(file);
              }} 
            />
          </label>
        </div>
        <button onClick={onReset} className="w-full text-[10px] text-red-500/70 hover:text-red-500 transition py-2 hover:bg-red-500/10 rounded-lg">
          ⚠ بازنشانی تنظیمات کارخانه
        </button>
      </div>
    </aside>
  );
}
