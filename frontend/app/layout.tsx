import './globals.css';

import Nav from './nav';
import AnalyticsWrapper from './analytics';
import { Suspense } from 'react';
import { AppContext, AppProvider } from '../store/app_provider';

export const metadata = {
  title: 'StockMate',
  description:
    'StockMate'
};

export default async function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full bg-gray-50">
      <body className="h-full">
        <Suspense fallback="...">
          {/* @ts-expect-error Server Component */}
          <Nav />
        </Suspense>
        <AppProvider>
          {children}
        </AppProvider>
        <AnalyticsWrapper />

      </body>
    </html>
  );
}
