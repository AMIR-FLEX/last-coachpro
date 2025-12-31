import React, { createContext, useContext, useState, useEffect } from 'react';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { toast } from 'react-hot-toast';
import Swal from 'sweetalert2';

const STORAGE_KEY = 'flexProMaxData_v14_Final';
const AppContext = createContext();

const migrateUser = (u) => {
    if (!u.plans) u.plans = {};
    if (!u.plans.workouts) u.plans.workouts = {};
    for (let i = 1; i <= 7; i++) if (!u.plans.workouts[i]) u.plans.workouts[i] = [];
    if (!u.plans.diet) u.plans.diet = [];
    if (!u.plans.supps) u.plans.supps = [];
    if (!u.plans.prog) u.plans.prog = [];
    if (!u.measurements) u.measurements = {};
    if (!u.financial) u.financial = { startDate: '', duration: 1, amount: 0 };
    return u;
};

// --- موتور تولید HTML برای چاپ ---
const generatePrintHTML = (user, type) => {
    const date = new Date().toLocaleDateString('fa-IR');
    // رنگ‌ها برای بخش‌های مختلف
    const headerColor = type === 'training' ? '#0ea5e9' : type === 'nutrition' ? '#10b981' : type === 'supplements' ? '#a855f7' : '#64748b';
    const title =
        type === 'training'
            ? 'برنامه تمرینی'
            : type === 'nutrition'
            ? 'رژیم غذایی'
            : type === 'supplements'
            ? 'نسخه مکمل'
            : 'پرونده اطلاعات فردی';

    // استایل‌های ثابت برای پرینت
    const containerStyle = "font-family:'Vazirmatn', sans-serif; direction:rtl; color:#000; padding:20px; width: 100%; box-sizing: border-box;";
    const headerStyle = `border-bottom: 4px solid ${headerColor}; padding-bottom:15px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:flex-end;`;
    const boxStyle = "background:#f1f5f9; border:1px solid #cbd5e1; border-radius:8px; padding:10px; margin-bottom:15px; font-size:12px;";
    const tableStyle = "width:100%; border-collapse:collapse; margin-bottom:15px; font-size:11px;";
    const thStyle = `background:${headerColor}; color:white; padding:8px; border:1px solid #ccc; text-align:center; -webkit-print-color-adjust: exact; print-color-adjust: exact;`;
    const tdStyle = "border:1px solid #ddd; padding:6px; text-align:center; vertical-align:middle;";

    let content = '';

    // حالت ۰: فقط پروفایل و اطلاعات هویتی / پزشکی / آنتروپومتریک (بدون برنامه‌ها)
    if (type === 'profile') {
        const injuries = (user.injuries || []).join('، ') || '-';
        const measurements = user.measurements || {};
        const financial = user.financial || { startDate: '', duration: '', amount: '' };

        const lifestyleHtml = `
            <div style="${boxStyle}">
                <div><b>شغل:</b> ${user.job || '-'}</div>
                <div><b>سطح فعالیت:</b> ${user.activity || '-'}</div>
                <div><b>کیفیت خواب:</b> ${user.sleep || '-'}</div>
                <div><b>سطح تمرینی:</b> ${user.level || '-'}</div>
            </div>
        `;

        const medicalHtml = `
            <div style="${boxStyle}">
                <div><b>حساسیت غذایی:</b> ${user.allergy || '-'}</div>
                <div><b>آسیب دیدگی‌ها / مشکلات پزشکی:</b> ${injuries}</div>
            </div>
        `;

        const anthropoHtml = `
            <h2 style="font-size:16px; background:#eee; padding:5px; margin-top:20px;">آنتروپومتری (cm)</h2>
            <table style="${tableStyle}">
                <thead>
                    <tr>
                        <th style="${thStyle}">گردن</th>
                        <th style="${thStyle}">کمر</th>
                        <th style="${thStyle}">لگن</th>
                        <th style="${thStyle}">ران</th>
                        <th style="${thStyle}">بازو</th>
                        <th style="${thStyle}">مچ</th>
                        <th style="${thStyle}">ساق</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="${tdStyle}">${measurements.neck || '-'}</td>
                        <td style="${tdStyle}">${measurements.waist || '-'}</td>
                        <td style="${tdStyle}">${measurements.hip || '-'}</td>
                        <td style="${tdStyle}">${measurements.thigh || '-'}</td>
                        <td style="${tdStyle}">${measurements.arm || '-'}</td>
                        <td style="${tdStyle}">${measurements.wrist || '-'}</td>
                        <td style="${tdStyle}">${measurements.calf || '-'}</td>
                    </tr>
                </tbody>
            </table>
        `;

        const financialHtml = `
            <h2 style="font-size:16px; background:#eee; padding:5px; margin-top:20px;">اطلاعات مالی</h2>
            <div style="${boxStyle}; display:flex; gap:15px; font-size:12px;">
                <div><b>شروع اشتراک:</b> ${financial.startDate || '-'}</div>
                <div><b>مدت (ماه):</b> ${financial.duration || '-'}</div>
                <div><b>مبلغ (تومان):</b> ${financial.amount || '-'}</div>
            </div>
        `;

        const notesHtml = user.notes
            ? `<div style="${boxStyle} background:#fefce8; border-color:#fef08a;"><b>یادداشت مربی:</b><br/>${user.notes}</div>`
            : '';

        content = lifestyleHtml + medicalHtml + anthropoHtml + financialHtml + notesHtml;

        return `
        <div style="${containerStyle}">
            <div style="${headerStyle}">
                <div>
                    <h1 style="margin:0; font-size:28px; font-weight:900; font-style:italic;">FLEX <span style="color:${headerColor}">PRO</span></h1>
                    <p style="margin:5px 0 0 0; font-size:12px; color:#64748b;">سیستم هوشمند مدیریت مربیگری</p>
                </div>
                <div style="text-align:left;">
                    <h2 style="margin:0; font-size:20px; color:${headerColor};">پرونده اطلاعات فردی</h2>
                    <p style="margin:5px 0 0 0; font-size:12px; font-weight:bold;">تاریخ: ${date}</p>
                </div>
            </div>

            <div style="${boxStyle} display:grid; grid-template-columns:repeat(4, 1fr); gap:10px;">
                <div><b>نام:</b> ${user.name}</div>
                <div><b>سن:</b> ${user.age || '-'}</div>
                <div><b>قد:</b> ${user.height || '-'}</div>
                <div><b>وزن:</b> ${user.weight || '-'}</div>
            </div>

            ${content}

            <div style="margin-top:30px; border-top:1px solid #ccc; padding-top:10px; text-align:center; font-size:10px; color:#94a3b8;">
                تنظیم شده توسط نرم‌افزار FLEX PRO | موفق باشید!
            </div>
        </div>
        `;
    }

    // ۱. ساخت محتوای تمرین
    if (type === 'training' || type === 'profile') {
        let trainingContent = '';
        Object.keys(user.plans.workouts).forEach(day => {
            const moves = user.plans.workouts[day];
            if (moves && moves.length > 0) {
                trainingContent += `<div style="margin-top:15px; break-inside: avoid;">
                    <h3 style="font-size:14px; margin:0 0 5px 0; border-bottom:2px solid #333; display:inline-block;">جلسه ${day}</h3>
                    <table style="${tableStyle}">
                        <thead><tr>
                            <th style="${thStyle}">سیستم</th><th style="${thStyle} width:40%;">حرکت</th>
                            <th style="${thStyle}">ست</th><th style="${thStyle}">تکرار/زمان</th>
                            <th style="${thStyle}">استراحت</th><th style="${thStyle}">نکات</th>
                        </tr></thead>
                        <tbody>`;
                moves.forEach(m => {
                    let name = `<b>${m.name}</b>`;
                    if (['superset', 'triset', 'giantset'].includes(m.type)) {
                        if (m.name2) name += `<br/><span style="color:${headerColor}">+</span> ${m.name2}`;
                        if (m.name3) name += `<br/><span style="color:${headerColor}">+</span> ${m.name3}`;
                    }
                    const val = m.mode === 'cardio' ? `${m.duration} دقیقه` : m.reps;
                    const restShow = m.restUnit === 'm' ? `${m.rest} دقیقه` : (m.rest ? `${m.rest} ثانیه` : '-');
                    
                    trainingContent += `<tr>
                        <td style="${tdStyle} font-weight:bold; font-size:10px;">${m.type ? m.type.toUpperCase() : 'NORMAL'}</td>
                        <td style="${tdStyle} text-align:right;">${name}</td>
                        <td style="${tdStyle} font-weight:bold;">${m.sets || '-'}</td>
                        <td style="${tdStyle}">${val}</td>
                        <td style="${tdStyle}">${restShow}</td>
                        <td style="${tdStyle} font-size:10px; text-align:right;">${m.note || ''}</td>
                    </tr>`;
                });
                trainingContent += `</tbody></table></div>`;
            }
        });
        if (trainingContent) {
            content += `<h2 style="font-size:16px; background:#eee; padding:5px; margin-top:20px;">برنامه تمرینی</h2>
                        <div style="${boxStyle} background:#fefce8; border-color:#fef08a;"><b>گرم کردن:</b> ۵-۱۰ دقیقه هوازی سبک + کشش پویا. <br/><b>سرد کردن:</b> کشش ایستا (هر عضله ۳۰ ثانیه).</div>
                        ${trainingContent}`;
        }
    }

    // ۲. ساخت محتوای تغذیه
    if (type === 'nutrition' || type === 'profile') {
        const order = ["صبحانه", "میان وعده ۱", "ناهار", "میان وعده ۲", "شام", "میان وعده ۳"];
        let dietContent = '';
        let totalCal = 0, totalP = 0, totalC = 0, totalF = 0;

        order.forEach(meal => {
            const items = user.plans.diet.filter(i => i.meal === meal);
            if (items.length > 0) {
                dietContent += `<div style="background:#e2e8f0; padding:5px 10px; font-weight:bold; font-size:12px; margin-top:10px; border:1px solid #cbd5e1;">${meal}</div>
                <table style="${tableStyle} margin-top:0;">
                    <thead><tr><th style="${thStyle} background:#475569;">غذا</th><th style="${thStyle} background:#475569;">مقدار</th><th style="${thStyle} background:#475569;">کالری</th><th style="${thStyle} background:#475569;">P / C / F</th></tr></thead><tbody>`;
                items.forEach(i => {
                    totalCal += i.c; totalP += i.p; totalC += i.ch; totalF += i.f;
                    dietContent += `<tr>
                        <td style="${tdStyle} text-align:right;">${i.name}</td>
                        <td style="${tdStyle}">${i.amount} ${i.unit}</td>
                        <td style="${tdStyle} font-weight:bold;">${i.c}</td>
                        <td style="${tdStyle} direction:ltr; font-size:10px;">${i.p} / ${i.ch} / ${i.f}</td>
                    </tr>`;
                });
                dietContent += `</tbody></table>`;
            }
        });

        if (dietContent) {
            content += `<h2 style="font-size:16px; background:#eee; padding:5px; margin-top:20px; page-break-before:auto;">رژیم غذایی</h2>
                        ${dietContent}
                        <div style="${boxStyle} background:#1e293b; color:white; display:flex; justify-content:space-around;">
                            <span>کالری کل: <b>${totalCal}</b></span>
                            <span>پروتئین: ${totalP}g</span>
                            <span>کربوهیدرات: ${totalC}g</span>
                            <span>چربی: ${totalF}g</span>
                        </div>`;
        }
    }

    // ۳. ساخت محتوای مکمل
    if (type === 'supplements' || type === 'profile') {
        if (user.plans.supps && user.plans.supps.length > 0) {
            let suppContent = `<table style="${tableStyle}">
                <thead><tr><th style="${thStyle} background:#7e22ce;">مکمل</th><th style="${thStyle} background:#7e22ce;">دوز</th><th style="${thStyle} background:#7e22ce;">زمان</th><th style="${thStyle} background:#7e22ce;">نکات</th></tr></thead><tbody>`;
            user.plans.supps.forEach(s => {
                suppContent += `<tr>
                    <td style="${tdStyle} font-weight:bold;">${s.name}</td>
                    <td style="${tdStyle}">${s.dose}</td>
                    <td style="${tdStyle}">${s.time}</td>
                    <td style="${tdStyle} text-align:right; font-size:10px;">${s.note}</td>
                </tr>`;
            });
            suppContent += `</tbody></table>`;
            content += `<h2 style="font-size:16px; background:#eee; padding:5px; margin-top:20px;">مکمل و داروها</h2>${suppContent}`;
        }
    }

    // بدنه نهایی HTML
    return `
        <div style="${containerStyle}">
            <div style="${headerStyle}">
                <div>
                    <h1 style="margin:0; font-size:28px; font-weight:900; font-style:italic;">FLEX <span style="color:${headerColor}">PRO</span></h1>
                    <p style="margin:5px 0 0 0; font-size:12px; color:#64748b;">سیستم هوشمند مدیریت مربیگری</p>
                </div>
                <div style="text-align:left;">
                    <h2 style="margin:0; font-size:20px; color:${headerColor};">${title}</h2>
                    <p style="margin:5px 0 0 0; font-size:12px; font-weight:bold;">تاریخ: ${date}</p>
                </div>
            </div>

            <div style="${boxStyle} display:grid; grid-template-columns:repeat(4, 1fr); gap:10px;">
                <div><b>نام:</b> ${user.name}</div>
                <div><b>سن:</b> ${user.age || '-'}</div>
                <div><b>قد:</b> ${user.height || '-'}</div>
                <div><b>وزن:</b> ${user.weight || '-'}</div>
            </div>

            ${content}

            <div style="margin-top:30px; border-top:1px solid #ccc; padding-top:10px; text-align:center; font-size:10px; color:#94a3b8;">
                تنظیم شده توسط نرم‌افزار FLEX PRO | موفق باشید!
            </div>
        </div>
    `;
};

export const AppProvider = ({ children }) => {
    const [users, setUsers] = useState([]);
    const [templates, setTemplates] = useState([]);
    const [activeUserId, setActiveUserId] = useState(null);
    const [currentTab, setCurrentTab] = useState('users');
    const [theme, setTheme] = useState('dark');
    const [printData, setPrintData] = useState(null);

    useEffect(() => {
        const savedData = localStorage.getItem(STORAGE_KEY);
        if (savedData) {
            try {
                const parsed = JSON.parse(savedData);
                setUsers(parsed.users.map(migrateUser));
                setTemplates(parsed.templates || []);
                // اگر دیتای خراب بود، ریست نکن، فقط آرایه خالی بده
            } catch (e) { console.error(e); }
        }
        const savedTheme = localStorage.getItem('flexTheme') || 'dark';
        setTheme(savedTheme);
        document.documentElement.classList.toggle('dark', savedTheme === 'dark');
    }, []);

    useEffect(() => {
        const data = JSON.stringify({ users, templates });
        localStorage.setItem(STORAGE_KEY, data);
    }, [users, templates]);

    const activeUser = users.find(u => u.id === activeUserId) || null;

    const saveUser = (userData) => {
        const newUser = migrateUser({ ...userData, id: userData.id || Date.now() });
        setUsers(prev => {
            const idx = prev.findIndex(u => u.id === newUser.id);
            if (idx > -1) {
                const updated = [...prev];
                updated[idx] = { ...prev[idx], ...newUser }; // حفظ داده‌های قبلی و اعمال اسکیمای جدید
                return updated;
            }
            return [...prev, newUser];
        });
        toast.success('اطلاعات با موفقیت ذخیره شد');
    };

    const updateActiveUser = (u) => {
        setUsers(prev => prev.map(user => user.id === u.id ? u : user));
    };

    const deleteUser = (id) => {
        Swal.fire({
            title: 'آیا مطمئن هستید؟',
            text: "اطلاعات این شاگرد غیرقابل بازگشت خواهد بود!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#ef4444',
            cancelButtonColor: '#64748b',
            confirmButtonText: 'بله، حذف کن',
            cancelButtonText: 'لغو',
            background: theme === 'dark' ? '#1e293b' : '#fff',
            color: theme === 'dark' ? '#fff' : '#000'
        }).then((result) => {
            if (result.isConfirmed) {
                setUsers(prev => prev.filter(u => u.id !== id));
                if (activeUserId === id) setActiveUserId(null);
                Swal.fire({
                    title: 'حذف شد!',
                    icon: 'success',
                    timer: 1500,
                    showConfirmButton: false,
                    background: theme === 'dark' ? '#1e293b' : '#fff',
                    color: theme === 'dark' ? '#fff' : '#000'
                });
            }
        });
    };

    // --- Templates ---
    const saveTemplate = (name, workout) => {
        setTemplates(prev => [...prev, { id: Date.now(), name, workout }]);
        toast.success('الگو ذخیره شد');
    };
    const deleteTemplate = (id) => {
        setTemplates(prev => prev.filter(t => t.id !== id));
        toast.success('الگو حذف شد');
    };

    // --- Print ---
    const handlePrintPreview = (type) => {
        if (!activeUser) return toast.error('لطفا یک شاگرد را انتخاب کنید');
        const html = generatePrintHTML(activeUser, type);
        setPrintData({ html });
    };

    const downloadPDF = async () => {
        const element = document.getElementById('print-content-area');
        if (!element) {
            toast.error('محتوایی برای چاپ یافت نشد');
            return;
        }
        
        try {
            toast.loading('در حال ساخت PDF...', { id: 'pdf' });
            
            // تنظیمات html2canvas برای کیفیت بهتر
            const canvas = await html2canvas(element, { 
                scale: 2, 
                useCORS: true, 
                backgroundColor: '#ffffff',
                logging: false,
                allowTaint: true,
                scrollX: 0,
                scrollY: 0,
                windowWidth: element.scrollWidth,
                windowHeight: element.scrollHeight
            });
            
            const imgData = canvas.toDataURL('image/png', 1.0);
            const pdf = new jsPDF('p', 'mm', 'a4');
            
            const pdfWidth = 210;
            const pdfHeight = 297;
            const margin = 0;
            
            const imgWidth = canvas.width;
            const imgHeight = canvas.height;
            
            // محاسبه نسبت برای فیت کردن در عرض صفحه
            const ratio = (pdfWidth - margin * 2) / imgWidth;
            const scaledHeight = imgHeight * ratio;
            
            // اگر محتوا از یک صفحه بیشتره، چند صفحه بساز
            let yPosition = 0;
            let pageCount = 0;
            const pageHeightPx = pdfHeight / ratio; // ارتفاع هر صفحه به پیکسل
            
            while (yPosition < imgHeight) {
                if (pageCount > 0) {
                    pdf.addPage();
                }
                
                // برش بخشی از تصویر برای این صفحه
                const sourceY = yPosition;
                const sourceHeight = Math.min(pageHeightPx, imgHeight - yPosition);
                
                // ساخت canvas موقت برای این صفحه
                const pageCanvas = document.createElement('canvas');
                pageCanvas.width = imgWidth;
                pageCanvas.height = sourceHeight;
                const ctx = pageCanvas.getContext('2d');
                ctx.drawImage(canvas, 0, sourceY, imgWidth, sourceHeight, 0, 0, imgWidth, sourceHeight);
                
                const pageImgData = pageCanvas.toDataURL('image/png', 1.0);
                const pageScaledHeight = sourceHeight * ratio;
                
                pdf.addImage(pageImgData, 'PNG', margin, 0, pdfWidth - margin * 2, pageScaledHeight);
                
                yPosition += pageHeightPx;
                pageCount++;
            }
            
            pdf.save(`FlexPro_${activeUser.name}_${new Date().toLocaleDateString('fa-IR')}.pdf`);
            toast.success(`PDF با ${pageCount} صفحه ذخیره شد`, { id: 'pdf' });
        } catch (err) {
            toast.error('خطا در ساخت PDF: ' + err.message, { id: 'pdf' });
            console.error(err);
        }
    };

    const toggleThemeFn = () => {
        const t = theme === 'dark' ? 'light' : 'dark';
        setTheme(t);
        localStorage.setItem('flexTheme', t);
        document.documentElement.classList.toggle('dark', t === 'dark');
    };

    const logoutUser = () => {
        setActiveUserId(null);
        setCurrentTab('users');
        toast.success('ورزشکار فعال خارج شد');
    };

    const resetSystem = () => {
        Swal.fire({
            title: 'بازنشانی کارخانه؟',
            text: "تمام اطلاعات پاک می‌شود!",
            icon: 'error',
            showCancelButton: true,
            confirmButtonText: 'بله، ریست کن',
            cancelButtonText: 'لغو'
        }).then((res) => {
            if(res.isConfirmed) {
                // فقط داده‌های مربوط به FLEX PRO پاک می‌شود
                localStorage.removeItem(STORAGE_KEY);
                localStorage.removeItem('flexTheme');
                window.location.reload();
            }
        });
    };

    return (
        <AppContext.Provider value={{
            users, activeUser, currentTab, theme, templates,
            setActiveUserId, setCurrentTab,
            saveUser, deleteUser, updateActiveUser,
            saveTemplate, deleteTemplate,
            toggleTheme: toggleThemeFn,
            logoutUser,
            backupData: () => {
                const raw = localStorage.getItem(STORAGE_KEY);
                if (!raw) {
                    toast.error('بکاپی برای ذخیره‌سازی وجود ندارد');
                    return;
                }
                const blob = new Blob([raw], {type: 'application/json'});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a'); a.href = url; a.download = 'backup.json'; a.click();
            },
            restoreData: (f) => {
                const r = new FileReader();
                r.onload = e => {
                    try {
                        const text = e.target.result;
                        const parsed = JSON.parse(text);
                        if (!parsed || typeof parsed !== 'object' || !Array.isArray(parsed.users)) {
                            throw new Error('invalid backup structure');
                        }
                        Swal.fire({
                            title: 'بازیابی بکاپ؟',
                            text: 'تمام اطلاعات فعلی با بکاپ جایگزین می‌شود.',
                            icon: 'warning',
                            showCancelButton: true,
                            confirmButtonText: 'بله، بازیابی کن',
                            cancelButtonText: 'لغو',
                            background: theme === 'dark' ? '#1e293b' : '#fff',
                            color: theme === 'dark' ? '#fff' : '#000'
                        }).then(res => {
                            if (res.isConfirmed) {
                                localStorage.setItem(STORAGE_KEY, text);
                                window.location.reload();
                            }
                        });
                    } catch (err) {
                        console.error(err);
                        toast.error('فایل بکاپ معتبر نیست');
                    }
                };
                r.readAsText(f);
            },
            resetSystem,
            // Print Props
            printData, handlePrintPreview, closePrintModal: () => setPrintData(null), downloadPDF
        }}>
            {children}
        </AppContext.Provider>
    );
};

export const useApp = () => useContext(AppContext);