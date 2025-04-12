import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Sidebar from './components/Sidebar';
import { AuthProvider } from './lib/auth/auth-context';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'MSPAlwaysOn',
  description: 'Unified AIOps and alert management platform for MSPs',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <div className="flex h-screen bg-gray-50">
            <Sidebar />
            <main className="flex-1 overflow-auto">
              {children}
              <ToastContainer />
            </main>
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
