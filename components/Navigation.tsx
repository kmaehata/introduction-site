'use client'

import { useState, useEffect } from 'react'
import { usePathname } from 'next/navigation'
import Link from 'next/link'
import styles from './Navigation.module.css'

const links = [
  { href: '/', label: 'Top' },
  { href: '/education/', label: 'Education' },
  { href: '/background/', label: 'Background' },
  { href: '/skill/', label: 'Skill' },
  { href: '/portfolio/', label: 'Portfolio' },
]

// 画面上部に浮かぶ、すりガラスのメニュー
export default function Navigation() {
  const pathname = usePathname()
  const [isOpen, setIsOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    setIsOpen(false)
  }, [pathname])

  // 少しスクロールしたら、メニューの背景を濃くする
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const isActive = (href: string) =>
    href === '/' ? pathname === '/' : pathname?.startsWith(href.replace(/\/$/, ''))

  return (
    <header className={styles.wrap}>
      <div className={`${styles.bar} ${scrolled ? styles.scrolled : ''}`}>
        <Link href="/" className={styles.logo} aria-label="トップへ">
          <span className={styles.logoMark}>KM</span>
          <span className={styles.logoText}>Cloud &amp; AI Engineer</span>
        </Link>

        <nav className={styles.links} aria-label="メインメニュー">
          {links.map(({ href, label }) => (
            <Link key={href} href={href} className={`${styles.link} ${isActive(href) ? styles.active : ''}`}>
              {label}
            </Link>
          ))}
        </nav>

        <span className={styles.status}>
          <span className={styles.dot} />
          Available
        </span>

        <button
          type="button"
          className={`${styles.menuBtn} ${isOpen ? styles.menuOpen : ''}`}
          onClick={() => setIsOpen(!isOpen)}
          aria-label="メニューを開く"
          aria-expanded={isOpen}
        >
          <span />
          <span />
        </button>
      </div>

      {isOpen && (
        <nav className={styles.sheet} aria-label="メニュー">
          {links.map(({ href, label }) => (
            <Link key={href} href={href} className={`${styles.sheetLink} ${isActive(href) ? styles.active : ''}`}>
              {label}
              <span aria-hidden="true">→</span>
            </Link>
          ))}
        </nav>
      )}
    </header>
  )
}
