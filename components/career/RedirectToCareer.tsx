'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

// 以前の URL(/education/・/background/)から、Career のページへ移す
export default function RedirectToCareer() {
  const router = useRouter()
  useEffect(() => {
    router.replace('/career/')
  }, [router])
  return null
}
