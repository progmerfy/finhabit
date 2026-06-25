"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import { useTelegram } from "@/hooks/use-telegram"
import { useInit } from "@/hooks/use-api"
import { DashboardPage } from "@/components/dashboard/dashboard-page"

export default function Home() {
  const { loading } = useInit()
  const { user } = useTelegram()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    )
  }

  if (!user) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
        <div className="text-6xl">💰</div>
        <h1 className="text-2xl font-bold">Finance Discipline</h1>
        <p className="text-muted-foreground text-center max-w-md">
          Откройте это приложение через Telegram WebApp для управления личным бюджетом
        </p>
      </div>
    )
  }

  return <DashboardPage />
}
