'use client';

import { useState, useEffect } from 'react';
import { supplementsData } from '@/data/supplementsData';
import { toast } from 'react-hot-toast';
import Swal from 'sweetalert2';
import { apiClient } from '@/lib/api-client';
import { Loader2 } from 'lucide-react';
import type { Athlete, SupplementPlan } from '@/types';
import { useAppStore } from '@/store/app-store';

interface SupplementsPanelProps {
  athlete: Athlete;
}

export function SupplementsPanel({ athlete }: SupplementsPanelProps) {
  const { theme } = useAppStore();
  const [formData, setFormData] = useState({ name: '', dose: '', time: '', note: '' });
  const [activePlan, setActivePlan] = useState<SupplementPlan | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (athlete?.id) {
      loadSupplementPlan();
    }
  }, [athlete?.id]);

  const loadSupplementPlan = async () => {
    try {
      setLoading(true);
      const plan = await apiClient.getActiveSupplementPlan(athlete.id);
      setActivePlan(plan);
    } catch (error: any) {
      if (error.response?.status === 404) {
        try {
          const newPlan = await apiClient.createSupplementPlan({
            athlete_id: athlete.id,
            name: 'نسخه مکمل',
            items: [],
          });
          setActivePlan(newPlan);
        } catch (createError) {
          console.error('Error creating supplement plan:', createError);
        }
      }
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = async () => {
    if (!formData.name || !activePlan) {
      toast.error('نام مکمل را انتخاب کنید');
      return;
    }

    const itemData = {
      custom_name: formData.name,
      dose: formData.dose,
      timing: formData.time,
      notes: formData.note,
      order: activePlan.items?.length || 0,
    };

    try {
      await apiClient.addSupplementItem(activePlan.id, itemData);
      await loadSupplementPlan();
      setFormData({ name: '', dose: '', time: '', note: '' });
      toast.success('مکمل اضافه شد');
    } catch (error) {
      toast.error('خطا در افزودن مکمل');
    }
  };

  const handleDelete = async (itemId: number) => {
    try {
      await apiClient.deleteSupplementItem(itemId);
      await loadSupplementPlan();
      toast.success('مکمل حذف شد');
    } catch (error) {
      toast.error('خطا در حذف مکمل');
    }
  };

  return (
    <div className="space-y-6 animate-fade-in-up">
      <div className="glass-panel p-6 rounded-3xl">
        <h3 className="font-bold text-lg text-[var(--text-primary)] border-b border-[var(--glass-border)] pb-4 mb-6 flex items-center gap-2">
          <span className="w-2 h-6 bg-purple-500 rounded-full"></span>
          تجویز مکمل و دارو
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="text-xs text-slate-400 mb-1 block">نام مکمل</label>
            <div className="flex gap-2">
              <select 
                className="input-glass font-bold" 
                value={formData.name} 
                onChange={e => setFormData({...formData, name: e.target.value})}
              >
                <option value="">انتخاب کنید...</option>
                {supplementsData.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
              <button
                onClick={async () => {
                  const { value: custom } = await Swal.fire({
                    title: 'نام مکمل جدید',
                    input: 'text',
                    inputPlaceholder: 'نام مکمل را وارد کنید...',
                    showCancelButton: true,
                    confirmButtonText: 'افزودن',
                    cancelButtonText: 'لغو',
                    background: theme === 'dark' ? '#1e293b' : '#fff',
                    color: theme === 'dark' ? '#fff' : '#000',
                    inputValidator: (value) => {
                      if (!value) {
                        return 'نام مکمل الزامی است';
                      }
                    }
                  });
                  if (custom) setFormData({ ...formData, name: custom });
                }}
                className="btn-glass bg-white/10 hover:bg-white/20 text-white"
                title="افزودن مکمل سفارشی"
              >
                +
              </button>
            </div>
          </div>
          <div>
            <label className="text-xs text-slate-400 mb-1 block">زمان مصرف</label>
            <select 
              className="input-glass" 
              value={formData.time} 
              onChange={e => setFormData({...formData, time: e.target.value})}
            >
              <option value="">انتخاب...</option>
              <option>ناشتا</option><option>همراه صبحانه</option><option>قبل تمرین</option>
              <option>حین تمرین</option><option>بعد تمرین</option><option>قبل خواب</option>
            </select>
          </div>
          <div>
            <label className="text-xs text-slate-400 mb-1 block">دوز مصرفی</label>
            <input 
              className="input-glass" 
              placeholder="مثال: ۱ اسکوپ / ۵ گرم"
              value={formData.dose}
              onChange={e => setFormData({...formData, dose: e.target.value})}
            />
          </div>
        </div>
        <input 
          className="input-glass mb-4" 
          placeholder="توضیحات تکمیلی (نحوه ترکیب و...)"
          value={formData.note}
          onChange={e => setFormData({...formData, note: e.target.value})}
        />
        <button onClick={handleAdd} className="w-full btn-glass bg-purple-600 hover:bg-purple-500 text-white shadow-lg shadow-purple-500/20 font-bold py-3">
          + ثبت در نسخه
        </button>
      </div>

      <div className="glass-panel rounded-3xl overflow-hidden min-h-[300px]">
        <table className="w-full text-right text-sm">
          <thead className="bg-[var(--text-primary)]/5 text-[var(--text-secondary)] text-xs uppercase font-semibold">
            <tr>
              <th className="p-5">نام مکمل</th>
              <th className="p-5">دوز</th>
              <th className="p-5">زمان</th>
              <th className="p-5">توضیحات</th>
              <th className="p-5 w-10"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[var(--glass-border)]">
            {loading ? (
              <tr>
                <td colSpan={5} className="p-10 text-center">
                  <Loader2 className="w-6 h-6 animate-spin text-sky-500 mx-auto" />
                </td>
              </tr>
            ) : (
              <>
                {activePlan?.items && activePlan.items.map((item) => (
                  <tr key={item.id} className="hover:bg-[var(--text-primary)]/5 transition-colors">
                    <td className="p-5 font-bold text-[var(--text-primary)]">{item.custom_name || item.supplement?.name || 'نامشخص'}</td>
                    <td className="p-5 text-[var(--text-secondary)]">{item.dose || '-'}</td>
                    <td className="p-5 text-purple-400 dark:text-purple-300">{item.timing || '-'}</td>
                    <td className="p-5 text-xs text-[var(--text-secondary)]">{item.notes || item.instructions || '-'}</td>
                    <td className="p-5 text-center">
                      <button onClick={() => handleDelete(item.id)} className="text-red-400 hover:text-red-500 transition">✕</button>
                    </td>
                  </tr>
                ))}
                {(!activePlan?.items || activePlan.items.length === 0) && (
                  <tr><td colSpan={5} className="p-10 text-center text-[var(--text-secondary)] opacity-60">هنوز مکملی تجویز نشده است.</td></tr>
                )}
              </>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
