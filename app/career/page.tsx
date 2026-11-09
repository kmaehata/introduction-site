import type { Metadata } from 'next'
import CareerTimeline from '@/components/career/CareerTimeline'

export const metadata: Metadata = {
  title: 'Career | KM',
  description: '学歴と職歴',
}

export default function CareerPage() {
  return <CareerTimeline />
}
