import styles from './page.module.css'

interface SkillGroup {
  category: string
  experience?: string
  items: string[]
}

const backend: SkillGroup = {
  category: 'BACKEND',
  experience: 'Python · 7 yrs',
  items: [
    'Python', 'numpy', 'scipy', 'pandas', 'scikit-learn',
    'TensorFlow', 'PyTorch', 'opencv-python', 'Pillow',
    'openpyxl', 'beautifulsoup4', 'requests', 'selenium',
    'boto3', 'botocore', 'awscli', 'sqlalchemy',
    'SQLite', 'FastAPI', 'jsonschema', 'pytest', 'Docker',
  ],
}

const frontend: SkillGroup = {
  category: 'FRONTEND',
  experience: 'JavaScript · 3 yrs',
  items: ['JavaScript', 'TypeScript', 'React', 'Next.js', 'HTML', 'CSS'],
}

const awsServices: SkillGroup = {
  category: 'AWS',
  experience: '5 yrs',
  items: [
    'EC2', 'ECS', 'Lambda', 'Step Functions',
    'RDS', 'Aurora', 'S3', 'DynamoDB',
    'VPC', 'Subnets', 'Route53', 'CloudFront',
    'API Gateway', 'IAM', 'IAM Roles', 'KMS', 'WAF',
    'CodeCommit', 'CodeBuild', 'CodeDeploy', 'CodePipeline',
    'CloudWatch', 'SQS', 'SNS', 'EventBridge',
    'SageMaker', 'Bedrock', 'Athena', 'Glue', 'Redshift',
    'CloudFormation', 'Cognito', 'ACM', 'Cost Explorer', 'Budgets',
  ],
}

const gcpServices: SkillGroup = {
  category: 'GCP',
  experience: '3 yrs',
  items: [
    'Cloud Run', 'Cloud Functions', 'Cloud Storage',
    'Filestore', 'Cloud SQL', 'BigQuery', 'Dataflow',
    'Vertex AI', 'VPC', 'Subnets', 'Cloud Build',
    'Cloud Deploy', 'Cloud Logging', 'Cloud Scheduler', 'gcloud CLI',
  ],
}

const azureServices: SkillGroup = {
  category: 'AZURE',
  experience: '3 yrs',
  items: [
    'Azure Functions', 'Container Apps', 'App Service',
    'AKS', 'Blob Storage',
    'Azure Database for PostgreSQL', 'Azure Database for MySQL',
  ],
}

const ai: SkillGroup = {
  category: 'AI · AGENTS',
  items: [
    'マルチエージェント設計', 'Claude Code', 'Claude API', 'Amazon Bedrock',
    'RAG', 'Tool Use', 'プロンプト設計', 'openai', 'langchain', 'ADK',
  ],
}

const iac: SkillGroup = {
  category: 'IaC · CI/CD',
  items: ['Terraform', 'CloudFormation', 'Cloud Build', 'GitHub Actions'],
}

export default function SkillPage() {
  return (
    <div className={styles.page}>
      <div className={styles.pageHeader}>
        <h1 className={styles.title}>SKILL</h1>
        <p className={styles.subtitle}>TECH STACK</p>
      </div>

      {/* Dev skills row */}
      <div className={styles.row}>
        <SkillCard group={backend} accent="backend" />
        <SkillCard group={frontend} accent="frontend" />
      </div>

      {/* AI full row */}
      <div className={styles.rowFull}>
        <SkillCard group={ai} accent="ai" />
      </div>

      {/* AWS full row */}
      <div className={styles.rowFull}>
        <SkillCard group={awsServices} accent="aws" />
      </div>

      {/* GCP + Azure row */}
      <div className={styles.row}>
        <SkillCard group={gcpServices} accent="gcp" />
        <SkillCard group={azureServices} accent="azure" />
      </div>

      {/* IaC small row */}
      <div className={styles.rowNarrow}>
        <SkillCard group={iac} accent="iac" />
      </div>
    </div>
  )
}

function SkillCard({ group, accent }: { group: SkillGroup; accent: string }) {
  return (
    <div className={`${styles.card} ${styles[accent]}`}>
      <div className={styles.cardHeader}>
        <span className={styles.category}>{group.category}</span>
        {group.experience && (
          <span className={styles.experience}>{group.experience}</span>
        )}
      </div>
      <div className={styles.tags}>
        {group.items.map(item => (
          <span key={item} className={styles.tag}>{item}</span>
        ))}
      </div>
    </div>
  )
}
