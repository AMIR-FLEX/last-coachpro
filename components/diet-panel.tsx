'use client';

import { useState, useEffect, useMemo } from 'react';
import { ShoppingBag, GripVertical, Trash2, Search, Copy, Plus, Loader2 } from 'lucide-react';
import { foodData } from '@/data/foodData';
import { toast } from 'react-hot-toast';
import Swal from 'sweetalert2';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { arrayMove, SortableContext, sortableKeyboardCoordinates, useSortable, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { apiClient } from '@/lib/api-client';
import type { Athlete, DietPlan, DietItem } from '@/types';

interface SortableFoodRowProps {
  item: {
    id?: number;
    meal: string;
    name: string;
    amount: number;
    unit: string;
    c: number;
    p: number;
    ch: number;
    f: number;
  };
  idx: number;
  onDelete: () => void;
}

const SortableFoodRow = ({ item, idx, onDelete }: SortableFoodRowProps) => {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({ id: `food-${idx}` });
  
  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <tr ref={setNodeRef} style={style} className="hover:bg-[var(--text-primary)]/5 group">
      <td className="p-2 text-center">
        <button {...attributes} {...listeners} className="cursor-grab active:cursor-grabbing p-1 hover:bg-[var(--text-primary)]/10 rounded">
          <GripVertical size={16} className="text-[var(--text-secondary)]" />
        </button>
      </td>
      <td className="p-4">
        <span className={`text-xs px-2 py-1 rounded-lg font-bold ${
          item.meal === 'صبحانه' ? 'bg-yellow-500/20 text-yellow-600' :
          item.meal === 'ناهار' ? 'bg-orange-500/20 text-orange-600' :
          item.meal === 'شام' ? 'bg-purple-500/20 text-purple-600' :
          'bg-sky-500/20 text-sky-600'
        }`}>
          {item.meal}
        </span>
      </td>
      <td className="p-4 font-bold text-[var(--text-primary)]">{item.name}</td>
      <td className="p-4 text-center text-[var(--text-secondary)]">{item.amount} {item.unit}</td>
      <td className="p-4 text-center font-bold text-emerald-500">{item.c}</td>
      <td className="p-4 text-center text-xs text-[var(--text-secondary)]">
        <span className="text-blue-500">{item.p}p</span> / 
        <span className="text-yellow-500"> {item.ch}c</span> / 
        <span className="text-red-500"> {item.f}f</span>
      </td>
      <td className="p-4 text-center">
        <button onClick={onDelete} className="text-red-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition p-1 hover:bg-red-500/10 rounded">
          <Trash2 size={16} />
        </button>
      </td>
    </tr>
  );
};

interface DietPanelProps {
  athlete: Athlete;
}

export function DietPanel({ athlete }: DietPanelProps) {
  const [meal, setMeal] = useState('صبحانه');
  const [category, setCategory] = useState('');
  const [foodName, setFoodName] = useState('');
  const [amount, setAmount] = useState('');
  const [foodsList, setFoodsList] = useState<string[]>([]);
  const [unit, setUnit] = useState('-');
  const [searchTerm, setSearchTerm] = useState('');
  const [customFood, setCustomFood] = useState({ name: '', cal: '', protein: '', carb: '', fat: '', unit: 'گرم', base: 100 });
  const [activePlan, setActivePlan] = useState<DietPlan | null>(null);
  const [loading, setLoading] = useState(false);
  const [foodCategories, setFoodCategories] = useState<any[]>([]);

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 8 } }),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
  );

  useEffect(() => {
    if (athlete?.id) {
      loadDietPlan();
    }
  }, [athlete?.id]);

  useEffect(() => {
    loadFoodCategories();
  }, []);

  const loadDietPlan = async () => {
    try {
      setLoading(true);
      const plan = await apiClient.getActiveDietPlan(athlete.id);
      setActivePlan(plan);
    } catch (error: any) {
      if (error.response?.status === 404) {
        try {
          const newPlan = await apiClient.createDietPlan({
            athlete_id: athlete.id,
            name: 'برنامه غذایی',
            items: [],
          });
          setActivePlan(newPlan);
        } catch (createError) {
          console.error('Error creating diet plan:', createError);
        }
      }
    } finally {
      setLoading(false);
    }
  };

  const loadFoodCategories = async () => {
    try {
      const categories = await apiClient.getFoodCategories();
      setFoodCategories(categories);
    } catch (error) {
      console.error('Error loading food categories:', error);
    }
  };

  useEffect(() => {
    if (category && foodData[category as keyof typeof foodData]) {
      setFoodsList(Object.keys(foodData[category as keyof typeof foodData]));
    } else {
      setFoodsList([]);
    }
    setFoodName('');
    setUnit('-');
    setSearchTerm('');
  }, [category]);

  useEffect(() => {
    if (category && foodName && foodData[category as keyof typeof foodData]) {
      const categoryData = foodData[category as keyof typeof foodData] as Record<string, any>;
      if (categoryData[foodName]) {
        setUnit(categoryData[foodName].u);
      }
    }
  }, [category, foodName]);

  const filteredFoods = searchTerm 
    ? foodsList.filter(f => f.toLowerCase().includes(searchTerm.toLowerCase()))
    : foodsList;

  const handleDragEnd = async (event: any) => {
    const { active, over } = event;
    if (!over || active.id === over.id || !activePlan) return;

    const oldIndex = parseInt(active.id.split('-')[1]);
    const newIndex = parseInt(over.id.split('-')[1]);
    const items = activePlan.items || [];
    const newItems = arrayMove(items, oldIndex, newIndex);
    const itemIds = newItems.map((item: DietItem) => item.id).filter(Boolean) as number[];

    if (itemIds.length > 0) {
      try {
        await apiClient.reorderDietItems(activePlan.id, itemIds);
        await loadDietPlan();
      } catch (error) {
        toast.error('خطا در تغییر ترتیب');
      }
    }
  };

  const handleDeleteFood = async (itemId: number) => {
    try {
      await apiClient.deleteDietItem(itemId);
      await loadDietPlan();
      toast.success('حذف شد');
    } catch (error) {
      toast.error('خطا در حذف غذا');
    }
  };

  const handleAddFood = async () => {
    if (!foodName || !amount || !activePlan) return toast.error('غذا و مقدار را وارد کنید');
    
    let info: any;
    if (category && foodData[category as keyof typeof foodData]) {
      const categoryData = foodData[category as keyof typeof foodData] as Record<string, any>;
      if (categoryData[foodName]) {
        info = categoryData[foodName];
      }
    }
    
    if (!info) {
      try {
        const foods = await apiClient.searchFoods(foodName);
        if (foods.length > 0) {
          const food = foods[0];
          info = {
            u: food.unit || 'گرم',
            b: food.base_amount || 100,
            c: food.calories || 0,
            p: food.protein || 0,
            ch: food.carbs || 0,
            f: food.fat || 0,
          };
        } else {
          toast.error('غذا یافت نشد');
          return;
        }
      } catch (error) {
        toast.error('خطا در جستجوی غذا');
        return;
      }
    }

    // Calculate macros based on unit type
    // If unit is "عدد" (piece/number), treat amount as count
    // Otherwise, treat as weight in the base unit (grams)
    const isPieceUnit = info.u?.toLowerCase().includes('عدد') || 
                       info.u?.toLowerCase().includes('number') || 
                       info.u?.toLowerCase().includes('piece') ||
                       info.u === 'عدد';
    
    let ratio: number;
    if (isPieceUnit) {
      // For piece units: amount is the count, so ratio = count
      // Base amount (info.b) represents macros per 1 piece
      ratio = parseFloat(amount);
    } else {
      // For weight units: ratio = actual_amount / base_amount
      ratio = parseFloat(amount) / info.b;
    }
    
    const itemData = {
      meal,
      custom_name: foodName,
      amount: parseFloat(amount),
      unit: info.u || 'گرم',
      custom_calories: Math.round(info.c * ratio),
      custom_protein: Math.round(info.p * ratio),
      custom_carbs: Math.round(info.ch * ratio),
      custom_fat: Math.round(info.f * ratio),
      order: activePlan.items?.length || 0,
    };

    try {
      await apiClient.addDietItem(activePlan.id, itemData);
      await loadDietPlan();
      setAmount('');
      toast.success('اضافه شد');
    } catch (error) {
      toast.error('خطا در افزودن غذا');
    }
  };

  const handleAddCustomFood = async () => {
    if (!customFood.name || !customFood.cal || !activePlan) return toast.error('نام و کالری الزامی است');
    
    const itemData = {
      meal,
      custom_name: customFood.name,
      amount: customFood.base,
      unit: customFood.unit,
      custom_calories: parseInt(customFood.cal) || 0,
      custom_protein: parseInt(customFood.protein) || 0,
      custom_carbs: parseInt(customFood.carb) || 0,
      custom_fat: parseInt(customFood.fat) || 0,
      order: activePlan.items?.length || 0,
    };

    try {
      await apiClient.addDietItem(activePlan.id, itemData);
      await loadDietPlan();
      setCustomFood({ name: '', cal: '', protein: '', carb: '', fat: '', unit: 'گرم', base: 100 });
      toast.success('غذای سفارشی اضافه شد');
    } catch (error) {
      toast.error('خطا در افزودن غذای سفارشی');
    }
  };

  const generateShoppingList = () => {
    const items: Record<string, number> = {};
    (activePlan?.items || []).forEach((i: DietItem) => {
      const key = `${i.custom_name || i.food?.name || 'نامشخص'} (${i.unit || 'گرم'})`;
      items[key] = (items[key] || 0) + i.amount;
    });

    if (Object.keys(items).length === 0) {
      toast.error('آیتمی در رژیم برای ساخت لیست خرید وجود ندارد');
      return;
    }

    const lines = Object.keys(items).map(k => `• ${k}: ${Math.round(items[k] * 7)}`);

    Swal.fire({
      title: '🛒 لیست خرید هفتگی',
      html: `<div style="text-align:right;direction:rtl;font-size:13px;max-height:400px;overflow-y:auto">${lines.join('<br/>')}</div>`,
      icon: 'info',
      confirmButtonText: 'متوجه شدم'
    });
  };

  const total = useMemo(() => {
    return (activePlan?.items || []).reduce(
      (acc, i) => ({ 
        c: acc.c + (i.calculated_calories || i.custom_calories || 0), 
        p: acc.p + (i.calculated_protein || i.custom_protein || 0), 
        ch: acc.ch + (i.calculated_carbs || i.custom_carbs || 0), 
        f: acc.f + (i.calculated_fat || i.custom_fat || 0) 
      }),
      { c: 0, p: 0, ch: 0, f: 0 }
    );
  }, [activePlan?.items]);

  const calcBmr = () => {
    const w = parseFloat(String(athlete.weight)) || 0;
    const h = parseFloat(String(athlete.height)) || 0;
    const a = parseFloat(String(athlete.age)) || 0;
    if (!w || !h || !a) return 0;
    const isMale = athlete.gender !== 'female';
    const base = 10 * w + 6.25 * h - 5 * a + (isMale ? 5 : -161);
    return Math.round(base);
  };

  const bmr = calcBmr();
  const activityFactor = parseFloat(String(athlete.activity_level)) || 1.2;
  const tdee = Math.round(bmr * activityFactor) || 0;

  const dietItems = activePlan?.items || [];

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
        <p className="text-lg mb-4">خطا در بارگذاری برنامه غذایی</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* کارت آمار */}
        <div className="glass-panel p-6 rounded-3xl relative overflow-hidden bg-gradient-to-br from-indigo-900 via-slate-900 to-slate-900 border-indigo-500/20 text-white">
          <div className="relative z-10">
            <div className="flex justify-between items-start mb-6">
              <div>
                <div className="text-xs text-indigo-300 uppercase font-bold mb-1">کالری هدف (TDEE)</div>
                <div className="text-4xl font-black text-white">{tdee}</div>
                <div className="text-xs text-slate-400 mt-1">BMR: {bmr} کالری</div>
              </div>
              <div className="text-left">
                <div className="text-xs text-indigo-300 uppercase font-bold mb-1">دریافتی</div>
                <div className={`text-3xl font-bold ${total.c > tdee ? 'text-red-400' : 'text-emerald-400'}`}>{total.c}</div>
                <div className="text-xs text-slate-400 mt-1">
                  {total.c > tdee ? `+${total.c - tdee} اضافه` : `${tdee - total.c} باقی‌مانده`}
                </div>
              </div>
            </div>
            
            <div className="h-3 bg-slate-700 rounded-full overflow-hidden mb-4">
              <div 
                className={`h-full rounded-full transition-all ${total.c > tdee ? 'bg-red-500' : 'bg-emerald-500'}`}
                style={{ width: `${Math.min((total.c / tdee) * 100, 100)}%` }}
              />
            </div>

            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="bg-white/10 rounded-xl p-3">
                <div className="text-blue-400 font-bold text-lg">{total.p}g</div>
                <div className="text-[10px] text-slate-400">پروتئین</div>
              </div>
              <div className="bg-white/10 rounded-xl p-3">
                <div className="text-yellow-400 font-bold text-lg">{total.ch}g</div>
                <div className="text-[10px] text-slate-400">کربوهیدرات</div>
              </div>
              <div className="bg-white/10 rounded-xl p-3">
                <div className="text-red-400 font-bold text-lg">{total.f}g</div>
                <div className="text-[10px] text-slate-400">چربی</div>
              </div>
            </div>
          </div>
        </div>

        {/* فرم افزودن */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-3xl">
          <div className="flex justify-between items-center border-b border-[var(--glass-border)] pb-4 mb-4">
            <h3 className="font-bold text-lg text-[var(--text-primary)]">مدیریت رژیم</h3>
            <div className="flex gap-2">
              <button onClick={generateShoppingList} className="btn-glass bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 text-xs border border-emerald-500/20">
                <ShoppingBag size={14} /> لیست خرید
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-3 mb-4">
            <select className="input-glass font-bold" value={meal} onChange={e => setMeal(e.target.value)}>
              <option>صبحانه</option>
              <option>میان وعده ۱</option>
              <option>ناهار</option>
              <option>میان وعده ۲</option>
              <option>شام</option>
              <option>میان وعده ۳</option>
            </select>
            <select className="input-glass" value={category} onChange={e => setCategory(e.target.value)}>
              <option value="">دسته...</option>
              {Object.keys(foodData).map(c => <option key={c} value={c}>{c}</option>)}
            </select>
            <div className="md:col-span-2">
              {foodsList.length > 15 && (
                <div className="relative mb-2">
                  <input
                    type="text"
                    className="input-glass pl-8 text-sm"
                    placeholder="جستجوی غذا..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                  />
                  <Search size={14} className="absolute left-3 top-3.5 text-slate-400" />
                </div>
              )}
              <select className="input-glass font-bold" value={foodName} onChange={e => setFoodName(e.target.value)}>
                <option value="">غذا...</option>
                {filteredFoods.map(f => <option key={f} value={f}>{f}</option>)}
              </select>
            </div>
          </div>
          <div className="flex gap-3 mb-6">
            <div className="flex-1 relative">
              <input 
                type="number" 
                className="input-glass text-center font-bold" 
                placeholder="مقدار" 
                value={amount} 
                onChange={e => setAmount(e.target.value)}
                min="0"
                step={unit?.toLowerCase().includes('عدد') ? "1" : "0.1"}
              />
              <span className="absolute left-3 top-3 text-xs text-slate-400 font-semibold">
                {unit === '-' ? 'واحد' : unit}
              </span>
              {unit !== '-' && (
                <span className="absolute left-14 top-3 text-[10px] text-slate-500">
                  {unit?.toLowerCase().includes('عدد') ? '(عدد)' : '(گرم)'}
                </span>
              )}
            </div>
            <button onClick={handleAddFood} className="btn-glass bg-emerald-600 hover:bg-emerald-500 text-white px-6">
              <Plus size={16} /> افزودن
            </button>
          </div>

          <div className="border-t border-[var(--glass-border)] pt-4">
            <div className="text-xs text-[var(--text-secondary)] mb-3 font-bold">➕ افزودن غذای سفارشی</div>
            <div className="grid grid-cols-2 md:grid-cols-6 gap-2">
              <input className="input-glass text-sm" placeholder="نام غذا" value={customFood.name} onChange={e => setCustomFood({ ...customFood, name: e.target.value })} />
              <input className="input-glass text-sm text-center" type="number" placeholder="کالری" value={customFood.cal} onChange={e => setCustomFood({ ...customFood, cal: e.target.value })} />
              <input className="input-glass text-sm text-center" type="number" placeholder="پروتئین" value={customFood.protein} onChange={e => setCustomFood({ ...customFood, protein: e.target.value })} />
              <input className="input-glass text-sm text-center" type="number" placeholder="کربو" value={customFood.carb} onChange={e => setCustomFood({ ...customFood, carb: e.target.value })} />
              <input className="input-glass text-sm text-center" type="number" placeholder="چربی" value={customFood.fat} onChange={e => setCustomFood({ ...customFood, fat: e.target.value })} />
              <button onClick={handleAddCustomFood} className="btn-glass bg-sky-600 hover:bg-sky-500 text-white text-sm">ثبت</button>
            </div>
          </div>
        </div>
      </div>

      {/* جدول غذاها */}
      <div className="glass-panel rounded-3xl overflow-hidden">
        <div className="bg-[var(--text-primary)]/5 px-4 py-3 border-b border-[var(--glass-border)] flex justify-between items-center">
          <span className="text-sm font-bold text-[var(--text-primary)]">برنامه غذایی</span>
          <span className="text-xs text-[var(--text-secondary)]">{dietItems.length} آیتم</span>
        </div>

        <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
          <table className="w-full text-right text-sm">
            <thead className="bg-[var(--text-primary)]/5 text-[var(--text-secondary)] text-xs border-b border-[var(--glass-border)]">
              <tr>
                <th className="p-2 w-10"></th>
                <th className="p-4 w-28">وعده</th>
                <th className="p-4">غذا</th>
                <th className="p-4 text-center w-24">مقدار</th>
                <th className="p-4 text-center w-20">کالری</th>
                <th className="p-4 text-center w-32">ماکرو</th>
                <th className="p-4 w-10"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--glass-border)]">
              <SortableContext items={dietItems.map((_, idx) => `food-${idx}`)} strategy={verticalListSortingStrategy}>
                {dietItems.map((item, idx) => {
                  const displayItem = {
                    id: item.id,
                    meal: item.meal,
                    name: item.custom_name || item.food?.name || 'نامشخص',
                    amount: item.amount,
                    unit: item.unit || 'گرم',
                    c: item.calculated_calories || item.custom_calories || 0,
                    p: item.calculated_protein || item.custom_protein || 0,
                    ch: item.calculated_carbs || item.custom_carbs || 0,
                    f: item.calculated_fat || item.custom_fat || 0,
                  };
                  return (
                    <SortableFoodRow 
                      key={item.id || idx} 
                      item={displayItem} 
                      idx={idx} 
                      onDelete={() => handleDeleteFood(item.id)} 
                    />
                  );
                })}
              </SortableContext>
              {dietItems.length === 0 && (
                <tr>
                  <td colSpan={7} className="p-10 text-center text-[var(--text-secondary)] opacity-50">
                    هنوز غذایی اضافه نشده است
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </DndContext>
      </div>
    </div>
  );
}
