import styles from './TabContent.module.css'

export default function GenerativeAI() {
  return (
    <div className={styles.tabContent}>
      <h2 className={styles.title}>生成AIの強いエンジニア</h2>
      
      <div className={styles.section}>
        <p>
          <strong>フルスタックエンジニア</strong>として活動し、
          生成AIのプロジェクトをいくつか経験をし、
          チャットbotの開発などの実務経験がある状態で現在<strong>フリー</strong>で活動しております。
        </p>
      </div>

      <div className={styles.section}>
        <p className={styles.highlight}>
          生成AI技術を活用した実践的なソリューション開発に携わっています。
        </p>
      </div>
    </div>
  )
}
