// 経歴(Career)ページのデータ。
// 学歴は「年・タイトル・解説」、職歴は「期間・会社・役割・活かしたスキル・案件」で書く。
// 公開ページなので、顧客名や個人を特定できる情報は書かない。

export type SchoolEntry = {
  year: string
  title: string
  paragraphs: string[]
}

export type Project = {
  period: string
  title: string
  team: string
  summary: string[]
  tech: string[]
}

export type Company = {
  period: string
  name: string
  employment: string
  lead: string
  roles: string[]
  skills: string[]
  projects: Project[]
}

export const education: SchoolEntry[] = [
  {
    year: '2004',
    title: '駒込小学校に入学',
    paragraphs: [
      '駒込小学校に入学し、ここで少年期を過ごす。友達を作るのが苦手で、一人を好む傾向にあった。家庭事情もあり、基本的に家では一人で過ごす時間が多く、ゲームやアニメを見ることが日常だった。',
      '人とは違うことをするのが好きで、皆が同じことに取り組むときでも、自分は別の方向で物事を考えて取り組むことが多かった。特に図工などのクリエイティブな部分で目立つことが多く、周りから発達障害疑惑が出ることもあった（笑）。変なことをするのが大好きだった。',
    ],
  },
  {
    year: '2010',
    title: '駒込中学校に進学',
    paragraphs: [
      '駒込小学校を卒業後、近くに駒込中学校があったため、そのまま駒込中学校に進学。',
      '小学生の頃から友達をあまり作らなかったこともあり、中学生時代はコミュニケーションの取り方に難しさを感じる時期だった。「なぜ友達を作るのか」「どうしたら他人に好感を持ってもらえるのか」「自分の感情とは何なのか」——人との関わりについて分析するような思考を持っていた。',
      '例えば男子中学生の世界では、バカをやるとウケが良いということに気づいた。これをすると男子は笑い、声をかけてもらえるようになる。しかし残念なことに女子ウケは最悪で、好きな女子にはキモがられる始末だった。卒業前にはディズニーに行く夢を持っていたが、叶わないまま卒業した（笑）。',
      '友達を作るためにバスケットボール部で活動していたが、成績は悪く偏差値は40程度だった。中学2年生から人生で初めて勉学に目を向け、偏差値を20ほど上げ、芝浦工業大学高等学校への進学を決意した。',
    ],
  },
  {
    year: '2013',
    title: '芝浦工業大学高等学校に入学',
    paragraphs: [
      '芝浦工業大学高等学校へ入学。男子校でもあり、この頃は恋愛に目を向けることが多かった時期だった。',
      '友達からの情報で、ゲームやWebサイトはプログラミングで作られていることを知った。恋愛で感情に葛藤する中、自分が本当にやりたいことを分析する時期でもあった。',
      '高校2年生の時には成績が最下位になった。担任の先生に忠告を受け、やりたいことをすべて断ち、坊主にし、勉学に励んだ。150位から50位まで順位を上げ、大学への進学権を得ることができた。',
      'プログラミングでAIについて学びたいという気持ちが強くなり、芝浦工業大学工学部情報工学科への進学が確定した。',
    ],
  },
  {
    year: '2016',
    title: '芝浦工業大学 工学部 情報工学科に入学',
    paragraphs: [
      '芝浦工業大学工学部情報工学科へ入学。勉学をしつつ、恋愛についても学び始めた。人間は一人で生きていくことは難しいのではないかという気づきを得た時期だった。',
      '異性相手だからこそ自分の弱みを話せるということに気づき、女性と結ばれるためにどうすればいいかを考え行動し始めた。ホストの1日体験もしてみた。',
      'しかしこうした寄り道に本気で取り組んだ結果、大学の単位で問題が起きた。単位不足かつ、インターンも十分にキャッチアップできていなかった。24単位必要なところを40単位履修し、集中モードで取り組んだ結果、半年の留年で収まり2020年に卒業見込みとなった。',
    ],
  },
  {
    year: '2020',
    title: '芝浦工業大学を卒業',
    paragraphs: [
      '芝浦工業大学工学部情報工学科を卒業。',
      '大学では、仮想空間のマップ上でエージェントがA地点からB地点へ移動する際、障害物が存在する環境の中で最適ルートを導き出すAIの研究を行っていた。Deep Q Learning という技術でこの課題を解決できないかをテーマに研究を進めた。',
      'Q値を求める論理式を理解しプログラムへ落とし込み、実装と検証を繰り返した。最終的に研究成果を論文としてまとめた。',
    ],
  },
]

export const companies: Company[] = [
  {
    period: '2021.12 – 2022.09',
    name: '株式会社ニューロンネットワーク',
    employment: '業務委託',
    lead: 'コロナ禍で就職が難しい中、縁があって参画。深層学習モデルの開発と研究開発に取り組んだ。',
    roles: ['AIエンジニア(検出系のモデル開発)', '研究開発'],
    skills: ['Python', 'TensorFlow', 'PyTorch', '画像認識', 'マルチラベル分類', 'Docker', 'Jupyter'],
    projects: [
      {
        period: '2021.12 – 2022.09',
        title: 'TensorFlow / PyTorch を活用したマルチラベル画像認識AIモデル開発',
        team: '開発2名',
        summary: [
          '画像を複数のラベルに分類する深層学習モデルを開発',
          '未経験の領域だったため、専門書で学びながら研修と並行して研究を推進',
          'データの準備からモデルの学習・評価までを担当',
        ],
        tech: ['Python', 'TensorFlow', 'PyTorch', 'Docker', 'Jupyter'],
      },
    ],
  },
  {
    period: '2022.10 – 2025.03',
    name: 'Kyla株式会社',
    employment: '正社員',
    lead: 'AWS を中心に、インフラ構築とバックエンド開発を担当。さまざまなプロジェクトで設計からリリースまでを経験した。',
    roles: ['インフラエンジニア', 'バックエンドエンジニア'],
    skills: ['AWS', 'Lambda', 'Step Functions', 'EventBridge', 'API Gateway', 'Redshift', 'Terraform', 'dbt', 'CI/CD', 'Python', 'SQL', '設計書作成'],
    projects: [
      {
        period: '2024.06 – 2025.03',
        title: 'AWS サービス群を活用した大規模データ連携基盤の構築・保守運用',
        team: '開発5名',
        summary: [
          'データ量の増加にともなう性能と運用コストの課題を解決',
          'Terraform による IaC と、CodeBuild による CI/CD を整備',
          'dbt で Redshift 向けの変換処理を開発し、クエリのチューニングとコストの改善提案を担当',
        ],
        tech: ['Terraform', 'dbt', 'Redshift', 'Step Functions', 'EventBridge', 'Lambda', 'CodeBuild'],
      },
      {
        period: '2023.10 – 2024.05',
        title: 'AWS サーバレス API による3社間データ連携システムの構築',
        team: '開発4名',
        summary: [
          '企業間のデータ連携の遅れと非効率を解消する連携基盤を開発',
          'Lambda と API Gateway で連携 API を構築し、複雑な JSON の整形と他社アカウントへの安全な連携を実装',
          '設計から開発、テスト、リリースまでを主導',
        ],
        tech: ['Lambda', 'API Gateway', 'S3', 'Step Functions', 'IAM', 'WAF', 'Python'],
      },
      {
        period: '2023.05 – 2023.09',
        title: '運送業界向け AI / ビッグデータ活用の安全診断サービス開発',
        team: '開発6名',
        summary: [
          '事故リスクの低減と安全運転の促進を目的とした分析基盤を構築',
          '運転ログなどのビッグデータのクレンジングと前処理を担当',
          'テスト設計から結合テストまでを実施し、品質を担保',
        ],
        tech: ['Redshift', 'RDS', 'EC2', 'ECS (Fargate)', 'Apache Airflow', 'Python', 'SQL'],
      },
      {
        period: '2022.10 – 2023.04',
        title: 'GCP / AWS 連携によるクラウド向けセキュリティ診断サービス開発',
        team: '開発4名',
        summary: [
          '顧客のクラウド環境のセキュリティリスクを検出・通知するサービスを開発',
          'GCP から届くデータを AWS 上で集約し、変換・正規化するロジックを実装',
          'Step Functions と EventBridge でサーバレスな処理の流れを構築し、CI/CD も整備',
        ],
        tech: ['Lambda', 'Step Functions', 'EventBridge', 'CodePipeline', 'CloudFormation', 'GCP', 'Python'],
      },
    ],
  },
  {
    period: '2025.05 – 2025.12',
    name: 'アカツキAIテクノロジーズ株式会社',
    employment: '正社員 → 業務委託',
    lead: '生成AI開発を中心としたプロジェクトに参画。LLM を使ったエージェントの設計から、業務で使えるアプリまでを手がけた。',
    roles: ['フルスタックエンジニア(インフラ、フロントエンド、バックエンド)', 'AIエンジニア(生成AI、AIエージェント、RAG)', 'FDE', 'PM'],
    skills: ['LangChain', 'マルチエージェント', 'RAG', 'プロンプト設計', 'OpenAI API', 'Azure OpenAI', 'Vertex AI', 'Whisper', 'Streamlit', 'GCP', 'Python'],
    projects: [
      {
        period: '2025.10 – 2025.12',
        title: 'PC操作ログを分析する生成AIエージェントの開発',
        team: '開発2名',
        summary: [
          'PC の操作ログから、作業内容を自動で分析・要約するエージェントを開発',
          'シングルエージェント構成から、LangChain によるマルチエージェント構成(解析・レポート・改善提案の分業)へ再設計',
          '設計書の作成から実装、精度の検証、改善提案までを担当',
        ],
        tech: ['LangChain', 'Azure OpenAI', 'GCP', 'Python', 'GitHub Copilot'],
      },
      {
        period: '2025.07 – 2025.09',
        title: 'マーケティング分析の生成AIエージェントの開発',
        team: '開発2名',
        summary: [
          '購買・商品・購入者のデータを統合し、チャットで分析できるエージェントを開発',
          '自然言語の質問から、指標の算出・傾向の要約・レポートの生成までを一貫して実行',
          'Streamlit でチャット UI と可視化を作り、業務デモとして使えるプロトタイプにした',
        ],
        tech: ['Vertex AI', 'BigQuery', 'Compute Engine', 'Streamlit', 'Python'],
      },
      {
        period: '2025.05 – 2025.06',
        title: '生成AIを活用した社内の業務効率化',
        team: '開発1名',
        summary: [
          '議事録の自動化アプリ(文字起こし・要約・検索、人が確認できる HITL 構成)',
          'YouTube Studio の指標を集めるスクレイピングツール',
          'LLM でスカウト文を作るブラウザ拡張',
        ],
        tech: ['LangChain', 'OpenAI API', 'Whisper', 'Streamlit', 'Selenium', 'Python'],
      },
    ],
  },
  {
    period: '2025.12 – NOW',
    name: 'solo Player',
    employment: 'Freelance',
    lead: '自立してさまざまな案件を受けながら、AI に限らず最先端の技術を追い続けるため、業務委託として独立。',
    roles: ['フルスタックエンジニア(インフラ、フロントエンド、バックエンド)', 'AIエンジニア', 'FDE', 'PM', 'テックリード'],
    skills: ['Claude Code', 'Spec Kit', 'Amazon Bedrock', 'AIエージェント', 'React', 'Next.js', 'FastAPI', 'AWS', 'GCP', 'Terraform', 'Python'],
    projects: [
      {
        period: '2026.05 – 2026.09',
        title: '経理業務アプリケーションのスクラッチ開発(Workato からの移行)',
        team: '開発2名',
        summary: [
          'Workato で動いていた経理の処理を、GCP 上の Python の日次バッチとして再構築',
          '既存の処理と計算ロジックを調べて仕様を整理し、設計・実装',
          '既存処理との結果の比較で、データの整合性を確認',
        ],
        tech: ['Python', 'GCP', 'Workato', 'Claude'],
      },
      {
        period: '2026.04 – 2026.09',
        title: '社内業務アプリケーションのスクラッチ開発(Dify からの移行)',
        team: '開発6名',
        summary: [
          'Dify で作られていた機能を、独立した Web アプリケーションとして再構築',
          'フロントエンド、バックエンド API、AWS のインフラまでを一貫して設計・実装',
          'Claude を使った AI 支援開発で、実装・調査・レビューを効率化',
        ],
        tech: ['React', 'Next.js', 'FastAPI', 'AWS', 'Dify', 'Claude'],
      },
      {
        period: '2026.02 – 2026.05',
        title: 'AIインタビューアシスタントの開発',
        team: '開発1名',
        summary: [
          '会議に AI Bot が参加し、会話の要約や追加の質問をチャットで提案するアプリを開発',
          'Spec Kit で要件整理から設計・タスク分解までを進め、Claude Code で実装',
          'GCP と AWS のマルチクラウドで、インフラ・バックエンド・フロントエンドを一人で担当',
        ],
        tech: ['Next.js', 'React', 'Python', 'AWS', 'GCP', 'Terraform', 'Claude Code', 'Spec Kit'],
      },
      {
        period: '2026.01 – 2026.04',
        title: 'オペレーター支援AIエージェントの開発',
        team: '開発8名',
        summary: [
          'Amazon Bedrock のエージェントの不具合対応、プロンプト調整、精度改善を担当',
          'キャッシュの有無で、応答速度・トークン消費・処理効率を比較検証',
          '検証結果から課題を整理し、改善方針を提案',
        ],
        tech: ['Amazon Bedrock', 'Lambda', 'S3', 'Python', 'Codex'],
      },
    ],
  },
]
