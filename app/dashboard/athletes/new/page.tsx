'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { UserModal } from '@/components/user-modal';
import type { Athlete } from '@/types';

export default function NewAthletePage() {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(true);

  const handleClose = () => {
    setIsOpen(false);
    router.push('/dashboard');
  };

  const handleSave = (athlete: Athlete) => {
    router.push(`/dashboard/athletes/${athlete.id}`);
  };

  return (
    <UserModal
      isOpen={isOpen}
      onClose={handleClose}
      onSave={handleSave}
      initialData={null}
    />
  );
}

