'use client';

import { useEffect, useRef } from 'react';

interface PrintModalProps {
  data: {
    html: string;
  } | null;
  onClose: () => void;
  onDownload: () => void;
}

export function PrintModal({ data, onClose, onDownload }: PrintModalProps) {
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (contentRef.current) {
      contentRef.current.scrollTop = 0;
    }
  }, [data]);

  if (!data) return null;

  const handleBrowserPrint = () => {
    const printContent = document.getElementById('print-content-area');
    if (!printContent) return;
    
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;
    
    printWindow.document.write(`
      <!DOCTYPE html>
      <html dir="rtl" lang="fa">
      <head>
        <meta charset="UTF-8">
        <title>FlexPro - چاپ برنامه</title>
        <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;700;900&display=swap" rel="stylesheet">
        <style>
          * { box-sizing: border-box; margin: 0; padding: 0; }
          body { font-family: 'Vazirmatn', sans-serif; direction: rtl; }
          @media print {
            body { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
            table { page-break-inside: auto; }
            tr { page-break-inside: avoid; page-break-after: auto; }
            thead { display: table-header-group; }
            .page-break { page-break-before: always; }
          }
        </style>
      </head>
      <body>
        ${printContent.innerHTML}
      </body>
      </html>
    `);
    printWindow.document.close();
    printWindow.focus();
    setTimeout(() => {
      printWindow.print();
      printWindow.close();
    }, 500);
  };

  return (
    <div className="fixed inset-0 z-[100] bg-slate-900/95 backdrop-blur-md flex flex-col animate-fade-in">
      <div className="h-16 bg-white/5 border-b border-white/10 flex justify-between items-center px-6 shrink-0">
        <h3 className="text-white font-bold flex items-center gap-2 text-lg">
          <span>🖨️</span> پیش‌نمایش چاپ
        </h3>
        <div className="flex gap-3">
          <button 
            onClick={onDownload} 
            className="btn-glass bg-emerald-600 hover:bg-emerald-500 text-white text-sm border border-emerald-500/30 shadow-lg"
          >
            📥 دانلود PDF
          </button>
          <button 
            onClick={handleBrowserPrint} 
            className="btn-glass bg-sky-600 hover:bg-sky-500 text-white text-sm border border-sky-500/30 shadow-lg"
          >
            🖨️ پرینت مرورگر
          </button>
          <button 
            onClick={onClose} 
            className="btn-glass bg-white/10 hover:bg-white/20 text-white text-sm"
          >
            ✕ بستن
          </button>
        </div>
      </div>

      <div 
        ref={contentRef}
        className="flex-1 overflow-y-auto p-8 flex justify-center bg-slate-800/50"
      >
        <div 
          id="print-content-area"
          className="bg-white text-black shadow-2xl mx-auto print-content"
          style={{ 
            width: '210mm', 
            minHeight: '297mm',
            padding: '0',
            boxSizing: 'border-box',
          }}
          dangerouslySetInnerHTML={{ __html: data.html }}
        />
      </div>

      <div className="h-12 bg-white/5 border-t border-white/10 flex items-center justify-center px-6 text-xs text-slate-400">
        <span>💡 برای بهترین کیفیت از دکمه «دانلود PDF» استفاده کنید</span>
      </div>
    </div>
  );
}

