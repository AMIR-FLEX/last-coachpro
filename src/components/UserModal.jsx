import React, { useState, useEffect, useMemo } from 'react';
import { toast } from 'react-hot-toast';
import { User, Activity, Heart, DollarSign, Ruler, Scale, Calculator, TrendingUp } from 'lucide-react';

const UserModal = ({ isOpen, onClose, onSave, initialData }) => {
  const initialFormState = {
    name: '', phone: '', age: '', gender: 'male',
    height: '', weight: '', activity: '1.55',
    injuries: [], notes: '',
    exp: '', level: 'beginner', job: '', allergy: '',
    days: '', sleep: 'fair', smoke: 'no', alcohol: 'no', caffeine: 'no',
    financial: { startDate: '', duration: 1, amount: 0 },
    measurements: { neck: '', hip: '', thigh: '', arm: '', waist: '', wrist: '', calf: '', chest: '', shoulder: '' },
    email: '', address: '', education: '', maritalStatus: 'single',
    medicalConditions: [], medications: '', dietType: '', nutritionGoals: '',
    waterIntake: '', mealFrequency: '', foodPreferences: [],
    targetWeight: '', bodyFat: ''
  };

  const [formData, setFormData] = useState(initialFormState);
  const [activeTab, setActiveTab] = useState('identity');

  useEffect(() => {
    if (!isOpen) return;
    if (initialData) {
      setFormData(JSON.parse(JSON.stringify(initialData)));
    } else {
      setFormData(initialFormState);
    }
  }, [initialData, isOpen]);

  // محاسبات خودکار
  const calculations = useMemo(() => {
    const w = parseFloat(formData.weight) || 0;
    const h = parseFloat(formData.height) || 0;
    const a = parseFloat(formData.age) || 0;
    const waist = parseFloat(formData.measurements?.waist) || 0;
    const hip = parseFloat(formData.measurements?.hip) || 0;
    const neck = parseFloat(formData.measurements?.neck) || 0;
    const isMale = formData.gender !== 'female';
    const activityFactor = parseFloat(formData.activity) || 1.2;

    // BMI (Body Mass Index)
    const heightM = h / 100;
    const bmi = heightM > 0 ? (w / (heightM * heightM)).toFixed(1) : 0;
    let bmiCategory = '';
    let bmiColor = '';
    if (bmi < 18.5) { bmiCategory = 'کمبود وزن'; bmiColor = 'text-yellow-500'; }
    else if (bmi < 25) { bmiCategory = 'نرمال'; bmiColor = 'text-emerald-500'; }
    else if (bmi < 30) { bmiCategory = 'اضافه وزن'; bmiColor = 'text-orange-500'; }
    else { bmiCategory = 'چاقی'; bmiColor = 'text-red-500'; }

    // WHR (Waist-to-Hip Ratio)
    const whr = hip > 0 ? (waist / hip).toFixed(2) : 0;
    let whrRisk = '';
    let whrColor = '';
    if (isMale) {
      if (whr < 0.9) { whrRisk = 'کم'; whrColor = 'text-emerald-500'; }
      else if (whr < 1.0) { whrRisk = 'متوسط'; whrColor = 'text-yellow-500'; }
      else { whrRisk = 'بالا'; whrColor = 'text-red-500'; }
    } else {
      if (whr < 0.8) { whrRisk = 'کم'; whrColor = 'text-emerald-500'; }
      else if (whr < 0.85) { whrRisk = 'متوسط'; whrColor = 'text-yellow-500'; }
      else { whrRisk = 'بالا'; whrColor = 'text-red-500'; }
    }

    // BMR (Basal Metabolic Rate) - Mifflin-St Jeor
    const bmr = w > 0 && h > 0 && a > 0 
      ? Math.round(10 * w + 6.25 * h - 5 * a + (isMale ? 5 : -161))
      : 0;

    // TDEE (Total Daily Energy Expenditure)
    const tdee = Math.round(bmr * activityFactor);

    // Body Fat % (Navy Formula) - تقریبی
    let bodyFatPercent = 0;
    if (waist > 0 && neck > 0 && h > 0) {
      if (isMale) {
        bodyFatPercent = (495 / (1.0324 - 0.19077 * Math.log10(waist - neck) + 0.15456 * Math.log10(h))) - 450;
      } else if (hip > 0) {
        bodyFatPercent = (495 / (1.29579 - 0.35004 * Math.log10(waist + hip - neck) + 0.22100 * Math.log10(h))) - 450;
      }
      bodyFatPercent = Math.max(0, Math.min(50, bodyFatPercent)).toFixed(1);
    }

    // Ideal Weight Range (BMI 18.5-24.9)
    const idealWeightMin = heightM > 0 ? Math.round(18.5 * heightM * heightM) : 0;
    const idealWeightMax = heightM > 0 ? Math.round(24.9 * heightM * heightM) : 0;

    // Macro Suggestions (based on goals)
    const protein = Math.round(w * 2); // 2g per kg for athletes
    const fat = Math.round(tdee * 0.25 / 9); // 25% of calories from fat
    const carbs = Math.round((tdee - protein * 4 - fat * 9) / 4);

    return { 
      bmi, bmiCategory, bmiColor, 
      whr, whrRisk, whrColor, 
      bmr, tdee, bodyFatPercent,
      idealWeightMin, idealWeightMax,
      protein, fat, carbs
    };
  }, [formData.weight, formData.height, formData.age, formData.gender, formData.activity, formData.measurements]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { id, value } = e.target;
    if (id.startsWith('m-')) {
      const field = id.split('-')[1];
      setFormData(prev => ({
        ...prev,
        measurements: { ...prev.measurements, [field]: value }
      }));
    } else {
      setFormData(prev => ({ ...prev, [id]: value }));
    }
  };

  const handleInjury = (inj) => {
    setFormData(prev => {
      const newInj = prev.injuries.includes(inj) 
        ? prev.injuries.filter(i => i !== inj) 
        : [...prev.injuries, inj];
      return { ...prev, injuries: newInj };
    });
  };

  const handleMedicalCondition = (cond) => {
    setFormData(prev => {
      const current = prev.medicalConditions || [];
      const updated = current.includes(cond) 
        ? current.filter(c => c !== cond)
        : [...current, cond];
      return { ...prev, medicalConditions: updated };
    });
  };

  const handleSubmit = () => {
    if (!formData.name.trim()) {
      toast.error('نام الزامی است');
      return;
    }
    if (formData.age && (+formData.age <= 0 || +formData.age > 100)) {
      toast.error('سن وارد شده معتبر نیست');
      return;
    }
    if (formData.height && (+formData.height < 100 || +formData.height > 230)) {
      toast.error('قد وارد شده غیرواقعی است');
      return;
    }
    if (formData.weight && (+formData.weight < 30 || +formData.weight > 250)) {
      toast.error('وزن وارد شده غیرواقعی است');
      return;
    }
    onSave(formData);
  };

  const tabs = [
    { id: 'identity', label: 'مشخصات فردی', icon: <User size={16} /> },
    { id: 'anthropometry', label: 'آنتروپومتری', icon: <Ruler size={16} /> },
    { id: 'medical', label: 'پزشکی', icon: <Heart size={16} /> },
    { id: 'financial', label: 'مالی', icon: <DollarSign size={16} /> },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-slate-900/80 backdrop-blur-sm" onClick={onClose}></div>
      <div className="relative glass-panel w-full max-w-6xl rounded-3xl shadow-2xl flex flex-col max-h-[92vh] animate-fade-in !bg-[var(--bg-primary)] dark:!bg-slate-900 border border-[var(--glass-border)]">
        
        {/* هدر */}
        <div className="p-6 border-b border-[var(--glass-border)] flex justify-between items-center bg-gradient-to-l from-sky-500/10 to-transparent">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-sky-500 to-blue-600 flex items-center justify-center text-white text-xl font-bold shadow-lg">
              {formData.name ? formData.name.charAt(0) : '👤'}
            </div>
            <div>
              <h3 className="text-xl font-black text-[var(--text-primary)]">
                {initialData ? 'ویرایش پرونده' : 'پرونده جدید'}
              </h3>
              <p className="text-xs text-[var(--text-secondary)]">
                {formData.name || 'ورزشکار جدید'}
              </p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-red-500 text-2xl transition hover:rotate-90">✕</button>
        </div>

        {/* تب‌ها */}
        <div className="px-6 pt-4 border-b border-[var(--glass-border)] flex gap-2 overflow-x-auto">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2.5 rounded-t-xl transition flex items-center gap-2 text-sm font-bold whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-sky-600 text-white shadow-lg shadow-sky-500/30'
                  : 'bg-[var(--glass-bg)] text-[var(--text-secondary)] hover:bg-[var(--text-primary)]/10'
              }`}
            >
              {tab.icon}
              {tab.label}
            </button>
          ))}
        </div>
        
        {/* محتوا */}
        <div className="p-6 overflow-y-auto flex-1 custom-scrollbar">
          
          {/* تب مشخصات فردی */}
          {activeTab === 'identity' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block font-bold">نام و نام خانوادگی *</label>
                  <input id="name" value={formData.name} onChange={handleChange} className="input-glass border-r-4 border-r-sky-500" placeholder="علی رضایی" />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">شماره تماس</label>
                  <input id="phone" value={formData.phone} onChange={handleChange} className="input-glass" placeholder="09123456789" />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">ایمیل</label>
                  <input id="email" type="email" value={formData.email || ''} onChange={handleChange} className="input-glass" placeholder="email@example.com" />
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">سن</label>
                  <input id="age" type="number" value={formData.age} onChange={handleChange} className="input-glass text-center text-lg font-bold" placeholder="25" />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">جنسیت</label>
                  <select id="gender" value={formData.gender} onChange={handleChange} className="input-glass">
                    <option value="male">آقا</option>
                    <option value="female">خانم</option>
                  </select>
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">وضعیت تأهل</label>
                  <select id="maritalStatus" value={formData.maritalStatus || 'single'} onChange={handleChange} className="input-glass">
                    <option value="single">مجرد</option>
                    <option value="married">متأهل</option>
                  </select>
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">تحصیلات</label>
                  <select id="education" value={formData.education || ''} onChange={handleChange} className="input-glass">
                    <option value="">انتخاب...</option>
                    <option value="diploma">دیپلم</option>
                    <option value="associate">فوق دیپلم</option>
                    <option value="bachelor">لیسانس</option>
                    <option value="master">فوق لیسانس</option>
                    <option value="phd">دکترا</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">شغل</label>
                  <input id="job" placeholder="مهندس نرم‌افزار" value={formData.job} onChange={handleChange} className="input-glass" />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">آدرس</label>
                  <input id="address" value={formData.address || ''} onChange={handleChange} className="input-glass" placeholder="تهران، ..." />
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">سطح تمرینی</label>
                  <select id="level" value={formData.level} onChange={handleChange} className="input-glass">
                    <option value="beginner">مبتدی</option>
                    <option value="intermediate">متوسط</option>
                    <option value="advanced">پیشرفته</option>
                    <option value="pro">حرفه‌ای</option>
                  </select>
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">کیفیت خواب</label>
                  <select id="sleep" value={formData.sleep} onChange={handleChange} className="input-glass">
                    <option value="good">خوب (7-9 ساعت)</option>
                    <option value="fair">متوسط (5-7 ساعت)</option>
                    <option value="poor">ضعیف (&lt;5 ساعت)</option>
                  </select>
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">سطح فعالیت</label>
                  <select id="activity" value={formData.activity} onChange={handleChange} className="input-glass text-xs">
                    <option value="1.2">کم‌تحرک</option>
                    <option value="1.375">سبک (1-3 روز)</option>
                    <option value="1.55">متوسط (3-5 روز)</option>
                    <option value="1.725">سنگین (6-7 روز)</option>
                    <option value="1.9">ورزشکار حرفه‌ای</option>
                  </select>
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">هدف تغذیه</label>
                  <select id="nutritionGoals" value={formData.nutritionGoals || ''} onChange={handleChange} className="input-glass">
                    <option value="">انتخاب...</option>
                    <option value="weight-loss">کاهش وزن</option>
                    <option value="weight-gain">افزایش وزن</option>
                    <option value="muscle-gain">عضله‌سازی</option>
                    <option value="maintenance">حفظ وزن</option>
                    <option value="recomp">ریکامپ</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* تب آنتروپومتری */}
          {activeTab === 'anthropometry' && (
            <div className="space-y-6">
              {/* قد و وزن اصلی */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block font-bold flex items-center gap-1">
                    <Ruler size={12} /> قد (cm)
                  </label>
                  <input id="height" type="number" value={formData.height} onChange={handleChange} className="input-glass text-center text-xl font-black text-sky-500" placeholder="180" />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block font-bold flex items-center gap-1">
                    <Scale size={12} /> وزن فعلی (kg)
                  </label>
                  <input id="weight" type="number" value={formData.weight} onChange={handleChange} className="input-glass text-center text-xl font-black text-emerald-500" placeholder="85" />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">وزن هدف (kg)</label>
                  <input id="targetWeight" type="number" value={formData.targetWeight || ''} onChange={handleChange} className="input-glass text-center font-bold" placeholder="75" />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">درصد چربی (%)</label>
                  <input id="bodyFat" type="number" value={formData.bodyFat || ''} onChange={handleChange} className="input-glass text-center font-bold" placeholder="18" />
                </div>
              </div>

              {/* کارت‌های محاسبات */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="glass-card p-4 rounded-2xl bg-gradient-to-br from-sky-500/10 to-blue-500/5 border border-sky-500/20">
                  <div className="flex items-center gap-2 mb-2">
                    <Calculator size={16} className="text-sky-500" />
                    <span className="text-xs text-slate-400 font-bold">BMI</span>
                  </div>
                  <div className={`text-2xl font-black ${calculations.bmiColor}`}>{calculations.bmi || '-'}</div>
                  <div className={`text-xs ${calculations.bmiColor}`}>{calculations.bmiCategory}</div>
                </div>

                <div className="glass-card p-4 rounded-2xl bg-gradient-to-br from-purple-500/10 to-pink-500/5 border border-purple-500/20">
                  <div className="flex items-center gap-2 mb-2">
                    <Activity size={16} className="text-purple-500" />
                    <span className="text-xs text-slate-400 font-bold">WHR</span>
                  </div>
                  <div className={`text-2xl font-black ${calculations.whrColor}`}>{calculations.whr || '-'}</div>
                  <div className={`text-xs ${calculations.whrColor}`}>ریسک: {calculations.whrRisk || '-'}</div>
                </div>

                <div className="glass-card p-4 rounded-2xl bg-gradient-to-br from-orange-500/10 to-red-500/5 border border-orange-500/20">
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingUp size={16} className="text-orange-500" />
                    <span className="text-xs text-slate-400 font-bold">BMR</span>
                  </div>
                  <div className="text-2xl font-black text-orange-500">{calculations.bmr || '-'}</div>
                  <div className="text-xs text-slate-400">کالری پایه</div>
                </div>

                <div className="glass-card p-4 rounded-2xl bg-gradient-to-br from-emerald-500/10 to-green-500/5 border border-emerald-500/20">
                  <div className="flex items-center gap-2 mb-2">
                    <Activity size={16} className="text-emerald-500" />
                    <span className="text-xs text-slate-400 font-bold">TDEE</span>
                  </div>
                  <div className="text-2xl font-black text-emerald-500">{calculations.tdee || '-'}</div>
                  <div className="text-xs text-slate-400">کالری روزانه</div>
                </div>
              </div>

              {/* اطلاعات تکمیلی محاسبات */}
              {calculations.tdee > 0 && (
                <div className="glass-card p-4 rounded-2xl bg-[var(--text-primary)]/5 border border-[var(--glass-border)]">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                    <div>
                      <div className="text-xs text-slate-400 mb-1">وزن ایده‌آل</div>
                      <div className="font-bold text-[var(--text-primary)]">{calculations.idealWeightMin}-{calculations.idealWeightMax} kg</div>
                    </div>
                    <div>
                      <div className="text-xs text-slate-400 mb-1">پروتئین پیشنهادی</div>
                      <div className="font-bold text-blue-500">{calculations.protein}g</div>
                    </div>
                    <div>
                      <div className="text-xs text-slate-400 mb-1">کربوهیدرات پیشنهادی</div>
                      <div className="font-bold text-yellow-500">{calculations.carbs}g</div>
                    </div>
                    <div>
                      <div className="text-xs text-slate-400 mb-1">چربی پیشنهادی</div>
                      <div className="font-bold text-red-500">{calculations.fat}g</div>
                    </div>
                  </div>
                </div>
              )}

              {/* سایزگیری بدن */}
              <div>
                <h4 className="text-purple-500 font-bold text-sm border-b border-[var(--glass-border)] pb-2 mb-4 flex items-center gap-2">
                  <Ruler size={16} /> سایزگیری بدن (cm)
                </h4>
                <div className="grid grid-cols-3 md:grid-cols-5 gap-3">
                  {[
                    { key: 'neck', label: 'گردن', emoji: '🔵' },
                    { key: 'shoulder', label: 'شانه', emoji: '💪' },
                    { key: 'chest', label: 'سینه', emoji: '🫁' },
                    { key: 'arm', label: 'بازو', emoji: '💪' },
                    { key: 'waist', label: 'کمر', emoji: '⭕' },
                    { key: 'hip', label: 'لگن', emoji: '🔴' },
                    { key: 'thigh', label: 'ران', emoji: '🦵' },
                    { key: 'calf', label: 'ساق', emoji: '🦶' },
                    { key: 'wrist', label: 'مچ دست', emoji: '✋' },
                  ].map(p => (
                    <div key={p.key} className="space-y-1">
                      <label className="text-[10px] text-slate-500 block text-center">{p.emoji} {p.label}</label>
                      <input 
                        id={`m-${p.key}`} 
                        type="number"
                        value={formData.measurements?.[p.key] || ''} 
                        onChange={handleChange} 
                        className="input-glass text-center px-1 font-bold" 
                        placeholder="0"
                      />
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* تب پزشکی */}
          {activeTab === 'medical' && (
            <div className="space-y-6">
              {/* آسیب‌دیدگی‌ها */}
              <div className="bg-red-500/5 p-4 rounded-2xl border border-red-500/20">
                <label className="text-xs text-red-500 block mb-3 font-bold flex items-center gap-2">
                  ⚠️ آسیب‌دیدگی‌ها و مشکلات اسکلتی-عضلانی
                </label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm text-[var(--text-secondary)]">
                  {['دیسک کمر', 'دیسک گردن', 'زانو درد', 'شانه درد', 'سیاتیک', 'قوز پشتی', 'لوردوز', 'کایفوز', 'اسکولیوز', 'آرنج درد', 'مچ درد', 'مچ پا درد', 'کمر درد مزمن', 'گردن درد', 'شانه یخ‌زده', 'سندرم تونل کارپال'].map(inj => (
                    <label key={inj} className="flex items-center gap-2 cursor-pointer hover:text-red-500 transition p-1 rounded hover:bg-red-500/10">
                      <input 
                        type="checkbox" 
                        checked={formData.injuries.includes(inj)} 
                        onChange={() => handleInjury(inj)} 
                        className="accent-red-500 w-4 h-4 rounded" 
                      />
                      {inj}
                    </label>
                  ))}
                </div>
              </div>

              {/* بیماری‌ها */}
              <div className="bg-yellow-500/5 p-4 rounded-2xl border border-yellow-500/20">
                <label className="text-xs text-yellow-600 block mb-3 font-bold flex items-center gap-2">
                  🏥 بیماری‌ها و شرایط پزشکی
                </label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm text-[var(--text-secondary)]">
                  {['دیابت نوع 1', 'دیابت نوع 2', 'فشار خون', 'کلسترول بالا', 'بیماری قلبی', 'آسم', 'آرتریت', 'پوکی استخوان', 'کم‌خونی', 'مشکلات تیروئید', 'مشکلات کلیوی', 'مشکلات کبدی', 'سندرم روده تحریک‌پذیر', 'ریفلاکس معده'].map(cond => (
                    <label key={cond} className="flex items-center gap-2 cursor-pointer hover:text-yellow-500 transition p-1 rounded hover:bg-yellow-500/10">
                      <input 
                        type="checkbox" 
                        checked={(formData.medicalConditions || []).includes(cond)} 
                        onChange={() => handleMedicalCondition(cond)} 
                        className="accent-yellow-500 w-4 h-4 rounded" 
                      />
                      {cond}
                    </label>
                  ))}
                </div>
              </div>

              {/* داروها و حساسیت */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">داروهای مصرفی</label>
                  <textarea 
                    id="medications" 
                    value={formData.medications || ''} 
                    onChange={handleChange} 
                    className="input-glass h-20" 
                    placeholder="آسپرین، انسولین، ..."
                  />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">حساسیت‌های غذایی</label>
                  <textarea 
                    id="allergy" 
                    value={formData.allergy} 
                    onChange={handleChange} 
                    className="input-glass h-20" 
                    placeholder="بادام زمینی، لاکتوز، گلوتن، ..."
                  />
                </div>
              </div>

              {/* ترجیحات تغذیه */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">نوع رژیم غذایی</label>
                  <select id="dietType" value={formData.dietType || ''} onChange={handleChange} className="input-glass">
                    <option value="">انتخاب...</option>
                    <option value="normal">عادی</option>
                    <option value="vegetarian">گیاهخوار</option>
                    <option value="vegan">وگان</option>
                    <option value="keto">کتوژنیک</option>
                    <option value="paleo">پالئو</option>
                    <option value="halal">حلال</option>
                  </select>
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">مصرف آب روزانه (لیتر)</label>
                  <input type="number" id="waterIntake" value={formData.waterIntake || ''} onChange={handleChange} className="input-glass" placeholder="2.5" />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block">تعداد وعده روزانه</label>
                  <select id="mealFrequency" value={formData.mealFrequency || ''} onChange={handleChange} className="input-glass">
                    <option value="">انتخاب...</option>
                    <option value="3">3 وعده</option>
                    <option value="4">4 وعده</option>
                    <option value="5">5 وعده</option>
                    <option value="6">6 وعده</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* تب مالی */}
          {activeTab === 'financial' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block font-bold">شروع اشتراک</label>
                  <input 
                    type="date" 
                    className="input-glass" 
                    value={formData.financial?.startDate} 
                    onChange={e => setFormData({...formData, financial: {...formData.financial, startDate: e.target.value}})} 
                  />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block font-bold">مدت (ماه)</label>
                  <input 
                    type="number" 
                    className="input-glass text-center font-bold" 
                    value={formData.financial?.duration} 
                    onChange={e => setFormData({...formData, financial: {...formData.financial, duration: parseInt(e.target.value) || 1}})} 
                  />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-500 block font-bold">مبلغ (تومان)</label>
                  <input 
                    type="number" 
                    className="input-glass text-center font-bold text-emerald-500" 
                    value={formData.financial?.amount} 
                    onChange={e => setFormData({...formData, financial: {...formData.financial, amount: e.target.value}})} 
                    placeholder="500000"
                  />
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-xs text-slate-500 block">یادداشت‌های خصوصی مربی</label>
                <textarea 
                  id="notes" 
                  placeholder="اهداف، محدودیت‌ها، نکات مهم..." 
                  value={formData.notes} 
                  onChange={handleChange} 
                  className="input-glass h-32" 
                />
              </div>
            </div>
          )}
        </div>

        {/* فوتر */}
        <div className="p-6 border-t border-[var(--glass-border)] flex justify-between items-center bg-[var(--glass-bg)]">
          <button onClick={onClose} className="btn-glass bg-slate-500/10 text-slate-400 hover:bg-slate-500/20">
            انصراف
          </button>
          <button onClick={handleSubmit} className="btn-glass bg-sky-600 hover:bg-sky-500 text-white py-3 px-10 text-lg shadow-lg shadow-sky-500/20">
            ✓ ذخیره پرونده
          </button>
        </div>
      </div>
    </div>
  );
};

export default UserModal;
