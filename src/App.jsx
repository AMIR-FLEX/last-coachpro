import React, { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import { useApp } from './context/AppContext';

// ایمپورت کامپوننت‌ها
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import UserList from './components/UserList';
import TrainingPanel from './components/TrainingPanel';
import DietPanel from './components/DietPanel';
import SupplementsPanel from './components/SupplementsPanel';
import UserModal from './components/UserModal';
import PrintModal from './components/PrintModal';
import ProfilePanel from './components/ProfilePanel';

// کامپوننت موقت برای بخش‌های توسعه نیافته
const PlaceholderComponent = ({ title, icon }) => (
  <div className="flex flex-col items-center justify-center h-full text-slate-400 glass-panel rounded-3xl m-4">
    <span className="text-7xl mb-6 opacity-50 drop-shadow-lg">{icon}</span>
    <span className="font-bold text-2xl text-[var(--text-primary)] mb-2">{title}</span>
    <span className="text-sm opacity-70">این ماژول در حال توسعه است...</span>
  </div>
);

function App() {
  const {
    theme, toggleTheme,
    currentTab, setCurrentTab,
    activeUser, users,
    saveUser, deleteUser, logoutUser, updateActiveUser,
    backupData, restoreData, resetSystem, setActiveUserId,
    handlePrintPreview, closePrintModal, printData, downloadPDF
  } = useApp();

  // مدیریت وضعیت‌های مودال کاربر
  const [isUserModalOpen, setIsUserModalOpen] = useState(false);
  const [editingUserId, setEditingUserId] = useState(null);

  const handleOpenUserModal = (id = null) => {
    setEditingUserId(id);
    setIsUserModalOpen(true);
  };

  const handleCloseUserModal = () => {
    setIsUserModalOpen(false);
    setEditingUserId(null);
  };

  const handleSaveUserForm = (formData) => {
    saveUser(formData);
    handleCloseUserModal();
  };

  const handleSelectUser = (id) => {
    setActiveUserId(id);
    setCurrentTab('training');
  };

  return (
    <div className={`flex flex-col h-screen overflow-hidden text-[var(--text-primary)] font-sans transition-colors duration-300 relative selection:bg-sky-500/30 selection:text-sky-200 ${theme}`}>
      
      {/* کامپوننت نمایش نوتیفیکیشن‌ها */}
      <Toaster position="bottom-left" toastOptions={{ style: { background: '#334155', color: '#fff', borderRadius: '10px' } }} />

      {/* پس‌زمینه متحرک */}
      <div className="bg-gradient-animated"></div>
      
      {/* گوی‌های رنگی پس‌زمینه برای زیبایی بیشتر */}
      <div className="orb orb-1"></div>
      <div className="orb orb-2"></div>
      
      {/* روکش گرادینت ملایم */}
      <div className="fixed inset-0 bg-[var(--bg-primary)]/80 z-[-1] transition-colors duration-500"></div>

      {/* هدر */}
      <Header
        toggleTheme={toggleTheme}
        isDark={theme === 'dark'}
        activeUser={activeUser}
        onLogout={logoutUser}
      />

      <div className="flex flex-1 overflow-hidden">
        
        {/* سایدبار */}
        <Sidebar
          currentTab={currentTab}
          setTab={setCurrentTab}
          onBackup={backupData}
          onRestore={(e) => restoreData(e.target.files[0])}
          onReset={resetSystem}
        />

        {/* محتوای اصلی */}
        <main className="flex-1 overflow-y-auto p-4 lg:p-8 relative scroll-smooth">
          
          {currentTab === 'users' && (
            <UserList
              users={users}
              onSelectUser={handleSelectUser}
              onAddUser={() => handleOpenUserModal(null)}
              onEditUser={handleOpenUserModal}
              onDeleteUser={deleteUser}
              onPrintUser={(id) => { setActiveUserId(id); handlePrintPreview('profile'); }}
            />
          )}

          {/* دکمه‌های شناور چاپ (فقط وقتی تب‌های برنامه فعال است) */}
          {activeUser && currentTab !== 'users' && (
             <div className="absolute top-6 left-10 z-20 flex gap-2">
                {currentTab === 'training' && <button onClick={() => handlePrintPreview('training')} className="btn-glass bg-white/5 hover:bg-white/10 text-xs border border-white/10">🖨️ چاپ برنامه</button>}
                {currentTab === 'nutrition' && <button onClick={() => handlePrintPreview('nutrition')} className="btn-glass bg-white/5 hover:bg-white/10 text-xs border border-white/10">🖨️ چاپ رژیم</button>}
                {currentTab === 'supplements' && <button onClick={() => handlePrintPreview('supplements')} className="btn-glass bg-white/5 hover:bg-white/10 text-xs border border-white/10">🖨️ چاپ نسخه</button>}
             </div>
          )}

          {currentTab === 'training' && activeUser && (
            <TrainingPanel
              activeUser={activeUser}
              onUpdateUser={updateActiveUser}
            />
          )}

          {currentTab === 'nutrition' && activeUser && (
            <DietPanel
              activeUser={activeUser}
              onUpdateUser={updateActiveUser}
            />
          )}

          {currentTab === 'supplements' && activeUser && (
            <SupplementsPanel
              activeUser={activeUser}
              onUpdateUser={updateActiveUser}
            />
          )}

          {currentTab === 'progress' && activeUser && (
            <ProfilePanel
              activeUser={activeUser}
              onUpdateUser={updateActiveUser}
            />
          )}

          {/* صفحه خالی وقتی کاربری انتخاب نشده */}
          {currentTab !== 'users' && !activeUser && (
            <div className="flex flex-col items-center justify-center h-full text-slate-400 glass-panel rounded-3xl m-4">
              <p className="text-lg mb-4">لطفا ابتدا یک ورزشکار را انتخاب کنید.</p>
              <button onClick={() => setCurrentTab('users')} className="btn-glass btn-primary">
                بازگشت به لیست شاگردان
              </button>
            </div>
          )}

        </main>
      </div>

      {/* مودال فرم کاربر */}
      {isUserModalOpen && (
        <UserModal
          isOpen={isUserModalOpen}
          onClose={handleCloseUserModal}
          onSave={handleSaveUserForm}
          initialData={editingUserId ? users.find(u => u.id === editingUserId) : null}
        />
      )}

      {/* مودال پیش‌نمایش چاپ */}
      {printData && (
          <PrintModal
            data={printData}
            onClose={closePrintModal}
            onDownload={downloadPDF}
          />
      )}

    </div>
  );
}

export default App;