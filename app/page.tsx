'use client'

import { useState, useRef, useEffect } from 'react'
import styles from './page.module.css'

type CharacterState = 'stand' | 'thinking' | 'talking'
type Phase = 'intro' | 'question' | 'answer'

const MOCK_RESPONSE =
  `ご質問ありがとうございます。\n\nAWS・GCP・Azure のマルチクラウドと生成AI開発を専門とするエンジニアです。\n\n深層学習モデルの研究開発から LLM を活用したプロダクト開発、エンタープライズ向けクラウドインフラの構築まで、プロジェクト全体を一気通貫でサポートできます。\n\n経歴・スキル・実績について、何でもお気軽にお聞きください。`

const sleep = (ms: number) => new Promise<void>(r => setTimeout(r, ms))

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isBusy) return

    const msg = input.trim()
    setInput('')
    setIsBusy(true)

    // 1. ボディ部分をフェードアウト（名前・役職は残る）
    setVisible(false)
    await sleep(300)

    // 2. 質問をセット → フェードイン / キャラ: thinking
    setUserQuery(msg)
    setResponseText('')
    setPhase('question')
    setCharacter('thinking')
    setVisible(true)

    // 3. 待機
    await sleep(1500)

    // 4. AI API を呼び出す（API URL が未設定の場合はモック）
    let aiResponse = MOCK_RESPONSE
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
          aiResponse = data.response ?? MOCK_RESPONSE
        }
      } catch (err) {
        console.error('AI API call failed, using mock:', err)
      }
    }

    // 5. ストリーミング開始 / キャラ: talking
    setCharacter('talking')
    setPhase('answer')

    const text = aiResponse
    let i = 0
    if (intervalRef.current) clearInterval(intervalRef.current)
    intervalRef.current = setInterval(() => {
      i++
      setResponseText(text.slice(0, i))
      if (i >= text.length) {
        clearInterval(intervalRef.current!)
        intervalRef.current = null
        setCharacter('stand')
        setIsBusy(false)
      }
    }, 18)
  }

  const characterSrc = {
    stand: '/img/pause_stand.png',
    thinking: '/img/pause_thinking.png',
    talking: '/img/pause_talking.png',
  }[character]

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <div className={styles.cardBody}>
          {/* Character */}
          <div className={styles.character}>
            <img src={characterSrc} alt="Character" className={styles.characterImg} />
          </div>

          {/* Area A */}
          <div className={styles.infoPanel}>

            {/* ── 固定ヘッダー: フェードしない ── */}
            <div className={styles.introHeader}>
              <p className={styles.introName}>前畑 康成</p>
              <p className={styles.introRole}>Cloud &amp; AI Engineer</p>
              <div className={styles.divider} />
            </div>

            {/* ── フェードするボディ ── */}
            <div className={`${styles.infoPanelBody} ${!visible ? styles.fadeOut : ''}`}>
              {phase === 'intro' ? (
                <div className={styles.introBody}>
                  <p>
                    AWS・GCP・Azure のマルチクラウドを基盤に、生成AI・機械学習システムの設計から実装まで一気通貫で対応できるエンジニアです。
                  </p>
                  <p>
                    深層学習モデルの研究開発・LLM を活用したプロダクト構築・エンタープライズ向けクラウドインフラ設計の実績を持ちます。バックエンド開発からインフラまでフルスタックに対応し、即戦力として技術貢献が可能です。
                  </p>
                  <p>
                    現在は業務委託として稼働中。スタートアップから大規模プロジェクトまで、幅広い案件に対応します。
                  </p>
                </div>
              ) : (
                <div className={styles.chatView}>
                  <p className={styles.msgRole}>YOU</p>
                  <p className={styles.userQuery}>{userQuery}</p>
                  <div className={styles.chatDivider} />
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
              )}
            </div>

          </div>
        </div>

        {/* Chat input */}
        <form className={styles.chatForm} onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="何でも聞いてみてください ..."
            className={styles.chatInput}
            disabled={isBusy}
          />
          <button
            type="submit"
            className={styles.sendBtn}
            disabled={isBusy || !input.trim()}
          >
            SEND
          </button>
        </form>
      </div>
    </div>
  )
}
