'use client';

import { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { UserModal } from '@/components/user-modal';
import { Loader2 } from 'lucide-react';
import type { Athlete } from '@/types';

export default function EditAthletePage() {
  const params = useParams();
  const router = useRouter();
  const athleteId = parseInt(params.id as string);
  const [isOpen, setIsOpen] = useState(true);

  const { data: athlete, isLoading } = useQuery<Athlete>({
    queryKey: ['athlete', athleteId],
    queryFn: () => apiClient.getAthlete(athleteId),
    enabled: !!athleteId,
  });

  const handleClose = () => {
    setIsOpen(false);
    router.push(`/dashboard/athletes/${athleteId}`);
  };

  const handleSave = (updatedAthlete: Athlete) => {
    router.push(`/dashboard/athletes/${updatedAthlete.id}`);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loader2 className="w-8 h-8 animate-spin text-sky-500" />
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
    <UserModal
      isOpen={isOpen}
      onClose={handleClose}
      onSave={handleSave}
      initialData={athlete}
    />
  );
}

