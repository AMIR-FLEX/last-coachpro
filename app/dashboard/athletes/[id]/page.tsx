'use client';

import { useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { TrainingPanel } from '@/components/training-panel';
import { DietPanel } from '@/components/diet-panel';
import { SupplementsPanel } from '@/components/supplements-panel';
import { ProfilePanel } from '@/components/profile-panel';
import { useAppStore } from '@/store/app-store';
import type { Athlete } from '@/types';

export default function AthleteDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { currentTab, setActiveAthlete } = useAppStore();
  const athleteId = parseInt(params.id as string);

  const { data: athlete, isLoading } = useQuery<Athlete>({
    queryKey: ['athlete', athleteId],
    queryFn: () => apiClient.getAthlete(athleteId),
    enabled: !!athleteId,
  });

  useEffect(() => {
    if (athlete) {
      setActiveAthlete(athlete);
    }
  }, [athlete, setActiveAthlete]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-sky-500"></div>
      </div>
    );
  }

  if (!athlete) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-400">
        <p className="text-lg mb-4">شاگرد یافت نشد</p>
        <button
          onClick={() => router.push('/dashboard')}
          className="btn-glass bg-sky-600 hover:bg-sky-500 text-white"
        >
          بازگشت به لیست
        </button>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      {currentTab === 'training' && <TrainingPanel athlete={athlete} />}
      {currentTab === 'nutrition' && <DietPanel athlete={athlete} />}
      {currentTab === 'supplements' && <SupplementsPanel athlete={athlete} />}
      {currentTab === 'progress' && <ProfilePanel athlete={athlete} />}
    </div>
  );
}

