import { notFound } from 'next/navigation'
import type { Metadata } from 'next'
import ProjectDetail from '@/components/portfolio/ProjectDetail'
import { findProject, projects } from '@/data/portfolio'

// 静的書き出し(output: 'export')のため、作品ごとのページを先に作る
export function generateStaticParams() {
  return projects.map((p) => ({ slug: p.slug }))
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const p = findProject(params.slug)
  return p ? { title: `${p.title} | KOSEI MAEHATA`, description: p.summary } : {}
}

export default function ProjectPage({ params }: { params: { slug: string } }) {
  const project = findProject(params.slug)
  if (!project) notFound()
  return <ProjectDetail project={project} />
}
