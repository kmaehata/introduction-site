import type { Metadata } from 'next'
import { Playfair_Display, Inter } from 'next/font/google'
import Navigation from '@/components/Navigation'
import styles from './layout.module.css'
import './globals.css'

const playfair = Playfair_Display({
  subsets: ['latin'],
  variable: '--font-serif',
  display: 'swap',
})

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
  weight: ['300', '400'],
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'KOSEI MAEHATA',
  description: 'Cloud & AI Engineer Portfolio',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja" className={`${playfair.variable} ${inter.variable}`}>
      <body>
        <header className={styles.header}>
          <div className={styles.logo}>KOSEI MAEHATA</div>
          <div className={styles.subtext}>CLOUD &amp; AI ENGINEER</div>
        </header>
        <Navigation />
        <main className={styles.main}>{children}</main>
      </body>
    </html>
  )
}
