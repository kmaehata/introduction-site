import type { Metadata, Viewport } from 'next'
import Navigation from '@/components/Navigation'
import styles from './layout.module.css'
import './globals.css'

export const metadata: Metadata = {
  title: 'KM',
  description: 'Cloud & AI Engineer Portfolio',
}

// iPhone の画面の端(ノッチ・ホームバー)まで使い、ブラウザの色をサイトに合わせる
export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  viewportFit: 'cover',
  themeColor: '#050816',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <head>
        {/* 書体(見出し: Space Grotesk、本文: Inter)。
            next/font はビルド時の取得が CI で不安定に失敗するため、使わずに直接読み込む */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        {/* eslint-disable-next-line @next/next/no-page-custom-font */}
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap" />
      </head>
      <body>
        {/* 背景のオーロラ */}
        <div className="aurora" aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
        <Navigation />
        <main className={styles.main}>{children}</main>
        <footer className={styles.footer}>
          <span>© KM</span>
          <span>Cloud &amp; AI Engineer</span>
        </footer>
      </body>
    </html>
  )
}
