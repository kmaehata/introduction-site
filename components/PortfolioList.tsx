import styles from './TabContent.module.css'

export default function PortfolioList() {
  return (
    <div className={styles.tabContent}>
      <h2 className={styles.title}>ポートフォリオ一覧</h2>
      
      <div className={styles.section}>
        <p>
          テスト(まだ何も用意してないのでいったんはこれで)
        </p>
      </div>

      <div className={styles.section}>
        <div className={styles.placeholder}>
          <p>🚧 準備中 🚧</p>
          <p className={styles.placeholderText}>
            今後、制作物や実績を追加予定です
          </p>
        </div>
      </div>
    </div>
  )
}
