'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import type { Slide } from '@/data/portfolio'
import styles from './SlideViewer.module.css'

type Props = {
  title: string
  slides: Slide[]
  pdf: string
  start: number
  onClose: () => void
}

// スライドを1枚ずつ大きく見せる。← → キー、スワイプ、下の一覧で移動できる
export default function SlideViewer({ title, slides, pdf, start, onClose }: Props) {
  const [index, setIndex] = useState(start)
  const touchX = useRef<number | null>(null)
  const stripRef = useRef<HTMLDivElement>(null)

  const go = useCallback(
    (n: number) => setIndex((i) => Math.min(slides.length - 1, Math.max(0, i + n))),
    [slides.length],
  )

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') go(1)
      if (e.key === 'ArrowLeft') go(-1)
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      window.removeEventListener('keydown', onKey)
      document.body.style.overflow = prev
    }
  }, [go, onClose])

  // 選んでいるサムネイルが見える位置まで一覧をずらす
  useEffect(() => {
    const el = stripRef.current?.children[index] as HTMLElement | undefined
    el?.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' })
  }, [index])

  const slide = slides[index]

  return (
    <div className={styles.backdrop} role="dialog" aria-modal="true" aria-label={title} onClick={onClose}>
      <div className={styles.panel} onClick={(e) => e.stopPropagation()}>
        <div className={styles.bar}>
          <div className={styles.barText}>
            <p className={styles.deck}>{title}</p>
            <p className={styles.slideTitle}>{slide.title}</p>
          </div>
          <span className={styles.counter}>
            {index + 1} / {slides.length}
          </span>
          <a className={styles.pdf} href={pdf} target="_blank" rel="noopener noreferrer">PDF</a>
          <button type="button" className={styles.close} onClick={onClose} aria-label="閉じる">×</button>
        </div>

        <div
          className={styles.stage}
          onTouchStart={(e) => (touchX.current = e.touches[0].clientX)}
          onTouchEnd={(e) => {
            if (touchX.current === null) return
            const dx = e.changedTouches[0].clientX - touchX.current
            if (Math.abs(dx) > 40) go(dx < 0 ? 1 : -1)
            touchX.current = null
          }}
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={slide.src} alt={slide.title} className={styles.image} />
          <button type="button" className={`${styles.nav} ${styles.prev}`} onClick={() => go(-1)} disabled={index === 0} aria-label="前のスライド">‹</button>
          <button type="button" className={`${styles.nav} ${styles.next}`} onClick={() => go(1)} disabled={index === slides.length - 1} aria-label="次のスライド">›</button>
        </div>

        <div className={styles.strip} ref={stripRef}>
          {slides.map((s, i) => (
            <button
              key={s.src}
              type="button"
              className={`${styles.thumb} ${i === index ? styles.thumbActive : ''}`}
              onClick={() => setIndex(i)}
              aria-label={`${i + 1}枚目: ${s.title}`}
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={s.src} alt="" loading="lazy" />
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
