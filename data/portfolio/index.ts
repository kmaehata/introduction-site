// ポートフォリオの作品データ。
// 新しい版を出すときは、資料を public/portfolio/<slug>/v<版>/ に置き、
// versions の先頭に1件足す(新しい版が先頭)。画面はこのファイルだけを見て作られる。
import tradeDeskV1 from './ai-trade-desk-v1.0.json'

export type Audience = 'engineer' | 'business'

export type Slide = { src: string; title: string }

export type Doc = {
  id: string
  no: string
  title: string
  catch: string
  audience: Audience[]
  pdf: string
  slides: Slide[]
}

export type Version = {
  version: string
  date: string
  title: string
  highlights: string[]
  docs: Doc[]
}

export type Project = {
  slug: string
  title: string
  subtitle: string
  summary: string
  status: string
  tags: string[]
  stack: string[]
  repoNote: string
  versions: Version[]
}

type Manifest = Record<string, { file: string; title: string }[]>

// 書き出し時に作った目次(manifest)から、スライドの一覧を作る
function slidesOf(manifest: Manifest, base: string, deck: string): Slide[] {
  return manifest[deck].map((s) => ({ src: `${base}/${deck}/${s.file}`, title: s.title }))
}

const v1Base = '/portfolio/ai-trade-desk/v1.0'

export const projects: Project[] = [
  {
    slug: 'ai-trade-desk',
    title: 'AIトレードデスク',
    subtitle: 'マルチエージェント自律取引システム',
    summary:
      '5人のAIが相場を調べて方針を考え、AIを使わない売買エンジンが24時間ルールどおりに売買します。結果は Slack と Web アプリで確認でき、案内役のAIに理由を聞けます。',
    status: 'ペーパー運用中',
    tags: ['マルチエージェント', '生成AI', '自動売買', 'AWS'],
    stack: ['Python', 'SQLite', 'Claude Code', 'Amazon Bedrock', 'AWS Lambda', 'Amazon S3', 'CloudFront', 'Cognito', 'DynamoDB', 'GitHub Actions'],
    repoNote: 'ソースコードは非公開です。設計の考え方や実装は、面談で画面を共有しながらご説明できます。',
    versions: [
      {
        version: '1.0',
        date: '2026.11',
        title: '3つの運用を同時にペーパー運用',
        highlights: [
          '5人のAI(アナリスト・戦略担当・判断役・記録係・案内役)の分担',
          'AIは方針を書くだけ。注文と損切りはAIなしのエンジンが担当',
          'ミドル・デイ守り・デイ攻めの3つの財布を、AIなしの比較役と並べて評価',
          'Slack 通知と、案内役アオに理由を聞ける Web アプリ',
        ],
        docs: [
          {
            id: 'architecture',
            no: '01',
            title: 'アーキテクチャ',
            catch: '全体像から、実際の構成まで',
            audience: ['engineer'],
            pdf: `${v1Base}/architecture.pdf`,
            slides: slidesOf(tradeDeskV1, v1Base, 'architecture'),
          },
          {
            id: 'flow',
            no: '02',
            title: '処理フロー',
            catch: '誰が・いつ・何をするのか',
            audience: ['engineer', 'business'],
            pdf: `${v1Base}/flow.pdf`,
            slides: slidesOf(tradeDeskV1, v1Base, 'flow'),
          },
          {
            id: 'business',
            no: '03',
            title: 'AIエージェントの狙いと解説',
            catch: '何ができて、なぜ安心で、どう測るのか',
            audience: ['business'],
            pdf: `${v1Base}/business.pdf`,
            slides: slidesOf(tradeDeskV1, v1Base, 'business'),
          },
        ],
      },
    ],
  },
]

export const audienceLabel: Record<Audience, string> = {
  engineer: 'エンジニア向け',
  business: 'ビジネス向け',
}

export function findProject(slug: string): Project | undefined {
  return projects.find((p) => p.slug === slug)
}
