import React, { useState, useEffect } from 'react';
import { ShoppingBag, GripVertical, Trash2, Search, Copy, Plus } from 'lucide-react';
import { foodData } from '../data/foodData';
import toast from 'react-hot-toast';
import Swal from 'sweetalert2';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { arrayMove, SortableContext, sortableKeyboardCoordinates, useSortable, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

// کامپوننت ردیف قابل جابجایی
const SortableFoodRow = ({ item, idx, onDelete }) => {
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
        <button onClick={() => onDelete(idx)} className="text-red-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition p-1 hover:bg-red-500/10 rounded">
          <Trash2 size={16} />
        </button>
      </td>
    </tr>
  );
};

const DietPanel = ({ activeUser, onUpdateUser }) => {
  const [meal, setMeal] = useState('صبحانه');
  const [category, setCategory] = useState('');
  const [foodName, setFoodName] = useState('');
  const [amount, setAmount] = useState('');
  const [foodsList, setFoodsList] = useState([]);
  const [unit, setUnit] = useState('-');
  const [searchTerm, setSearchTerm] = useState('');
  const [customFood, setCustomFood] = useState({ name: '', cal: '', protein: '', carb: '', fat: '', unit: 'گرم', base: 100 });

  // سنسورها برای drag & drop
  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 8 } }),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
  );

  useEffect(() => {
    if (category && foodData[category]) {
      setFoodsList(Object.keys(foodData[category]));
    } else {
      setFoodsList([]);
    }
    setFoodName('');
    setUnit('-');
    setSearchTerm('');
  }, [category]);

  useEffect(() => {
    if (category && foodName && foodData[category] && foodData[category][foodName]) {
      setUnit(foodData[category][foodName].u);
    }
  }, [category, foodName]);

  // فیلتر غذاها با جستجو
  const filteredFoods = searchTerm 
    ? foodsList.filter(f => f.toLowerCase().includes(searchTerm.toLowerCase()))
    : foodsList;

  // هندلر جابجایی
  const handleDragEnd = (event) => {
    const { active, over } = event;
    if (!over || active.id === over.id) return;

    const oldIndex = parseInt(active.id.split('-')[1]);
    const newIndex = parseInt(over.id.split('-')[1]);

    const newUser = { ...activeUser };
    newUser.plans.diet = arrayMove(newUser.plans.diet, oldIndex, newIndex);
    onUpdateUser(newUser);
  };

  const handleDeleteFood = (idx) => {
    const u = { ...activeUser };
    u.plans.diet.splice(idx, 1);
    onUpdateUser(u);
  };

  const handleAddFood = () => {
    if (!foodName || !amount) return toast.error('غذا و مقدار را وارد کنید');
    const info = foodData[category][foodName];
    const ratio = parseFloat(amount) / info.b;
    const newItem = {
      meal, name: foodName, amount: parseFloat(amount), unit: info.u,
      c: Math.round(info.c * ratio), p: Math.round(info.p * ratio),
      ch: Math.round(info.ch * ratio), f: Math.round(info.f * ratio)
    };
    const newUser = { ...activeUser };
    if (!newUser.plans.diet) newUser.plans.diet = [];
    newUser.plans.diet.push(newItem);
    onUpdateUser(newUser);
    setAmount('');
    toast.success('اضافه شد');
  };

  const handleAddCustomFood = () => {
    if (!customFood.name || !customFood.cal) return toast.error('نام و کالری الزامی است');
    const newItem = {
      meal,
      name: customFood.name,
      amount: customFood.base,
      unit: customFood.unit,
      c: parseInt(customFood.cal) || 0,
      p: parseInt(customFood.protein) || 0,
      ch: parseInt(customFood.carb) || 0,
      f: parseInt(customFood.fat) || 0
    };
    const newUser = { ...activeUser };
    if (!newUser.plans.diet) newUser.plans.diet = [];
    newUser.plans.diet.push(newItem);
    onUpdateUser(newUser);
    setCustomFood({ name: '', cal: '', protein: '', carb: '', fat: '', unit: 'گرم', base: 100 });
    toast.success('غذای سفارشی اضافه شد');
  };

  const generateShoppingList = () => {
    const items = {};
    (activeUser.plans.diet || []).forEach(i => {
      const key = `${i.name} (${i.unit})`;
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

  const copyMealToOtherDay = async () => {
    const { value: targetMeal } = await Swal.fire({
      title: 'کپی به کدام وعده؟',
      input: 'select',
      inputOptions: {
        'صبحانه': 'صبحانه',
        'میان وعده ۱': 'میان وعده ۱',
        'ناهار': 'ناهار',
        'میان وعده ۲': 'میان وعده ۲',
        'شام': 'شام',
        'میان وعده ۳': 'میان وعده ۳'
      },
      showCancelButton: true,
      confirmButtonText: 'کپی',
      cancelButtonText: 'لغو'
    });

    if (targetMeal) {
      const currentItems = (activeUser.plans.diet || []).filter(i => i.meal === meal);
      if (currentItems.length === 0) {
        toast.error('این وعده خالی است');
        return;
      }
      const newItems = currentItems.map(i => ({ ...i, meal: targetMeal }));
      const newUser = { ...activeUser };
      newUser.plans.diet = [...(newUser.plans.diet || []), ...newItems];
      onUpdateUser(newUser);
      toast.success(`${currentItems.length} آیتم به ${targetMeal} کپی شد`);
    }
  };

  const total = (activeUser.plans.diet || []).reduce(
    (acc, i) => ({ c: acc.c + i.c, p: acc.p + i.p, ch: acc.ch + i.ch, f: acc.f + i.f }),
    { c: 0, p: 0, ch: 0, f: 0 }
  );

  const calcBmr = () => {
    const w = parseFloat(activeUser.weight);
    const h = parseFloat(activeUser.height);
    const a = parseFloat(activeUser.age);
    if (!w || !h || !a) return 0;
    const isMale = activeUser.gender !== 'female';
    const base = 10 * w + 6.25 * h - 5 * a + (isMale ? 5 : -161);
    return Math.round(base);
  };

  const bmr = calcBmr();
  const activityFactor = parseFloat(activeUser.activity || '1.2');
  const tdee = Math.round(bmr * activityFactor) || 0;

  const dietItems = activeUser.plans.diet || [];

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
            
            {/* نوار پیشرفت */}
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
              <button onClick={copyMealToOtherDay} className="btn-glass bg-purple-500/10 text-purple-600 dark:text-purple-400 text-xs border border-purple-500/20">
                <Copy size={14} /> کپی وعده
              </button>
              <button onClick={generateShoppingList} className="btn-glass bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 text-xs border border-emerald-500/20">
                <ShoppingBag size={14} /> لیست خرید
              </button>
            </div>
          </div>

          {/* انتخاب از بانک غذایی */}
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
              <input type="number" className="input-glass text-center font-bold" placeholder="مقدار" value={amount} onChange={e => setAmount(e.target.value)} />
              <span className="absolute left-3 top-3 text-xs text-slate-400">{unit}</span>
            </div>
            <button onClick={handleAddFood} className="btn-glass bg-emerald-600 hover:bg-emerald-500 text-white px-6">
              <Plus size={16} /> افزودن
            </button>
          </div>

          {/* افزودن غذای سفارشی */}
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
                {dietItems.map((item, idx) => (
                  <SortableFoodRow key={`food-${idx}`} item={item} idx={idx} onDelete={handleDeleteFood} />
                ))}
              </SortableContext>
              {dietItems.length === 0 && (
                <tr>
                  <td colSpan="7" className="p-10 text-center text-[var(--text-secondary)] opacity-50">
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
};

export default DietPanel;
