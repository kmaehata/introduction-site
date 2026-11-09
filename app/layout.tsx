import type { Metadata } from 'next'
import { Space_Grotesk, Inter } from 'next/font/google'
import Navigation from '@/components/Navigation'
import styles from './layout.module.css'
import './globals.css'

const display = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-display',
  weight: ['400', '500', '600', '700'],
  display: 'swap',
})

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
  weight: ['300', '400', '500', '600'],
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'KM',
  description: 'Cloud & AI Engineer Portfolio',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja" className={`${display.variable} ${inter.variable}`}>
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
