import Link from 'next/link'
import { projects } from '@/data/portfolio'
import styles from './page.module.css'

export default function PortfolioPage() {
  return (
    <div className={styles.page}>
      <div className={styles.pageHeader}>
        <p className={styles.eyebrow}>Works</p>
        <h1 className={styles.title}>Portfolio</h1>
        <p className={styles.subtitle}>作ったもの、育てているもの</p>
      </div>

      <div className={styles.grid}>
        {projects.map((p) => {
          const latest = p.versions[0]
          const cover = latest.docs.find((d) => d.id === 'business')?.slides[1] ?? latest.docs[0].slides[0]
          const pages = latest.docs.reduce((n, d) => n + d.slides.length, 0)
          return (
            <Link key={p.slug} href={`/portfolio/${p.slug}/`} className={styles.card}>
              <div className={styles.thumb}>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={cover.src} alt={cover.title} loading="lazy" />
                <span className={styles.version}>Version {latest.version}</span>
              </div>
              <div className={styles.body}>
                <p className={styles.kicker}>{p.subtitle}</p>
                <h2 className={styles.cardTitle}>{p.title}</h2>
                <p className={styles.summary}>{p.summary}</p>
                <div className={styles.tags}>
                  {p.tags.map((t) => (
                    <span key={t} className={styles.tag}>{t}</span>
                  ))}
                </div>
                <div className={styles.meta}>
                  <span className={styles.status}>{p.status}</span>
                  <span>資料 {latest.docs.length}点・{pages}枚</span>
                  <span className={styles.more}>詳しく見る →</span>
                </div>
              </div>
            </Link>
          )
        })}

        <div className={styles.soon}>
          <p className={styles.soonLabel}>COMING SOON</p>
          <p className={styles.soonText}>次の作品を準備しています</p>
        </div>
      </div>
    </div>
  )
}
