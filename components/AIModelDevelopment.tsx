import styles from './TabContent.module.css'

export default function AIModelDevelopment() {
  return (
    <div className={styles.tabContent}>
      <h2 className={styles.title}>AIモデルの開発経験</h2>
      
      <div className={styles.section}>
        <p>
          大学卒業当時は新型コロナウイルスの影響もあり、就職環境が非常に厳しい状況でした。
          その中で「正社員という形にこだわらず、まずは実務経験を積むのも一つの選択肢ではないか」という助言を受け、
          大学研究で培った Deep Q-Learning の知識を活かせる環境を探しました。
        </p>
      </div>

      <div className={styles.section}>
        <p>
          その結果、<strong>ニューロンネットワーク株式会社</strong>とご縁があり、
          アルバイトとしてAIモデル開発業務に携わることになりました。
        </p>
      </div>

      <div className={styles.section}>
        <p>
          本業務では、<strong>マルチ画像分類モデルの研究・開発</strong>を担当しました。
          実務経験がほぼない状態からのスタートでしたが、課題に対して仮説を立て、
          実装・検証・評価を繰り返しながら、モデル精度の向上に取り組みました。
        </p>
      </div>

      <div className={styles.section}>
        <h3 className={styles.subtitle}>主な技術スタック</h3>
        <ul className={styles.list}>
          <li>Python</li>
          <li>PyTorch / TensorFlow</li>
          <li>OpenCV、NumPy、Matplotlib などの画像処理・可視化ライブラリ</li>
        </ul>
      </div>

      <div className={styles.section}>
        <p>
          対象とする画像は構造が複雑で、かつ分類ラベルも多岐にわたっていたため、精度向上の難易度が高いプロジェクトでした。
          開発を進める中で、特定のラベルに対してモデルが分類しづらい傾向があることを分析し、
          データセットの品質やラベル構成がモデル性能に大きく影響することを実感しました。
        </p>
      </div>

      <div className={styles.section}>
        <p>
          こうした知見を通じて、
          モデルの特性理解、データ前処理の重要性、評価結果から次の改善策を導く思考力など、
          研究開発に必要な基礎力を実務の中で身につけることができました。
        </p>
      </div>

      <div className={styles.section}>
        <p>
          その後、これらの経験を評価いただき、別企業よりオファーを受け、
          人生で初めて<strong>正社員</strong>としてのキャリアに進む決断をしました。
        </p>
      </div>
    </div>
  )
}
