import styles from './page.module.css'

export default function PortfolioPage() {
  return (
    <div className={styles.page}>
      <div className={styles.pageHeader}>
        <h1 className={styles.title}>PORTFOLIO</h1>
        <p className={styles.subtitle}>WORKS</p>
      </div>

      <div className={styles.wipCard}>
        <div className={styles.wipInner}>
          <p className={styles.wipLabel}>UNDER CONSTRUCTION</p>
          <p className={styles.wipText}>制作中です。しばらくお待ちください。</p>
        </div>
      </div>
    </div>
  )
}
