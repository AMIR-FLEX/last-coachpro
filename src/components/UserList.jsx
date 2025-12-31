import React, { useState } from 'react';
import { Search, UserPlus, Edit, Trash2, Printer, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';

const UserList = ({ users, onSelectUser, onAddUser, onEditUser, onDeleteUser, onPrintUser }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredUsers = users.filter(u => 
    u.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
    (u.phone && u.phone.includes(searchTerm))
  );

  const getFinancialStatus = (user) => {
      if (!user.financial?.startDate) return { text: 'نامشخص', color: 'text-slate-400 bg-slate-500/10', icon: <AlertTriangle size={16}/> };
      const start = new Date(user.financial.startDate);
      const end = new Date(start);
      end.setMonth(end.getMonth() + (user.financial.duration || 1));
      const now = new Date();
      const daysLeft = Math.ceil((end - now) / (1000 * 60 * 60 * 24));

      if (daysLeft < 0) return { text: 'منقضی شده', color: 'text-red-500 bg-red-500/10', icon: <XCircle size={16}/> };
      if (daysLeft <= 5) return { text: `${daysLeft} روز مانده`, color: 'text-yellow-500 bg-yellow-500/10', icon: <AlertTriangle size={16}/> };
      return { text: 'فعال', color: 'text-emerald-500 bg-emerald-500/10', icon: <CheckCircle size={16}/> };
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* هدر و جستجو */}
      <div className="flex flex-col md:flex-row justify-between items-center glass-panel p-5 rounded-2xl gap-4 sticky top-0 z-20">
        <div>
          <h2 className="text-2xl font-black text-[var(--text-primary)]">لیست شاگردان ({filteredUsers.length})</h2>
        </div>
        <div className="flex gap-3 w-full md:w-auto">
          <div className="relative flex-1 md:w-64">
            <input 
              type="text" 
              placeholder="جستجو..." 
              className="input-glass pl-10 py-2.5"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <Search className="absolute left-3 top-3 text-slate-400 w-4 h-4" />
          </div>
          <button onClick={() => onAddUser(null)} className="btn-glass bg-sky-600 hover:bg-sky-500 text-white text-sm py-2.5">
            <UserPlus size={18} /> جدید
          </button>
        </div>
      </div>

      {/* لیست کارت‌ها (افقی) */}
      <div className="flex flex-col gap-4">
          {filteredUsers.map(u => {
            const status = getFinancialStatus(u);
            return (
            <div key={u.id} className="glass-card flex flex-col md:flex-row items-center justify-between p-4 gap-4 group hover:border-sky-500/40">
              
              {/* بخش اطلاعات */}
              <div className="flex items-center gap-4 w-full md:w-auto">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-sky-500 to-blue-600 flex items-center justify-center text-white font-bold text-lg shadow-lg">
                      {u.name.charAt(0)}
                  </div>
                  <div>
                      <h3 className="font-bold text-lg text-[var(--text-primary)]">{u.name}</h3>
                      <div className="flex items-center gap-3 text-xs text-[var(--text-secondary)] mt-1">
                          <span className="flex items-center gap-1 bg-[var(--glass-border)] px-2 py-0.5 rounded">{u.age || '-'} ساله</span>
                          <span className="flex items-center gap-1 bg-[var(--glass-border)] px-2 py-0.5 rounded">{u.weight || '-'} kg</span>
                          <span className={`flex items-center gap-1 px-2 py-0.5 rounded font-bold ${status.color}`}>
                              {status.icon} {status.text}
                          </span>
                      </div>
                  </div>
              </div>

              {/* بخش دکمه‌ها */}
              <div className="flex items-center gap-2 w-full md:w-auto justify-end">
                <button 
                    onClick={() => onSelectUser(u.id)} 
                    className="btn-glass bg-sky-500/10 hover:bg-sky-500 hover:text-white text-sky-600 dark:text-sky-400 border border-sky-500/20 text-sm flex-1 md:flex-none"
                >
                  مدیریت برنامه
                </button>
                <button onClick={() => onEditUser(u.id)} className="p-2 rounded-lg bg-[var(--text-primary)]/5 hover:bg-[var(--text-primary)]/10 text-[var(--text-secondary)] transition" title="ویرایش">
                  <Edit size={18}/>
                </button>
                <button onClick={() => onPrintUser(u.id)} className="p-2 rounded-lg bg-[var(--text-primary)]/5 hover:bg-[var(--text-primary)]/10 text-[var(--text-secondary)] transition" title="چاپ">
                  <Printer size={18}/>
                </button>
                <button onClick={() => onDeleteUser(u.id)} className="p-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-500 transition" title="حذف">
                  <Trash2 size={18}/>
                </button>
              </div>
            </div>
          )})}
          
          {filteredUsers.length === 0 && (
              <div className="text-center py-10 opacity-50">موردی یافت نشد.</div>
          )}
      </div>
    </div>
  );
};

export default UserList;