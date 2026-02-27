import styles from './TimelinePage.module.css'

export interface TimelineEntry {
  year: string
  imageSrc?: string
  portrait?: boolean
  paragraphs: string[]
}

interface Props {
  title: string
  subtitle: string
  entries: TimelineEntry[]
}

export default function TimelinePage({ title, subtitle, entries }: Props) {
  return (
    <div className={styles.page}>
      <div className={styles.pageHeader}>
        <h1 className={styles.title}>{title}</h1>
        <p className={styles.subtitle}>{subtitle}</p>
      </div>

      <div className={styles.timeline}>
        {entries.map(entry => (
          <div key={entry.year} className={styles.entry}>
            {/* Year + node */}
            <div className={styles.yearBlock}>
              <span className={styles.year}>{entry.year}</span>
              <div className={styles.node} />
            </div>

            {/* Glass card */}
            <div className={styles.card}>
              <div className={styles.cardInner}>
                {entry.imageSrc && (
                  <div className={`${styles.imageSection} ${entry.portrait ? styles.portrait : ''}`}>
                    <img
                      src={entry.imageSrc}
                      alt={entry.year}
                      className={styles.cardImage}
                    />
                  </div>
                )}
                <div className={entry.imageSrc ? styles.textSection : styles.textSectionFull}>
                  <div className={styles.paragraphs}>
                    {entry.paragraphs.map((p, i) => (
                      <p key={i} className={styles.paragraph}>{p}</p>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
