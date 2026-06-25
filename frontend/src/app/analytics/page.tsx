"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import { formatCurrency } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { PieChartComponent } from "@/components/charts/pie-chart"
import { LineChartComponent } from "@/components/charts/line-chart"
import { BarChartComponent } from "@/components/charts/bar-chart"
import type { AnalyticsData, BalanceHistoryItem, MonthlyAnalytics } from "@/types"

export default function AnalyticsPage() {
  const [period, setPeriod] = useState("month")
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null)
  const [balanceHistory, setBalanceHistory] = useState<BalanceHistoryItem[]>([])
  const [monthly, setMonthly] = useState<MonthlyAnalytics[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      try {
        const [a, b, m] = await Promise.all([
          api.getAnalytics(period),
          api.getBalanceHistory(6),
          api.getMonthlyAnalytics(6),
        ])
        setAnalytics(a)
        setBalanceHistory(b)
        setMonthly(m)
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [period])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    )
  }

  const expensePieData = analytics?.top_categories.map((c) => ({
    name: c.category_name,
    value: c.percentage,
  })) || []

  const incomePieData: { name: string; value: number }[] = []

  const balanceLines = balanceHistory.map((b) => ({
    date: b.date,
    Баланс: b.balance,
    Доходы: b.income,
    Расходы: b.expense,
  }))

  const monthlyLines = monthly.map((m) => ({
    date: m.month,
    Доходы: m.income,
    Расходы: m.expense,
    Накопления: m.savings,
  }))

  const topExpenses = (analytics?.top_categories || []).map((c) => ({
    name: c.category_name,
    value: c.amount,
  }))

  const changeColor = analytics && analytics.change_vs_last_period >= 0 ? "text-red-500" : "text-green-500"

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Аналитика</h1>
          <p className="text-muted-foreground text-sm">
            Анализ финансов за период
          </p>
        </div>
        <Tabs value={period} onValueChange={setPeriod}>
          <TabsList>
            <TabsTrigger value="week">Неделя</TabsTrigger>
            <TabsTrigger value="month">Месяц</TabsTrigger>
            <TabsTrigger value="quarter">Квартал</TabsTrigger>
            <TabsTrigger value="year">Год</TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <Card>
          <CardContent className="p-4">
            <p className="text-xs text-muted-foreground mb-1">Доход</p>
            <p className="text-lg font-bold text-green-500">
              {formatCurrency(analytics?.total_income || 0)}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-xs text-muted-foreground mb-1">Расход</p>
            <p className="text-lg font-bold text-red-500">
              {formatCurrency(analytics?.total_expense || 0)}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-xs text-muted-foreground mb-1">Накопления</p>
            <p className="text-lg font-bold">
              {formatCurrency(analytics?.net_savings || 0)}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-xs text-muted-foreground mb-1">Изменение</p>
            <p className={`text-lg font-bold ${changeColor}`}>
              {analytics ? `${analytics.change_vs_last_period >= 0 ? "+" : ""}${analytics.change_vs_last_period}%` : "0%"}
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Расходы по категориям</CardTitle>
          </CardHeader>
          <CardContent>
            <PieChartComponent data={expensePieData} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Доходы по категориям</CardTitle>
          </CardHeader>
          <CardContent>
            <PieChartComponent data={incomePieData} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Доходы и расходы по месяцам</CardTitle>
          </CardHeader>
          <CardContent>
            <LineChartComponent
              data={monthlyLines}
              lines={[
                { dataKey: "Доходы", color: "hsl(142.1, 76.2%, 36.3%)", name: "Доходы" },
                { dataKey: "Расходы", color: "hsl(0, 84%, 60%)", name: "Расходы" },
              ]}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Накопления по месяцам</CardTitle>
          </CardHeader>
          <CardContent>
            <LineChartComponent
              data={monthlyLines}
              lines={[
                { dataKey: "Накопления", color: "hsl(217.2, 91.2%, 59.8%)", name: "Накопления" },
              ]}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Динамика баланса</CardTitle>
          </CardHeader>
          <CardContent>
            <LineChartComponent
              data={balanceLines}
              lines={[
                { dataKey: "Баланс", color: "hsl(142.1, 76.2%, 36.3%)", name: "Баланс" },
              ]}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Топ расходов</CardTitle>
          </CardHeader>
          <CardContent>
            <BarChartComponent data={topExpenses} />
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
