'use client'

import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'
import styles from './page.module.css'

type CharacterState = 'stand' | 'thinking' | 'talking'
type Phase = 'intro' | 'question' | 'answer'

const sleep = (ms: number) => new Promise<void>(r => setTimeout(r, ms))

const stats = [
  { value: '7', unit: 'yrs', label: 'Python' },
  { value: '5', unit: 'yrs', label: 'AWS' },
  { value: '3', unit: 'clouds', label: 'AWS · GCP · Azure' },
]

const suggestions = ['得意なことは?', '最近作ったものは?', 'どんな案件に対応できる?']

export default function TopPage() {
  const [character, setCharacter] = useState<CharacterState>('stand')
  const [phase, setPhase] = useState<Phase>('intro')
  const [visible, setVisible] = useState(true)
  const [userQuery, setUserQuery] = useState('')
  const [responseText, setResponseText] = useState('')
  const [isBusy, setIsBusy] = useState(false)
  const [input, setInput] = useState('')
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
  }, [])

  const ask = async (raw: string) => {
    const msg = raw.trim()
    if (!msg || isBusy) return
    setInput('')
    setIsBusy(true)

    // 1. 会話の欄をフェードアウト
    setVisible(false)
    await sleep(300)

    // 2. 質問を表示 / キャラ: thinking
    setUserQuery(msg)
    setResponseText('')
    setPhase('question')
    setCharacter('thinking')
    setVisible(true)

    // 3. 待機
    await sleep(1500)

    // 4. Lambda RAG API を呼び出す
    let aiResponse = ''
    const apiUrl = process.env.NEXT_PUBLIC_AI_API_URL
    if (apiUrl) {
      try {
        const res = await fetch(apiUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: msg }),
        })
        if (res.ok) {
          const data = await res.json()
          aiResponse = data.response ?? ''
        } else {
          aiResponse = 'エラーが発生しました。しばらく後でお試しください。'
        }
      } catch (err) {
        console.error('AI API call failed:', err)
        aiResponse = 'エラーが発生しました。しばらく後でお試しください。'
      }
    } else {
      aiResponse = 'API が設定されていません。'
    }

    // 5. 1文字ずつ表示 / キャラ: talking
    setCharacter('talking')
    setPhase('answer')

    let i = 0
    if (intervalRef.current) clearInterval(intervalRef.current)
    intervalRef.current = setInterval(() => {
      i++
      setResponseText(aiResponse.slice(0, i))
      if (i >= aiResponse.length) {
        clearInterval(intervalRef.current!)
        intervalRef.current = null
        setCharacter('stand')
        setIsBusy(false)
      }
    }, 18)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    ask(input)
  }

  const characterSrc = {
    stand: '/img/pause_stand.png',
    thinking: '/img/pause_thinking.png',
    talking: '/img/pause_talking.png',
  }[character]

  return (
    <div className={styles.page}>
      {/* ── 左: 自己紹介 ── */}
      <section className={styles.hero}>
        <p className={styles.eyebrow}>
          <span className={styles.eyebrowDot} />
          K.M — Portfolio
        </p>
        <h1 className={styles.headline}>
          <span className={styles.gradientText}>Cloud &amp; AI</span>
          <br />
          Engineer
        </h1>
        <div className={styles.introBody}>
          <p className={styles.lead}>
            AWS・GCP・Azure のマルチクラウドを基盤に、生成AI・機械学習システムの設計から実装まで一気通貫で対応できるエンジニアです。
          </p>
          <p>
            深層学習モデルの研究開発・LLM を活用したプロダクト構築・エンタープライズ向けクラウドインフラ設計の実績を持ちます。バックエンド開発からインフラまでフルスタックに対応し、即戦力として技術貢献が可能です。
          </p>
          <p>
            現在は業務委託として稼働中。スタートアップから大規模プロジェクトまで、幅広い案件に対応します。
          </p>
        </div>

        <div className={styles.stats}>
          {stats.map((s) => (
            <div key={s.label} className={styles.stat}>
              <p className={styles.statValue}>
                {s.value}
                <span>{s.unit}</span>
              </p>
              <p className={styles.statLabel}>{s.label}</p>
            </div>
          ))}
        </div>

        <div className={styles.actions}>
          <Link href="/portfolio/" className={styles.primaryBtn}>
            制作物を見る <span aria-hidden="true">→</span>
          </Link>
          <Link href="/career/" className={styles.ghostBtn}>
            経歴を見る
          </Link>
        </div>
      </section>

      {/* ── 右: AI に質問 ── */}
      <section className={styles.chatCard} aria-label="AI に質問">
        <div className={styles.chatHead}>
          <span className={styles.liveDot} />
          <p className={styles.chatTitle}>Ask my AI</p>
          <p className={styles.chatSub}>経歴やスキルについて、AI が本人に代わって答えます</p>
        </div>

        <div className={styles.chatBody}>
          <div className={styles.character}>
            <div className={styles.halo} />
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={characterSrc} alt="キャラクター" className={styles.characterImg} />
          </div>

          <div className={`${styles.conversation} ${!visible ? styles.fadeOut : ''}`}>
            {phase === 'intro' ? (
              <div className={`${styles.bubble} ${styles.bubbleAi}`}>
                <span className={styles.sender}>AI</span>
                <p>こんにちは、K.M です。経歴やスキル、制作物について、なんでも聞いてください。</p>
              </div>
            ) : (
              <>
                <div className={`${styles.bubble} ${styles.bubbleUser}`}>
                  <span className={styles.sender}>あなた</span>
                  <p>{userQuery}</p>
                </div>
                <div className={`${styles.bubble} ${styles.bubbleAi}`}>
                  <span className={styles.sender}>AI</span>
                  {phase === 'question' ? (
                    <div className={styles.thinkingDots}>
                      <span /><span /><span />
                    </div>
                  ) : (
                    <p className={styles.responseText}>
                      {responseText}
                      {isBusy && <span className={styles.cursor} />}
                    </p>
                  )}
                </div>
              </>
            )}
          </div>
        </div>

        <div className={styles.suggestions}>
          {suggestions.map((q) => (
            <button key={q} type="button" onClick={() => ask(q)} disabled={isBusy}>
              {q}
            </button>
          ))}
        </div>

        <form className={styles.chatForm} onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="何でも聞いてみてください …"
            className={styles.chatInput}
            disabled={isBusy}
            aria-label="質問"
          />
          <button type="submit" className={styles.sendBtn} disabled={isBusy || !input.trim()} aria-label="送信">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="m22 2-7 20-4-9-9-4Z" />
              <path d="M22 2 11 13" />
            </svg>
          </button>
        </form>
      </section>
    </div>
  )
}
