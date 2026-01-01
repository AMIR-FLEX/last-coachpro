import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(d);
}

export function formatDateShort(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat('fa-IR').format(d);
}

export function getFinancialStatus(
  startDate?: string,
  duration?: number
): { text: string; color: string; icon: string } {
  if (!startDate) {
    return {
      text: 'نامشخص',
      color: 'text-slate-400 bg-slate-500/10',
      icon: '⚠️',
    };
  }

  const start = new Date(startDate);
  const end = new Date(start);
  end.setMonth(end.getMonth() + (duration || 1));
  const now = new Date();
  const daysLeft = Math.ceil((end.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));

  if (daysLeft < 0) {
    return {
      text: 'منقضی شده',
      color: 'text-red-500 bg-red-500/10',
      icon: '❌',
    };
  }

  if (daysLeft <= 5) {
    return {
      text: `${daysLeft} روز مانده`,
      color: 'text-yellow-500 bg-yellow-500/10',
      icon: '⚠️',
    };
  }

  return {
    text: 'فعال',
    color: 'text-emerald-500 bg-emerald-500/10',
    icon: '✅',
  };
}

