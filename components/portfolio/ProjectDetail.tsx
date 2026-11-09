'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { audienceLabel, type Audience, type Doc, type Project } from '@/data/portfolio'
import SlideViewer from './SlideViewer'
import styles from './ProjectDetail.module.css'

type Filter = 'all' | Audience

const PREVIEW_COUNT = 4 // 見出しを何件まで見せるか

export default function ProjectDetail({ project }: { project: Project }) {
  const [versionId, setVersionId] = useState(project.versions[0].version)
  const [filter, setFilter] = useState<Filter>('all')
  const [open, setOpen] = useState<{ doc: Doc; index: number } | null>(null)

  // URL の #v1.0 で版を指定できるようにする(共有しやすくするため)
  useEffect(() => {
    const v = window.location.hash.replace(/^#v/, '')
    if (project.versions.some((x) => x.version === v)) setVersionId(v)
  }, [project.versions])

  const selectVersion = (v: string) => {
    setVersionId(v)
    window.history.replaceState(null, '', `#v${v}`)
  }

  const version = project.versions.find((v) => v.version === versionId) ?? project.versions[0]
  const latest = project.versions[0].version
  const docs = useMemo(
    () => version.docs.filter((d) => filter === 'all' || d.audience.includes(filter)),
    [version, filter],
  )

  return (
    <div className={styles.page}>
      <nav className={styles.crumb}>
        <Link href="/portfolio/">PORTFOLIO</Link>
        <span>/</span>
        <span>{project.title}</span>
      </nav>

      <header className={styles.hero}>
        <p className={styles.kicker}>{project.subtitle}</p>
        <h1 className={styles.title}>{project.title}</h1>
        <p className={styles.summary}>{project.summary}</p>
        <div className={styles.heroMeta}>
          <span className={styles.status}>{project.status}</span>
          <span className={styles.latest}>最新 Version {latest}</span>
        </div>
        <div className={styles.stack}>
          {project.stack.map((s) => (
            <span key={s}>{s}</span>
          ))}
        </div>
        {project.links && (
          <div className={styles.links}>
            {project.links.map((l) => (
              <a key={l.href} href={l.href} target="_blank" rel="noopener noreferrer" className={styles.linkBtn}>
                <span className={styles.linkLabel}>
                  {l.label} <span aria-hidden="true">↗</span>
                </span>
                {l.note && <span className={styles.linkNote}>{l.note}</span>}
              </a>
            ))}
          </div>
        )}
      </header>

      {/* 版の切り替え。新しい版ほど左に並ぶ */}
      <section className={styles.versions} aria-label="バージョン">
        <p className={styles.sectionLabel}>VERSIONS</p>
        <div className={styles.versionRail}>
          {project.versions.map((v) => (
            <button
              key={v.version}
              type="button"
              className={`${styles.versionChip} ${v.version === version.version ? styles.versionActive : ''}`}
              onClick={() => selectVersion(v.version)}
              aria-pressed={v.version === version.version}
            >
              <span className={styles.versionNo}>Version {v.version}</span>
              <span className={styles.versionDate}>{v.date}</span>
              {v.version === latest && <span className={styles.newBadge}>最新</span>}
            </button>
          ))}
          <div className={styles.versionNext}>次の版を準備中…</div>
        </div>

        <div className={styles.release}>
          <h2 className={styles.releaseTitle}>
            <span>v{version.version}</span>
            {version.title}
          </h2>
          <ul className={styles.highlights}>
            {version.highlights.map((h) => (
              <li key={h}>{h}</li>
            ))}
          </ul>
        </div>
      </section>

      {/* 資料 */}
      <section aria-label="資料">
        <div className={styles.docsHead}>
          <p className={styles.sectionLabel}>DOCUMENTS</p>
          <div className={styles.filter} role="tablist" aria-label="読む人で絞り込む">
            {(['all', 'engineer', 'business'] as Filter[]).map((f) => (
              <button
                key={f}
                type="button"
                role="tab"
                aria-selected={filter === f}
                className={filter === f ? styles.filterActive : ''}
                onClick={() => setFilter(f)}
              >
                {f === 'all' ? 'すべて' : audienceLabel[f]}
              </button>
            ))}
          </div>
        </div>

        <div className={styles.docs}>
          {docs.map((d) => {
            const body = d.slides.slice(1) // 1枚目は表紙
            return (
              <article key={d.id} className={styles.doc}>
                <button type="button" className={styles.docThumb} onClick={() => setOpen({ doc: d, index: 0 })} aria-label={`${d.title}をひらく`}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={d.slides[0].src} alt={`${d.title}の表紙`} loading="lazy" />
                  <span className={styles.docCount}>{d.slides.length}枚</span>
                </button>
                <div className={styles.docBody}>
                  <div className={styles.docTop}>
                    <span className={styles.docNo}>{d.no}</span>
                    <div className={styles.audiences}>
                      {d.audience.map((a) => (
                        <span key={a} className={a === 'engineer' ? styles.engineer : styles.business}>{audienceLabel[a]}</span>
                      ))}
                    </div>
                  </div>
                  <h3 className={styles.docTitle}>{d.title}</h3>
                  <p className={styles.docCatch}>{d.catch}</p>

                  {/* 見出しを少しだけ見せる。押すとそのページから読める */}
                  <ol className={styles.toc}>
                    {body.slice(0, PREVIEW_COUNT).map((s, i) => (
                      <li key={s.src}>
                        <button type="button" onClick={() => setOpen({ doc: d, index: i + 1 })}>
                          <span>{String(i + 1).padStart(2, '0')}</span>
                          {s.title}
                        </button>
                      </li>
                    ))}
                  </ol>
                  {body.length > PREVIEW_COUNT && (
                    <p className={styles.tocMore}>ほか {body.length - PREVIEW_COUNT} 枚 — 続きはスライドで</p>
                  )}

                  <div className={styles.docActions}>
                    <button type="button" className={styles.primary} onClick={() => setOpen({ doc: d, index: 0 })}>
                      スライドを見る
                    </button>
                    <a className={styles.secondary} href={d.pdf} target="_blank" rel="noopener noreferrer">
                      PDF
                    </a>
                  </div>
                </div>
              </article>
            )
          })}
        </div>
      </section>

      <section className={styles.note}>
        <p className={styles.sectionLabel}>SOURCE CODE</p>
        <p>{project.repoNote}</p>
      </section>

      {open && (
        <SlideViewer
          title={`${open.doc.title} ・ Version ${version.version}`}
          slides={open.doc.slides}
          pdf={open.doc.pdf}
          start={open.index}
          onClose={() => setOpen(null)}
        />
      )}
    </div>
  )
}
