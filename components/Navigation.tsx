'use client'

import { usePathname } from 'next/navigation'
import Link from 'next/link'
import styles from './Navigation.module.css'

const links = [
  { href: '/', label: 'TOP' },
  { href: '/education', label: 'EDUCATION', sub: '2004–2020' },
  { href: '/background', label: 'BACKGROUND', sub: '2020–NOW' },
  { href: '/skill', label: 'SKILL' },
  { href: '/portfolio', label: 'PORTFOLIO' },
]

export default function Navigation() {
  const pathname = usePathname()

  return (
    <nav className={styles.nav}>
      {links.map(({ href, label, sub }) => {
        const isActive = pathname === href
        return (
          <Link
            key={href}
            href={href}
            className={`${styles.link} ${isActive ? styles.active : ''}`}
          >
            <span className={styles.label}>{label}</span>
            {sub && <span className={styles.sub}>{sub}</span>}
          </Link>
        )
      })}
    </nav>
  )
}
