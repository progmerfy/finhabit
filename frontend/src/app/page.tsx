"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import { useTelegram } from "@/hooks/use-telegram"
import { useInit } from "@/hooks/use-api"
import { DashboardPage } from "@/components/dashboard/dashboard-page"

export default function Home() {
  const { loading, error } = useInit()
  const { user } = useTelegram()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    )
  }

  return <DashboardPage />
}
