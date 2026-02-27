import styles from './TabContent.module.css'

export default function UniversityResearch() {
  return (
    <div className={styles.tabContent}>
      <h2 className={styles.title}>大学卒業研究</h2>
      
      <div className={styles.section}>
        <p>
          大学では、<strong>強化学習(Deep Q-Learning)</strong>を用いた経路最適化をテーマに研究を行いました。
        </p>
      </div>

      <div className={styles.section}>
        <p>
          仮想マップ上において、エージェントが現在位置から目的地まで移動する際の最適なルートを、
          障害物や壁といった制約条件を考慮しながら、どのように導出できるかを検討しました。
        </p>
      </div>

      <div className={styles.section}>
        <h3 className={styles.subtitle}>研究プロセス</h3>
        <ul className={styles.list}>
          <li>課題設定(環境・制約条件の定義)</li>
          <li>学習理論の整理とアルゴリズム設計</li>
          <li>設計内容をもとにした実装</li>
          <li>学習結果・挙動の評価と考察</li>
        </ul>
      </div>

      <div className={styles.section}>
        <p>
          という一連のプロセスを通して、
          理論設計から実装・評価までを一貫して実施しました。
        </p>
      </div>

      <div className={styles.section}>
        <p>
          最終的には研究成果を発表し、
          あわせて改善点や拡張可能性を整理し、後続研究のテーマを明確化したうえで卒業しました。
        </p>
      </div>
    </div>
  )
}
