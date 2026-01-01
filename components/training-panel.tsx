'use client';

import { useState, useEffect } from 'react';
import { resistanceExercises, riskyExercises } from '@/data/resistanceExercises';
import { correctiveExercises } from '@/data/correctiveExercises';
import { cardioExercises } from '@/data/cardioExercises';
import { warmupExercises, cooldownExercises } from '@/data/warmupCooldown';
import { Save, FolderOpen, AlertTriangle, Plus, GripVertical, Trash2, Search, Loader2 } from 'lucide-react';
import { toast } from 'react-hot-toast';
import Swal from 'sweetalert2';
import { apiClient } from '@/lib/api-client';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { arrayMove, SortableContext, sortableKeyboardCoordinates, useSortable, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import type { Athlete, TrainingPlan, WorkoutItem as WorkoutItemType, TrainingDay } from '@/types';
import { useAppStore } from '@/store/app-store';

interface SortableRowProps {
  item: {
    id?: number;
    type: string;
    name: string;
    name2?: string;
    name3?: string;
    sets?: number;
    reps?: string;
    duration?: number;
    rest?: number;
    restUnit?: string;
    note?: string;
    intensity?: string;
    mode?: string;
  };
  idx: number;
  day: number;
  onDelete: () => void;
}

const SortableRow = ({ item, idx, day, onDelete }: SortableRowProps) => {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({ id: `${day}-${idx}` });
  
  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
    zIndex: isDragging ? 1000 : 1,
  };

  return (
    <tr ref={setNodeRef} style={style} className="hover:bg-[var(--text-primary)]/5 transition group">
      <td className="p-2 text-center">
        <button {...attributes} {...listeners} className="cursor-grab active:cursor-grabbing p-1 hover:bg-[var(--text-primary)]/10 rounded">
          <GripVertical size={16} className="text-[var(--text-secondary)]" />
        </button>
      </td>
      <td className="p-4 align-top">
        <div className="flex items-center gap-2">
          <span className={`text-[10px] px-2 py-0.5 rounded font-bold ${
            item.type === 'cardio' ? 'bg-green-500/20 text-green-500' :
            item.type === 'corrective' ? 'bg-purple-500/20 text-purple-500' :
            item.type === 'warmup' ? 'bg-orange-500/20 text-orange-500' :
            item.type === 'cooldown' ? 'bg-blue-500/20 text-blue-500' :
            'bg-sky-500/20 text-sky-500'
          }`}>
            {item.type === 'cardio' ? 'هوازی' : 
             item.type === 'corrective' ? 'اصلاحی' : 
             item.type === 'warmup' ? 'گرم کردن' :
             item.type === 'cooldown' ? 'سرد کردن' :
             item.type?.toUpperCase() || 'NORMAL'}
          </span>
        </div>
        <div className="font-bold text-[var(--text-primary)] mt-1">{item.name}</div>
        {item.name2 && <div className="text-xs text-sky-500 mt-1">+ {item.name2}</div>}
        {item.name3 && <div className="text-xs text-orange-500 mt-1">+ {item.name3}</div>}
        {item.note && <div className="text-[10px] text-[var(--text-secondary)] mt-1 bg-[var(--text-primary)]/5 p-1 rounded inline-block">{item.note}</div>}
      </td>
      <td className="p-4 text-center text-[var(--text-primary)] font-mono">{item.sets || '-'}</td>
      <td className="p-4 text-center text-[var(--text-primary)] font-mono">{item.mode === 'cardio' ? `${item.duration} min` : item.reps}</td>
      <td className="p-4 text-center text-[var(--text-secondary)] text-xs">
        {item.rest ? `${item.rest} ${item.restUnit === 'm' ? 'دقیقه' : 'ثانیه'}` : '-'}
      </td>
      <td className="p-4 text-center">
        <button onClick={onDelete} className="text-red-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition p-1 hover:bg-red-500/10 rounded">
          <Trash2 size={16} />
        </button>
      </td>
    </tr>
  );
};

interface TrainingPanelProps {
  athlete: Athlete;
}

export function TrainingPanel({ athlete }: TrainingPanelProps) {
  const { theme } = useAppStore();
  const [day, setDay] = useState(1);
  const [mode, setMode] = useState<'resist' | 'cardio' | 'corrective' | 'warmup' | 'cooldown'>('resist');
  const [searchTerm, setSearchTerm] = useState('');
  const [activePlan, setActivePlan] = useState<TrainingPlan | null>(null);
  const [loading, setLoading] = useState(false);
  
  const initialFormState = {
    system: 'normal', muscle: '', subMuscle: '', ex1: '', ex2: '', name3: '', name4: '', sets: '3', reps: '10', 
    rest: '60', restUnit: 's' as 's' | 'm', note: '',
    cCategory: '', cType: '', cTime: '', cInt: '', cIntensity: '', corrEx: '', corrType: '',
    dropCount: '', restPauseTime: '', tempo: '', holdTime: '',
    warmupType: '', cooldownType: ''
  };

  const [formData, setFormData] = useState(initialFormState);
  const [subMuscles, setSubMuscles] = useState<string[]>([]);
  const [exercises, setExercises] = useState<string[]>([]);
  const [corrExercisesList, setCorrExercisesList] = useState<string[]>([]);
  const [warning, setWarning] = useState<string | null>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 8 } }),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
  );

  useEffect(() => {
    if (formData.muscle && resistanceExercises[formData.muscle]) {
      setSubMuscles(Object.keys(resistanceExercises[formData.muscle]));
    } else setSubMuscles([]);
  }, [formData.muscle]);

  useEffect(() => {
    if (formData.subMuscle && formData.muscle && resistanceExercises[formData.muscle]) {
      setExercises(resistanceExercises[formData.muscle][formData.subMuscle] || []);
    } else setExercises([]);
  }, [formData.subMuscle, formData.muscle]);

  useEffect(() => {
    if (formData.corrType) setCorrExercisesList(correctiveExercises[formData.corrType] || []);
  }, [formData.corrType]);

  useEffect(() => {
    if (mode === 'resist' && formData.ex1 && athlete.injuries?.length) {
      let conflict: string | null = null;
      athlete.injuries.forEach((injury: any) => {
        const injuryName = typeof injury === 'string' ? injury : injury.body_part || '';
        if (riskyExercises[injuryName]?.includes(formData.ex1)) {
          conflict = `هشدار: مضر برای "${injuryName}"`;
        }
      });
      setWarning(conflict);
    } else setWarning(null);
  }, [formData.ex1, athlete.injuries, mode]);

  useEffect(() => {
    setFormData(prev => ({
      ...initialFormState,
      rest: prev.rest,
      restUnit: prev.restUnit,
    }));
    setSubMuscles([]);
    setExercises([]);
    setCorrExercisesList([]);
    setSearchTerm('');
  }, [mode]);

  useEffect(() => {
    if (athlete?.id) {
      loadTrainingPlan();
    }
  }, [athlete?.id]);

  const loadTrainingPlan = async () => {
    try {
      setLoading(true);
      const plan = await apiClient.getActiveTrainingPlan(athlete.id);
      setActivePlan(plan);
    } catch (error: any) {
      if (error.response?.status === 404) {
        try {
          const newPlan = await apiClient.createTrainingPlan({
            athlete_id: athlete.id,
            name: 'برنامه تمرینی',
            days: Array.from({ length: 7 }, (_, i) => ({
              day_number: i + 1,
              workout_items: [],
            })),
          });
          setActivePlan(newPlan);
        } catch (createError) {
          console.error('Error creating training plan:', createError);
        }
      }
    } finally {
      setLoading(false);
    }
  };

  const filteredExercises = searchTerm 
    ? exercises.filter(ex => ex.toLowerCase().includes(searchTerm.toLowerCase()))
    : exercises;

  const handleDragEnd = async (event: any) => {
    const { active, over } = event;
    if (!over || active.id === over.id || !activePlan) return;

    const currentDayObj = activePlan.days?.find((d: TrainingDay) => d.day_number === day);
    if (!currentDayObj) return;

    const oldIndex = parseInt(String(active.id).split('-')[1]);
    const newIndex = parseInt(String(over.id).split('-')[1]);
    const items = currentDayObj.workout_items || [];
    const newItems = arrayMove(items, oldIndex, newIndex);
    const itemIds = newItems.map((item: WorkoutItemType) => item.id).filter(Boolean) as number[];

    if (itemIds.length > 0) {
      try {
        await apiClient.reorderWorkoutItems(currentDayObj.id, itemIds);
        await loadTrainingPlan();
      } catch (error) {
        toast.error('خطا در تغییر ترتیب');
      }
    }
  };

  const handleDeleteExercise = async (itemId: number) => {
    try {
      await apiClient.deleteWorkoutItem(itemId);
      await loadTrainingPlan();
      toast.success('حرکت حذف شد');
    } catch (error) {
      toast.error('خطا در حذف حرکت');
    }
  };

  const handleAddExercise = async () => {
    if (!activePlan) {
      toast.error('لطفا صبر کنید تا برنامه بارگذاری شود');
      return;
    }

    const currentDayObj = activePlan.days?.find((d: TrainingDay) => d.day_number === day);
    if (!currentDayObj) {
      toast.error('روز تمرینی یافت نشد');
      return;
    }

    let itemData: any = {
      order: currentDayObj.workout_items?.length || 0,
      set_type: formData.system === 'normal' ? 'normal' : formData.system,
      notes: formData.note || undefined,
      rest_seconds: formData.rest ? parseInt(formData.rest) : undefined,
    };

    if (mode === 'resist') {
      if (!formData.ex1) return toast.error('لطفا حرکت را انتخاب کنید');
      if (!formData.sets || !formData.reps) return toast.error('ست و تکرار الزامی است');
      itemData.custom_name = formData.ex1;
      itemData.sets = parseInt(formData.sets);
      itemData.reps = formData.reps;
      if (formData.ex2) itemData.secondary_exercise_name = formData.ex2;
      if (formData.name3) itemData.tertiary_exercise_name = formData.name3;
    } else if (mode === 'cardio') {
      if (!formData.cType || !formData.cTime) return toast.error('نوع تمرین و مدت زمان الزامی است');
      itemData.custom_name = formData.cType;
      itemData.duration_minutes = parseInt(formData.cTime);
      itemData.intensity = formData.cIntensity || undefined;
    } else if (mode === 'corrective') {
      if (!formData.corrEx) return toast.error('حرکت اصلاحی الزامی است');
      itemData.custom_name = formData.corrEx;
      itemData.sets = parseInt(formData.sets) || undefined;
      itemData.reps = formData.reps || undefined;
    } else if (mode === 'warmup') {
      if (!formData.warmupType) return toast.error('نوع گرم کردن را انتخاب کنید');
      itemData.custom_name = formData.warmupType;
      itemData.duration_minutes = parseInt(formData.cTime) || 5;
    } else if (mode === 'cooldown') {
      if (!formData.cooldownType) return toast.error('نوع سرد کردن را انتخاب کنید');
      itemData.custom_name = formData.cooldownType;
      itemData.duration_minutes = parseInt(formData.cTime) || 5;
    }

    try {
      await apiClient.addWorkoutItem(currentDayObj.id, itemData);
      await loadTrainingPlan();
      toast.success('ثبت شد');
      setFormData({
        ...initialFormState,
        rest: formData.rest,
        restUnit: formData.restUnit,
      });
    } catch (error) {
      toast.error('خطا در ثبت حرکت');
    }
  };

  const currentDayObj = activePlan?.days?.find((d: TrainingDay) => d.day_number === day);
  const workoutItems = currentDayObj?.workout_items?.map((item: WorkoutItemType) => ({
    id: item.id,
    type: item.set_type || 'normal',
    name: item.custom_name || item.exercise?.name || '',
    name2: item.secondary_exercise_name,
    name3: item.tertiary_exercise_name,
    sets: item.sets,
    reps: item.reps,
    duration: item.duration_minutes,
    rest: item.rest_seconds,
    restUnit: 's' as const,
    note: item.notes,
    intensity: item.intensity,
    mode: item.duration_minutes ? 'cardio' : 'resist',
  })) || [];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loader2 className="w-8 h-8 animate-spin text-sky-500" />
      </div>
    );
  }

  if (!activePlan) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-400">
        <p className="text-lg mb-4">خطا در بارگذاری برنامه تمرینی</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="glass-panel p-3 rounded-2xl flex justify-between items-center overflow-x-auto">
        <div className="flex gap-2">
          {[1, 2, 3, 4, 5, 6, 7].map(d => {
            const dayWorkouts = activePlan.days?.find((dd: TrainingDay) => dd.day_number === d)?.workout_items || [];
            return (
              <button 
                key={d} 
                onClick={() => setDay(d)} 
                className={`px-4 py-2 rounded-xl text-sm font-bold whitespace-nowrap transition-all ${
                  day === d 
                    ? 'bg-sky-600 text-white shadow-lg' 
                    : 'bg-[var(--glass-bg)] text-[var(--text-secondary)] hover:bg-[var(--text-primary)]/10'
                }`}
              >
                جلسه {d}
                {dayWorkouts.length > 0 && (
                  <span className="mr-1 text-[10px] bg-white/20 px-1.5 rounded-full">{dayWorkouts.length}</span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-4 space-y-6">
          <div className="glass-panel p-5 rounded-3xl sticky top-6">
            <div className="flex justify-between mb-4 bg-[var(--input-bg)] p-1 rounded-xl">
              {(['warmup', 'resist', 'cardio', 'corrective', 'cooldown'] as const).map(m => (
                <button key={m} onClick={() => setMode(m)} className={`flex-1 text-[10px] font-bold py-2 rounded-lg transition ${mode === m ? 'bg-sky-600 text-white shadow-md' : 'text-[var(--text-secondary)]'}`}>
                  {m === 'warmup' ? '🔥 گرم' : m === 'resist' ? '💪 مقاومتی' : m === 'cardio' ? '🏃 هوازی' : m === 'corrective' ? '🩹 اصلاحی' : '❄️ سرد'}
                </button>
              ))}
            </div>

            <div className="space-y-3">
              {mode === 'warmup' && (
                <>
                  <select className="input-glass font-bold" value={formData.warmupType} onChange={e => setFormData({ ...formData, warmupType: e.target.value })}>
                    <option value="">انتخاب نوع گرم کردن...</option>
                    {warmupExercises.map(ex => <option key={ex} value={ex}>{ex}</option>)}
                  </select>
                  <input className="input-glass" type="number" placeholder="مدت زمان (دقیقه)" value={formData.cTime} onChange={e => setFormData({ ...formData, cTime: e.target.value })} />
                </>
              )}

              {mode === 'cooldown' && (
                <>
                  <select className="input-glass font-bold" value={formData.cooldownType} onChange={e => setFormData({ ...formData, cooldownType: e.target.value })}>
                    <option value="">انتخاب نوع سرد کردن...</option>
                    {cooldownExercises.map(ex => <option key={ex} value={ex}>{ex}</option>)}
                  </select>
                  <input className="input-glass" type="number" placeholder="مدت زمان (دقیقه)" value={formData.cTime} onChange={e => setFormData({ ...formData, cTime: e.target.value })} />
                </>
              )}

              {mode === 'resist' && (
                <>
                  <select className="input-glass" value={formData.system} onChange={e => setFormData({ ...formData, system: e.target.value })}>
                    <option value="normal">سیستم ساده (Straight Set)</option>
                    <option value="superset">سوپرست (۲ حرکت پشت‌سرهم)</option>
                    <option value="triset">تری‌ست (۳ حرکت)</option>
                    <option value="giantset">جاینت‌ست (۴+ حرکت)</option>
                    <option value="dropset">درآپ‌ست (Drop Set)</option>
                    <option value="pyramid">هرمی (Pyramid)</option>
                    <option value="restpause">رست-پاز (Rest-Pause)</option>
                    <option value="german-volume">حجم آلمانی (10x10)</option>
                    <option value="fst7">FST-7</option>
                    <option value="5x5">5x5 (Stronglifts)</option>
                    <option value="cluster">کلاستر ست</option>
                    <option value="myorep">مایورپ (Myo-Reps)</option>
                    <option value="tempo">تمپو (Tempo)</option>
                    <option value="isometric">ایزومتریک</option>
                    <option value="negatives">نگاتیو</option>
                    <option value="21s">21s</option>
                  </select>
                  
                  <div className="grid grid-cols-2 gap-2">
                    <select className="input-glass text-xs" value={formData.muscle} onChange={e => setFormData({ ...formData, muscle: e.target.value, subMuscle: '' })}>
                      <option value="">عضله...</option>
                      {Object.keys(resistanceExercises).map(m => <option key={m} value={m}>{m}</option>)}
                    </select>
                    <select className="input-glass text-xs" value={formData.subMuscle} onChange={e => setFormData({ ...formData, subMuscle: e.target.value })}>
                      <option value="">ناحیه...</option>
                      {subMuscles.map(s => <option key={s} value={s}>{s}</option>)}
                    </select>
                  </div>

                  {exercises.length > 10 && (
                    <div className="relative">
                      <input
                        type="text"
                        className="input-glass pl-8 text-sm"
                        placeholder="جستجوی حرکت..."
                        value={searchTerm}
                        onChange={e => setSearchTerm(e.target.value)}
                      />
                      <Search size={14} className="absolute left-3 top-3.5 text-slate-400" />
                    </div>
                  )}

                  <select className="input-glass font-bold text-sky-600 dark:text-sky-400" value={formData.ex1} onChange={e => setFormData({ ...formData, ex1: e.target.value })}>
                    <option value="">انتخاب حرکت...</option>
                    {filteredExercises.map(e => <option key={e} value={e}>{e}</option>)}
                  </select>

                  {['superset', 'triset', 'giantset'].includes(formData.system) && (
                    <>
                      <input className="input-glass border-r-4 border-r-yellow-400" placeholder="+ حرکت دوم" value={formData.ex2} onChange={e => setFormData({ ...formData, ex2: e.target.value })} />
                      {['triset', 'giantset'].includes(formData.system) && (
                        <input className="input-glass border-r-4 border-r-orange-400" placeholder="+ حرکت سوم" value={formData.name3} onChange={e => setFormData({ ...formData, name3: e.target.value })} />
                      )}
                    </>
                  )}

                  {warning && (
                    <div className="bg-red-500/10 border border-red-500/30 p-2 rounded-lg flex items-center gap-2 text-red-500 text-xs animate-pulse">
                      <AlertTriangle size={14} /> {warning}
                    </div>
                  )}

                  <div className="grid grid-cols-3 gap-2">
                    <input className="input-glass text-center px-1" placeholder="ست" value={formData.sets} onChange={e => setFormData({ ...formData, sets: e.target.value })} />
                    <input className="input-glass text-center px-1 col-span-2" placeholder="تکرار" value={formData.reps} onChange={e => setFormData({ ...formData, reps: e.target.value })} />
                  </div>
                </>
              )}

              {mode === 'cardio' && (
                <>
                  <select className="input-glass" value={formData.cCategory} onChange={e => setFormData({ ...formData, cCategory: e.target.value, cType: '' })}>
                    <option value="">انتخاب دسته...</option>
                    {Object.keys(cardioExercises).map(cat => <option key={cat} value={cat}>{cat}</option>)}
                  </select>
                  {formData.cCategory && (
                    <select className="input-glass font-bold" value={formData.cType} onChange={e => setFormData({ ...formData, cType: e.target.value })}>
                      <option value="">انتخاب نوع...</option>
                      {cardioExercises[formData.cCategory]?.map(ex => <option key={ex} value={ex}>{ex}</option>)}
                    </select>
                  )}
                  <input className="input-glass" placeholder="زمان (دقیقه)" type="number" value={formData.cTime} onChange={e => setFormData({ ...formData, cTime: e.target.value })} />
                  <select className="input-glass" value={formData.cIntensity} onChange={e => setFormData({ ...formData, cIntensity: e.target.value })}>
                    <option value="">سطح شدت...</option>
                    <option value="low">سبک (50-60%)</option>
                    <option value="moderate">متوسط (60-70%)</option>
                    <option value="high">سنگین (70-85%)</option>
                    <option value="very-high">خیلی سنگین (85%+)</option>
                  </select>
                </>
              )}

              {mode === 'corrective' && (
                <>
                  <select className="input-glass" value={formData.corrType} onChange={e => setFormData({ ...formData, corrType: e.target.value })}>
                    <option value="">نوع ناهنجاری...</option>
                    {Object.keys(correctiveExercises).map(k => <option key={k} value={k}>{k}</option>)}
                  </select>
                  <select className="input-glass" value={formData.corrEx} onChange={e => setFormData({ ...formData, corrEx: e.target.value })}>
                    <option value="">حرکت...</option>
                    {corrExercisesList.map(e => <option key={e} value={e}>{e}</option>)}
                  </select>
                  <input className="input-glass" placeholder="تکرار/زمان" value={formData.reps} onChange={e => setFormData({ ...formData, reps: e.target.value })} />
                </>
              )}

              {(mode === 'resist' || mode === 'corrective') && (
                <div className="flex gap-2">
                  <input className="input-glass flex-1 text-center" placeholder="استراحت" type="number" value={formData.rest} onChange={e => setFormData({ ...formData, rest: e.target.value })} />
                  <select className="input-glass w-24 text-center" value={formData.restUnit} onChange={e => setFormData({ ...formData, restUnit: e.target.value as 's' | 'm' })}>
                    <option value="s">ثانیه</option>
                    <option value="m">دقیقه</option>
                  </select>
                </div>
              )}

              <input className="input-glass" placeholder="توضیحات فنی" value={formData.note} onChange={e => setFormData({ ...formData, note: e.target.value })} />
            </div>
            
            <button onClick={handleAddExercise} className="w-full btn-glass bg-sky-600 hover:bg-sky-500 text-white mt-4">
              <Plus size={18} /> ثبت در برنامه
            </button>
          </div>
        </div>

        <div className="lg:col-span-8 glass-panel rounded-3xl p-0 overflow-hidden min-h-[500px]">
          <div className="bg-[var(--text-primary)]/5 px-4 py-3 border-b border-[var(--glass-border)] flex justify-between items-center">
            <span className="text-sm font-bold text-[var(--text-primary)]">برنامه جلسه {day}</span>
            <span className="text-xs text-[var(--text-secondary)]">{workoutItems.length} حرکت</span>
          </div>
          
          <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
            <table className="w-full text-right text-sm">
              <thead className="bg-[var(--text-primary)]/5 text-[var(--text-secondary)] text-xs border-b border-[var(--glass-border)]">
                <tr>
                  <th className="p-2 w-10"></th>
                  <th className="p-4">شرح حرکت</th>
                  <th className="p-4 w-16 text-center">ست</th>
                  <th className="p-4 w-20 text-center">تکرار</th>
                  <th className="p-4 w-20 text-center">استراحت</th>
                  <th className="p-4 w-10"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--glass-border)]">
                <SortableContext items={workoutItems.map((item, idx) => `item-${item.id || idx}`)} strategy={verticalListSortingStrategy}>
                  {workoutItems.map((item, idx) => (
                    <SortableRow
                      key={item.id || idx}
                      item={item}
                      idx={idx}
                      day={day}
                      onDelete={() => handleDeleteExercise(item.id!)}
                    />
                  ))}
                </SortableContext>
                {workoutItems.length === 0 && (
                  <tr>
                    <td colSpan={6} className="p-10 text-center text-[var(--text-secondary)] opacity-50">
                      حرکتی ثبت نشده است. از فرم سمت راست استفاده کنید.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </DndContext>
        </div>
      </div>
    </div>
  );
}

