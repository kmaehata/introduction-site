import styles from './TabContent.module.css'

export default function CloudEngineer() {
  return (
    <div className={styles.tabContent}>
      <h2 className={styles.title}>IT戦士(クラウド系)</h2>
      
      <div className={styles.section}>
        <p>
          <strong>Kyla株式会社</strong>よりオファーをいただき、
          人生で初めて正社員としてのキャリアをスタートしました。
          本職を通じて、IT分野における自身の志向や、今後のキャリアの方向性が明確になっていきました。
        </p>
      </div>

      <div className={styles.section}>
        <p>
          もともと「PCを使い、技術で価値を生み出す仕事をしたい」という思いを持っていましたが、
          実務を経験する中で、特定領域に限定されない <strong>幅広い技術を扱えるエンジニア</strong> を目指すようになりました。
        </p>
      </div>

      <div className={styles.section}>
        <h3 className={styles.subtitle}>在籍中の主な業務</h3>
        <ul className={styles.list}>
          <li>クラウド環境を前提としたバックエンド開発</li>
          <li>インフラ設計・運用</li>
          <li>Django を用いたフロントエンドを含むWeb開発</li>
          <li>データ処理・連携を含むシステム実装</li>
        </ul>
        <p>
          いわゆる<strong>フルスタック</strong>寄りの立場で、
          複数の技術領域を横断しながら業務を担当していました。
        </p>
      </div>

      <div className={styles.section}>
        <h3 className={styles.subtitle}>技術志向の変化と次の挑戦</h3>
        <p>
          2022年に ChatGPT が公開され、生成AI分野が急速に発展していく中で、
          私はこの技術革新を「一時的な流行」ではなく、<strong>ITの在り方そのものを変える転換点</strong>だと捉えました。
        </p>
      </div>

      <div className={styles.section}>
        <p>
          これまで正社員としてのポジションを得るため努力してきましたが、
          それ以上に重要だと感じるようになったのが、
          <strong>常に新しい技術に向き合い、学び続ける姿勢</strong>でした。
        </p>
      </div>

      <div className={styles.section}>
        <p>
          幅広い技術を扱うエンジニアとして成長するためには、
          生成AIという新しい分野に早い段階から関わることが必要だと判断し、
          自らの意思で次の挑戦へ進む決断をしました。
        </p>
      </div>

      <div className={styles.section}>
        <p>
          その後、<strong>AIタレントフォース株式会社</strong>よりオファーをいただき、
          転職という形で新たなチャレンジに取り組むこととなりました。
        </p>
      </div>
    </div>
  )
}
