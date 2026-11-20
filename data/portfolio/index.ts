// ポートフォリオの作品データ。
// 新しい版を出すときは、資料を public/portfolio/<slug>/v<版>/ に置き、
// versions の先頭に1件足す(新しい版が先頭)。画面はこのファイルだけを見て作られる。
import tradeDeskV1 from './ai-trade-desk-v1.0.json'
import tradeDeskV11 from './ai-trade-desk-v1.1.json'
import nakamaV1 from './nakama-v1.0.json'

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
  links?: { label: string; href: string; note?: string }[]
  versions: Version[]
}

type Manifest = Record<string, { file: string; title: string }[]>

// 書き出し時に作った目次(manifest)から、スライドの一覧を作る
function slidesOf(manifest: Manifest, base: string, deck: string): Slide[] {
  return manifest[deck].map((s) => ({ src: `${base}/${deck}/${s.file}`, title: s.title }))
}

const v1Base = '/portfolio/ai-trade-desk/v1.0'
const v11Base = '/portfolio/ai-trade-desk/v1.1'
const nakamaBase = '/portfolio/nakama/v1.0'

export const projects: Project[] = [
  {
    slug: 'nakama',
    title: 'NAKAMA',
    subtitle: '悪口を言い合える、日常会話AIエージェント',
    summary:
      '声で話しかけると、3Dのキャラが約1秒で言い返してくる日常会話AIです。超辛口ドSのレンと、ゆるふわのミル。仲良くなるほど遠慮のないいじりに変わり、名前や好きなものを覚えて次の会話に使います。使わない日は0円、月5ドルを超える前に自動で止まります。',
    status: '公開中',
    tags: ['音声AI', 'AIエージェント', '3D', 'GCP'],
    stack: ['Gemini 3.8 Live', 'Vertex AI', 'Cloud Run', 'Firestore', 'Cloud Functions', 'Pub/Sub', 'Python', 'FastAPI', 'React', 'TypeScript', 'React Three Fiber', 'three-vrm', 'Web Audio'],
    repoNote: 'ソースコードは非公開です。設計の考え方や実装は、面談で画面を共有しながらご説明できます。',
    links: [
      {
        label: 'アプリで話してみる',
        href: 'https://nakama-ag-877445725924.us-central1.run.app/',
        note: 'マイクを使います ・ 1回3分・1日5分まで ・ 3Dモデルは準備中(いまは光る球で表示)',
      },
    ],
    versions: [
      {
        version: '1.0',
        date: '2026.11',
        title: '声で掛け合える、2人のキャラを公開',
        highlights: [
          '音声のまま理解して声で返す Gemini 3.8 Live で、返事まで約0.7〜1.2秒',
          '話の途中で割り込むと、すぐ黙って聞き直す',
          '辛口レベルと親密度で口調が変わり、名前や好きなものを覚える。越えない線は最優先で固定',
          'Cloud Run は呼ばれた時だけ動き、使わない日は0円。1日1ドル・月5ドルで自動停止',
        ],
        docs: [
          {
            id: 'architecture',
            no: '01',
            title: 'アーキテクチャ',
            catch: '声で話すAIを、使わない日は0円で動かす',
            audience: ['engineer'],
            pdf: `${nakamaBase}/architecture.pdf`,
            slides: slidesOf(nakamaV1, nakamaBase, 'architecture'),
          },
          {
            id: 'flow',
            no: '02',
            title: '処理の流れ',
            catch: '話しかけてから、返事が聞こえるまで',
            audience: ['engineer', 'business'],
            pdf: `${nakamaBase}/flow.pdf`,
            slides: slidesOf(nakamaV1, nakamaBase, 'flow'),
          },
        ],
      },
    ],
  },
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
    links: [
      {
        label: 'Webアプリのデモを見る',
        href: 'https://d16oi8osid5n77.cloudfront.net/',
        note: 'ログイン不要 ・ 本番と同じ画面を、架空のデータで見られます',
      },
    ],
    versions: [
      {
        version: '1.1',
        date: '2026.11',
        title: '負け方を調べて、ルールを作り直した',
        highlights: [
          'デイ攻め: 15分足の突破をやめ、4時間足の流れの方向に1時間足の押し・戻りで入る形に',
          'デイ守り: 下げの相場でも、急落の行き過ぎからの戻りを小さく・こまめに取る',
          'ミドル: 自動売買をやめ、AIの「買い時か」の見立てを Slack で知らせる係に',
          '比べる相手に「下げで売るだけ」を追加し、デイの財布は100万円から再スタート',
          'Webアプリ: ログインなしでデモを見られるように',
        ],
        docs: [
          {
            id: 'changes',
            no: '04',
            title: 'v1.1 の変更点',
            catch: '負け方を調べて、ルールを作り直した',
            audience: ['engineer', 'business'],
            pdf: `${v11Base}/changes.pdf`,
            slides: slidesOf(tradeDeskV11, v11Base, 'changes'),
          },
        ],
      },
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
