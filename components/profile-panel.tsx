'use client';

import { useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js';
import { Plus } from 'lucide-react';
import { toast } from 'react-hot-toast';
import type { Athlete, Measurement, MeasurementCreate } from '@/types';
import { apiClient } from '@/lib/api-client';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

interface ProfilePanelProps {
  athlete: Athlete;
  onAthleteUpdate?: (athlete: Athlete) => void;
}

export function ProfilePanel({ athlete, onAthleteUpdate }: ProfilePanelProps) {
  const [progressForm, setProgressForm] = useState({
    date: new Date().toISOString().slice(0, 10),
    weight: '',
    bf: '',
    note: '',
  });

  const [measurements, setMeasurements] = useState<Measurement[]>([]);
  const [loading, setLoading] = useState(false);

  const handleAddProgress = async () => {
    if (!progressForm.date || !progressForm.weight) {
      toast.error('تاریخ و وزن الزامی است');
      return;
    }

    const measurementData: MeasurementCreate = {
      recorded_at: progressForm.date,
      weight: parseFloat(progressForm.weight),
      body_fat: progressForm.bf ? parseFloat(progressForm.bf) : undefined,
      notes: progressForm.note || undefined,
    };

    try {
      setLoading(true);
      // TODO: Call API to create measurement
      // await apiClient.createMeasurement(athlete.id, measurementData);
      // await loadMeasurements();
      toast.success('رکورد پیشرفت ثبت شد');
      setProgressForm(prev => ({ ...prev, weight: '', bf: '', note: '' }));
    } catch (error) {
      toast.error('خطا در ثبت پیشرفت');
    } finally {
      setLoading(false);
    }
  };

  // Mock data for now - باید از API لود شود
  const progList = measurements.map(m => ({
    date: m.recorded_at,
    weight: m.weight?.toString() || '',
    bf: m.body_fat?.toString() || '',
    note: m.notes || '',
  }));

  const sortedProg = [...progList].sort((a, b) => (a.date || '').localeCompare(b.date || ''));
  
  const chartData = {
    labels: sortedProg.map(p => p.date),
    datasets: [
      {
        label: 'وزن (kg)',
        data: sortedProg.map(p => Number(p.weight) || null),
        borderColor: '#38bdf8',
        backgroundColor: 'rgba(56,189,248,0.25)',
        tension: 0.3,
      },
    ],
  };

  const chartOptions = {
    plugins: {
      legend: { display: false },
    },
    scales: {
      x: { grid: { display: false } },
      y: { grid: { color: 'rgba(148,163,184,0.2)' } },
    },
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="glass-panel p-6 rounded-3xl">
          <h3 className="font-bold text-lg text-[var(--text-primary)] mb-4">مشخصات پایه</h3>
          <div className="space-y-2 text-sm text-[var(--text-secondary)]">
            <div><span className="font-bold text-[var(--text-primary)]">نام:</span> {athlete.name}</div>
            <div><span className="font-bold text-[var(--text-primary)]">سن:</span> {athlete.age || '-'}</div>
            <div><span className="font-bold text-[var(--text-primary)]">قد:</span> {athlete.height || '-'} cm</div>
            <div><span className="font-bold text-[var(--text-primary)]">وزن فعلی:</span> {athlete.weight || '-'} kg</div>
            <div><span className="font-bold text-[var(--text-primary)]">شغل:</span> {athlete.job || '-'}</div>
          </div>
        </div>

        <div className="lg:col-span-2 glass-panel p-6 rounded-3xl">
          <h3 className="font-bold text-lg text-[var(--text-primary)] mb-4">نمودار پیشرفت وزن</h3>
          {sortedProg.length === 0 ? (
            <div className="text-sm text-[var(--text-secondary)] opacity-60">
              هنوز رکوردی ثبت نشده است.
            </div>
          ) : (
            <div className="h-64">
              <Line data={chartData} options={chartOptions} />
            </div>
          )}
        </div>
      </div>

      <div className="glass-panel p-6 rounded-3xl">
        <div className="flex flex-col md:flex-row gap-4 md:items-end">
          <div className="space-y-1">
            <label className="text-xs text-slate-500 block">تاریخ</label>
            <input
              type="date"
              className="input-glass"
              value={progressForm.date}
              onChange={e => setProgressForm({ ...progressForm, date: e.target.value })}
            />
          </div>
          <div className="space-y-1">
            <label className="text-xs text-slate-500 block">وزن (kg)</label>
            <input
              type="number"
              className="input-glass"
              value={progressForm.weight}
              onChange={e => setProgressForm({ ...progressForm, weight: e.target.value })}
            />
          </div>
          <div className="space-y-1">
            <label className="text-xs text-slate-500 block">درصد چربی بدن (اختیاری)</label>
            <input
              type="number"
              className="input-glass"
              value={progressForm.bf}
              onChange={e => setProgressForm({ ...progressForm, bf: e.target.value })}
            />
          </div>
          <div className="flex-1 space-y-1">
            <label className="text-xs text-slate-500 block">یادداشت کوتاه</label>
            <input
              className="input-glass"
              value={progressForm.note}
              onChange={e => setProgressForm({ ...progressForm, note: e.target.value })}
              placeholder="مثال: پایان فاز کات، شروع حجم..."
            />
          </div>
          <button
            onClick={handleAddProgress}
            disabled={loading}
            className="btn-glass bg-sky-600 hover:bg-sky-500 text-white px-6 py-3 font-bold flex items-center gap-2 disabled:opacity-50"
          >
            <Plus size={18} /> ثبت پیشرفت
          </button>
        </div>
      </div>

      <div className="glass-panel rounded-3xl overflow-hidden">
        <table className="w-full text-right text-sm">
          <thead className="bg-[var(--text-primary)]/5 text-[var(--text-secondary)] text-xs border-b border-[var(--glass-border)]">
            <tr>
              <th className="p-3">تاریخ</th>
              <th className="p-3 text-center">وزن</th>
              <th className="p-3 text-center">% چربی</th>
              <th className="p-3">یادداشت</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[var(--glass-border)]">
            {sortedProg.map((p, idx) => (
              <tr key={idx} className="hover:bg-[var(--text-primary)]/5">
                <td className="p-3">{p.date}</td>
                <td className="p-3 text-center">{p.weight}</td>
                <td className="p-3 text-center">{p.bf || '-'}</td>
                <td className="p-3 text-[var(--text-secondary)] text-xs">{p.note || '-'}</td>
              </tr>
            ))}
            {sortedProg.length === 0 && (
              <tr>
                <td colSpan={4} className="p-6 text-center text-[var(--text-secondary)] opacity-60">
                  هنوز هیچ رکورد پیشرفتی برای این شاگرد ثبت نشده است.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
