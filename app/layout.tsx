import type { Metadata } from 'next';
import { Vazirmatn } from 'next/font/google';
import './globals.css';
import { Providers } from '@/components/providers';
import { Toaster } from 'react-hot-toast';

const vazirmatn = Vazirmatn({
  subsets: ['latin'],
  weight: ['100', '200', '300', '400', '500', '600', '700', '800', '900'],
  variable: '--font-vazirmatn',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'FLEX PRO - سیستم مدیریت مربیگری ورزشی',
  description: 'سیستم جامع مدیریت برنامه‌های تمرینی، تغذیه و مکمل‌های ورزشی',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fa" dir="rtl" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body className={`${vazirmatn.variable} font-sans`}>
        <Providers>
          {children}
          <Toaster
            position="bottom-left"
            toastOptions={{
              style: {
                background: '#334155',
                color: '#fff',
                borderRadius: '10px',
              },
            }}
          />
        </Providers>
      </body>
    </html>
  );
}

