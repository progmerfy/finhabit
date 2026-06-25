"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import { formatCurrency } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { BalanceCard } from "./balance-card"
import { StatsCard } from "./stats-card"
import { RecentTransactions } from "./recent-transactions"
import { DashboardData } from "@/types"
import {
  Wallet,
  TrendingUp,
  TrendingDown,
  PiggyBank,
  Percent,
  Star,
} from "lucide-react"

export function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const dashboard = await api.getDashboard()
        setData(dashboard)
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    )
  }

  if (!data) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
        <div className="text-6xl">📊</div>
        <h2 className="text-xl font-semibold">Добро пожаловать в Finance Discipline</h2>
        <p className="text-muted-foreground text-center max-w-md">
          Откройте приложение через Telegram WebApp, чтобы начать управлять бюджетом.
        </p>
      </div>
    )
  }

  const stats = [
    {
      title: "Доходы за месяц",
      value: formatCurrency(data.monthly_income),
      icon: TrendingUp,
      gradient: "card-gradient",
    },
    {
      title: "Расходы за месяц",
      value: formatCurrency(data.monthly_expense),
      icon: TrendingDown,
      gradient: "card-gradient-orange",
    },
    {
      title: "Накопления",
      value: formatCurrency(data.total_savings),
      icon: PiggyBank,
      gradient: "card-gradient-blue",
    },
    {
      title: "Процент накоплений",
      value: `${data.savings_percent}%`,
      icon: Percent,
      gradient: "card-gradient-purple",
    },
  ]

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Дашборд</h1>
          <p className="text-muted-foreground text-sm">Ваша финансовая сводка</p>
        </div>
        <Badge variant="secondary" className="text-sm px-3 py-1">
          <Star className="h-4 w-4 mr-1 text-yellow-500" />
          Рейтинг: {data.financial_rating}
        </Badge>
      </div>

      <BalanceCard
        balance={data.balance}
        todaySpent={data.today_spent}
        dailyLimit={data.daily_limit}
        dailyRemaining={data.daily_remaining}
      />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {stats.map((stat) => (
          <StatsCard key={stat.title} {...stat} />
        ))}
      </div>

      <RecentTransactions />
    </div>
  )
}
