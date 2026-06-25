"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Brain, RefreshCw, Sparkles, TrendingUp, TrendingDown, Lightbulb } from "lucide-react"

export default function AdvisorPage() {
  const [report, setReport] = useState<string>("")
  const [loading, setLoading] = useState(false)
  const [loaded, setLoaded] = useState(false)

  const loadReport = async () => {
    setLoading(true)
    try {
      const result = await api.getAIReport()
      setReport(result.report)
      setLoaded(true)
    } catch (e) {
      console.error(e)
      setReport("Не удалось получить рекомендации. Попробуйте позже.")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadReport()
  }, [])

  const tips = report.split("\n").filter((line) => line.trim())

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <Brain className="h-6 w-6 text-primary" />
            AI Советник
          </h1>
          <p className="text-muted-foreground text-sm">
            Персональные финансовые рекомендации
          </p>
        </div>
        <Button
          variant="outline"
          size="sm"
          className="gap-2"
          onClick={loadReport}
          disabled={loading}
        >
          <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
          Обновить
        </Button>
      </div>

      <Card className="bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
        <CardContent className="p-6">
          <div className="flex items-start gap-3 mb-4">
            <div className="h-12 w-12 rounded-2xl bg-primary/10 flex items-center justify-center shrink-0">
              <Sparkles className="h-6 w-6 text-primary" />
            </div>
            <div>
              <h2 className="font-semibold text-lg">Финансовый анализ</h2>
              <p className="text-sm text-muted-foreground">
                На основе ваших транзакций за текущий месяц
              </p>
            </div>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
            </div>
          ) : (
            <div className="space-y-3">
              {tips.map((tip, i) => {
                const isPositive = tip.includes("снизились") || tip.includes("сократить") || tip.includes("сможете откладывать") || tip.includes("накоплено")
                const isNegative = tip.includes("выросли") || tip.includes("тратите")
                return (
                  <div
                    key={i}
                    className="flex items-start gap-3 p-4 rounded-xl bg-background/80 backdrop-blur"
                  >
                    <div
                      className={`h-8 w-8 rounded-lg flex items-center justify-center shrink-0 ${
                        isPositive
                          ? "bg-green-500/10"
                          : isNegative
                          ? "bg-red-500/10"
                          : "bg-primary/10"
                      }`}
                    >
                      {isPositive ? (
                        <TrendingUp className="h-4 w-4 text-green-500" />
                      ) : isNegative ? (
                        <TrendingDown className="h-4 w-4 text-red-500" />
                      ) : (
                        <Lightbulb className="h-4 w-4 text-primary" />
                      )}
                    </div>
                    <p className="text-sm">{tip}</p>
                  </div>
                )
              })}
            </div>
          )}
        </CardContent>
      </Card>

      {!loaded && !loading && (
        <Card>
          <CardContent className="py-12 text-center text-muted-foreground">
            <Brain className="h-12 w-12 mx-auto mb-3 opacity-50" />
            <p>Нажмите "Обновить", чтобы получить рекомендации</p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
