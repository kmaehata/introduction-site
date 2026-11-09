'use client'

import { useState } from 'react'
import Link from 'next/link'
import { companies, education, type Company, type Project, type SchoolEntry } from '@/data/career'
import styles from './CareerTimeline.module.css'

type Filter = 'all' | 'work' | 'education'

// 年号とタイトルだけを並べ、押すと解説が開く年表
export default function CareerTimeline() {
  const [filter, setFilter] = useState<Filter>('all')
  // 開いている項目。最初は最新の職歴だけ開いておく
  const [open, setOpen] = useState<Set<string>>(new Set([`work-${companies.length - 1}`]))

  const toggle = (id: string) =>
    setOpen((prev) => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })

  const allIds = [
    ...education.map((_, i) => `edu-${i}`),
    ...companies.map((_, i) => `work-${i}`),
  ]
  const allOpen = allIds.every((id) => open.has(id))

  return (
    <div className={styles.page}>
      <header className={styles.pageHeader}>
        <p className={styles.eyebrow}>Timeline</p>
        <h1 className={styles.title}>Career</h1>
        <p className={styles.subtitle}>学歴と職歴 ・ 2004 – NOW</p>
      </header>

      <div className={styles.toolbar}>
        <div className={styles.filter} role="tablist" aria-label="表示する経歴">
          {([
            ['all', 'すべて'],
            ['work', '職歴'],
            ['education', '学歴'],
          ] as [Filter, string][]).map(([f, label]) => (
            <button
              key={f}
              type="button"
              role="tab"
              aria-selected={filter === f}
              className={filter === f ? styles.filterActive : ''}
              onClick={() => setFilter(f)}
            >
              {label}
            </button>
          ))}
        </div>
        <button
          type="button"
          className={styles.expandAll}
          onClick={() => setOpen(allOpen ? new Set() : new Set(allIds))}
        >
          {allOpen ? 'すべて閉じる' : 'すべて開く'}
        </button>
      </div>

      <div className={styles.timeline}>
        {filter !== 'work' && (
          <>
            <p className={styles.section}>Education</p>
            {education.map((e, i) => (
              <SchoolItem key={e.year} entry={e} open={open.has(`edu-${i}`)} onToggle={() => toggle(`edu-${i}`)} />
            ))}
          </>
        )}

        {filter !== 'education' && (
          <>
            <p className={styles.section}>Work</p>
            {companies.map((c, i) => (
              <CompanyItem key={c.name} company={c} open={open.has(`work-${i}`)} onToggle={() => toggle(`work-${i}`)} />
            ))}
          </>
        )}
      </div>
    </div>
  )
}

// 開閉する見出しの行(年・タイトル・補足・矢印)
function Row({ when, title, note, open, onToggle, accent }: {
  when: string
  title: string
  note?: string
  open: boolean
  onToggle: () => void
  accent?: boolean
}) {
  return (
    <button type="button" className={styles.row} onClick={onToggle} aria-expanded={open}>
      <span className={`${styles.node} ${accent ? styles.nodeAccent : ''}`} aria-hidden="true" />
      <span className={styles.when}>{when}</span>
      <span className={styles.rowTitle}>
        {title}
        {note && <span className={styles.note}>{note}</span>}
      </span>
      <span className={`${styles.chevron} ${open ? styles.chevronOpen : ''}`} aria-hidden="true" />
    </button>
  )
}

// 開閉する中身(高さをなめらかに変える)
function Panel({ open, children }: { open: boolean; children: React.ReactNode }) {
  return (
    <div className={`${styles.panel} ${open ? styles.panelOpen : ''}`}>
      <div className={styles.panelInner}>{children}</div>
    </div>
  )
}

function SchoolItem({ entry, open, onToggle }: { entry: SchoolEntry; open: boolean; onToggle: () => void }) {
  return (
    <article className={`${styles.item} ${open ? styles.itemOpen : ''}`}>
      <Row when={entry.year} title={entry.title} open={open} onToggle={onToggle} />
      <Panel open={open}>
        <div className={styles.body}>
          {entry.paragraphs.map((p, i) => (
            <p key={i} className={styles.paragraph}>{p}</p>
          ))}
        </div>
      </Panel>
    </article>
  )
}

function CompanyItem({ company, open, onToggle }: { company: Company; open: boolean; onToggle: () => void }) {
  const [openProject, setOpenProject] = useState<number | null>(null)

  return (
    <article className={`${styles.item} ${styles.company} ${open ? styles.itemOpen : ''}`}>
      <Row when={company.period} title={company.name} note={company.employment} open={open} onToggle={onToggle} accent />
      <Panel open={open}>
        <div className={styles.body}>
          <p className={styles.lead}>{company.lead}</p>

          <div className={styles.block}>
            <p className={styles.label}>役割</p>
            <div className={styles.roles}>
              {company.roles.map((r) => (
                <span key={r} className={styles.role}>{r}</span>
              ))}
            </div>
          </div>

          <div className={styles.block}>
            <p className={styles.label}>活かしたスキル</p>
            <div className={styles.chips}>
              {company.skills.map((s) => (
                <span key={s} className={styles.chip}>{s}</span>
              ))}
            </div>
          </div>

          <div className={styles.block}>
            <p className={styles.label}>
              案件 <span className={styles.count}>{company.projects.length}</span>
            </p>
            <div className={styles.projects}>
              {company.projects.map((p, i) => (
                <ProjectItem
                  key={p.title}
                  project={p}
                  open={openProject === i}
                  onToggle={() => setOpenProject(openProject === i ? null : i)}
                />
              ))}
            </div>
          </div>

          {company.employment === 'Freelance' && (
            <Link href="/portfolio/" className={styles.portfolioLink}>
              個人開発: AIトレードデスク(マルチエージェント自律取引システム)を見る <span aria-hidden="true">→</span>
            </Link>
          )}
        </div>
      </Panel>
    </article>
  )
}

function ProjectItem({ project, open, onToggle }: { project: Project; open: boolean; onToggle: () => void }) {
  return (
    <div className={`${styles.project} ${open ? styles.projectOpen : ''}`}>
      <button type="button" className={styles.projectHead} onClick={onToggle} aria-expanded={open}>
        <span className={styles.projectTitle}>{project.title}</span>
        <span className={styles.projectMeta}>
          {project.period} ・ {project.team}
        </span>
        <span className={`${styles.chevron} ${styles.chevronSmall} ${open ? styles.chevronOpen : ''}`} aria-hidden="true" />
      </button>
      <Panel open={open}>
        <div className={styles.projectBody}>
          <ul className={styles.summary}>
            {project.summary.map((s) => (
              <li key={s}>{s}</li>
            ))}
          </ul>
          <div className={styles.chips}>
            {project.tech.map((t) => (
              <span key={t} className={`${styles.chip} ${styles.chipSmall}`}>{t}</span>
            ))}
          </div>
        </div>
      </Panel>
    </div>
  )
}
