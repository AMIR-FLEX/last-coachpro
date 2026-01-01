import { create } from 'zustand';
import type { TabType, Athlete } from '@/types';

interface AppState {
  theme: 'dark' | 'light';
  currentTab: TabType;
  activeAthleteId: number | null;
  activeAthlete: Athlete | null;
  
  // Actions
  setTheme: (theme: 'dark' | 'light') => void;
  setCurrentTab: (tab: TabType) => void;
  setActiveAthleteId: (id: number | null) => void;
  setActiveAthlete: (athlete: Athlete | null) => void;
  toggleTheme: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  theme: (typeof window !== 'undefined' && localStorage.getItem('theme') === 'light') ? 'light' : 'dark',
  currentTab: 'users',
  activeAthleteId: null,
  activeAthlete: null,

  setTheme: (theme) => {
    set({ theme });
    if (typeof window !== 'undefined') {
      localStorage.setItem('theme', theme);
      document.documentElement.classList.toggle('dark', theme === 'dark');
    }
  },

  setCurrentTab: (tab) => set({ currentTab: tab }),

  setActiveAthleteId: (id) => set({ activeAthleteId: id }),

  setActiveAthlete: (athlete) => set({ activeAthlete: athlete, activeAthleteId: athlete?.id ?? null }),

  toggleTheme: () => {
    set((state) => {
      const newTheme = state.theme === 'dark' ? 'light' : 'dark';
      if (typeof window !== 'undefined') {
        localStorage.setItem('theme', newTheme);
        document.documentElement.classList.toggle('dark', newTheme === 'dark');
      }
      return { theme: newTheme };
    });
  },
}));

