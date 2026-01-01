'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import { Search, UserPlus, Edit, Trash2, Printer, CheckCircle, XCircle, AlertTriangle, Loader2 } from 'lucide-react';
import { apiClient } from '@/lib/api-client';
import { useAppStore } from '@/store/app-store';
import { getFinancialStatus } from '@/lib/utils';
import { toast } from 'react-hot-toast';
import Swal from 'sweetalert2';
import type { Athlete } from '@/types';

export function UserList() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { setCurrentTab, theme } = useAppStore();
  const [searchTerm, setSearchTerm] = useState('');

  const { data: athletes = [], isLoading } = useQuery<Athlete[]>({
    queryKey: ['athletes'],
    queryFn: () => apiClient.getAthletes({ limit: 100 }),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => apiClient.deleteAthlete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['athletes'] });
      toast.success('شاگرد حذف شد');
    },
    onError: () => {
      toast.error('خطا در حذف شاگرد');
    },
  });

  const filteredAthletes = athletes.filter(
    (u) =>
      u.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (u.phone && u.phone.includes(searchTerm))
  );

  const handleSelect = (athlete: Athlete) => {
    const { setActiveAthlete } = useAppStore.getState();
    setActiveAthlete(athlete);
    setCurrentTab('training');
    router.push(`/dashboard/athletes/${athlete.id}`);
  };

  const handleDelete = (id: number, name: string) => {
    Swal.fire({
      title: 'آیا مطمئن هستید؟',
      text: `اطلاعات ${name} غیرقابل بازگشت خواهد بود!`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#ef4444',
      cancelButtonColor: '#64748b',
      confirmButtonText: 'بله، حذف کن',
      cancelButtonText: 'لغو',
      background: theme === 'dark' ? '#1e293b' : '#fff',
      color: theme === 'dark' ? '#fff' : '#000',
    }).then((result) => {
      if (result.isConfirmed) {
        deleteMutation.mutate(id);
      }
    });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loader2 className="w-8 h-8 animate-spin text-sky-500" />
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* هدر و جستجو */}
      <div className="flex flex-col md:flex-row justify-between items-center glass-panel p-5 rounded-2xl gap-4 sticky top-0 z-20">
        <div>
          <h2 className="text-2xl font-black text-[var(--text-primary)]">
            لیست شاگردان ({filteredAthletes.length})
          </h2>
        </div>
        <div className="flex gap-3 w-full md:w-auto">
          <div className="relative flex-1 md:w-64">
            <input
              type="text"
              placeholder="جستجو..."
              className="input-glass pl-10 py-2.5"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <Search className="absolute left-3 top-3 text-slate-400 w-4 h-4" />
          </div>
          <button
            onClick={() => router.push('/dashboard/athletes/new')}
            className="btn-glass bg-sky-600 hover:bg-sky-500 text-white text-sm py-2.5"
          >
            <UserPlus size={18} /> جدید
          </button>
        </div>
      </div>

      {/* لیست کارت‌ها */}
      <div className="flex flex-col gap-4">
        {filteredAthletes.map((athlete) => {
          const status = getFinancialStatus(athlete.subscription_start, athlete.subscription_months);
          return (
            <div
              key={athlete.id}
              className="glass-card flex flex-col md:flex-row items-center justify-between p-4 gap-4 group hover:border-sky-500/40"
            >
              {/* بخش اطلاعات */}
              <div className="flex items-center gap-4 w-full md:w-auto">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-sky-500 to-blue-600 flex items-center justify-center text-white font-bold text-lg shadow-lg">
                  {athlete.name.charAt(0)}
                </div>
                <div>
                  <h3 className="font-bold text-lg text-[var(--text-primary)]">{athlete.name}</h3>
                  <div className="flex items-center gap-3 text-xs text-[var(--text-secondary)] mt-1">
                    <span className="flex items-center gap-1 bg-[var(--glass-border)] px-2 py-0.5 rounded">
                      {athlete.age || '-'} ساله
                    </span>
                    <span className="flex items-center gap-1 bg-[var(--glass-border)] px-2 py-0.5 rounded">
                      {athlete.weight || '-'} kg
                    </span>
                    <span className={`flex items-center gap-1 px-2 py-0.5 rounded font-bold ${status.color}`}>
                      {status.icon} {status.text}
                    </span>
                  </div>
                </div>
              </div>

              {/* بخش دکمه‌ها */}
              <div className="flex items-center gap-2 w-full md:w-auto justify-end">
                <button
                  onClick={() => handleSelect(athlete)}
                  className="btn-glass bg-sky-500/10 hover:bg-sky-500 hover:text-white text-sky-600 dark:text-sky-400 border border-sky-500/20 text-sm flex-1 md:flex-none"
                >
                  مدیریت برنامه
                </button>
                <button
                  onClick={() => router.push(`/dashboard/athletes/${athlete.id}/edit`)}
                  className="p-2 rounded-lg bg-[var(--text-primary)]/5 hover:bg-[var(--text-primary)]/10 text-[var(--text-secondary)] transition"
                  title="ویرایش"
                >
                  <Edit size={18} />
                </button>
                <button
                  onClick={() => router.push(`/dashboard/athletes/${athlete.id}/print`)}
                  className="p-2 rounded-lg bg-[var(--text-primary)]/5 hover:bg-[var(--text-primary)]/10 text-[var(--text-secondary)] transition"
                  title="چاپ"
                >
                  <Printer size={18} />
                </button>
                <button
                  onClick={() => handleDelete(athlete.id, athlete.name)}
                  disabled={deleteMutation.isPending}
                  className="p-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-500 transition disabled:opacity-50"
                  title="حذف"
                >
                  {deleteMutation.isPending ? (
                    <Loader2 size={18} className="animate-spin" />
                  ) : (
                    <Trash2 size={18} />
                  )}
                </button>
              </div>
            </div>
          );
        })}

        {filteredAthletes.length === 0 && (
          <div className="text-center py-10 opacity-50">موردی یافت نشد.</div>
        )}
      </div>
    </div>
  );
}

