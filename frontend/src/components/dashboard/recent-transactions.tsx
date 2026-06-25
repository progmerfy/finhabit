"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import { formatCurrency } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowUpRight, ArrowDownRight, Plus } from "lucide-react"
import type { Income, Expense } from "@/types"

export function RecentTransactions() {
  const [incomes, setIncomes] = useState<Income[]>([])
  const [expenses, setExpenses] = useState<Expense[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const [inc, exp] = await Promise.all([
          api.getIncomes(),
          api.getExpenses(),
        ])
        setIncomes(inc.slice(0, 3))
        setExpenses(exp.slice(0, 3))
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const allTransactions = [
    ...incomes.map(i => ({ ...i, type: "income" as const, label: i.category?.name || "Доход", desc: i.comment })),
    ...expenses.map(e => ({ ...e, type: "expense" as const, label: e.category?.name || "Расход", desc: e.description })),
  ].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()).slice(0, 5)

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-lg">Последние операции</CardTitle>
        <Button size="sm" variant="outline" className="h-8 gap-1">
          <Plus className="h-4 w-4" /> Добавить
        </Button>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary" />
          </div>
        ) : allTransactions.length === 0 ? (
          <p className="text-center text-muted-foreground py-8">
            Нет транзакций. Добавьте первый доход или расход.
          </p>
        ) : (
          <div className="space-y-3">
            {allTransactions.map((t) => (
              <div
                key={`${t.type}-${t.id}`}
                className="flex items-center justify-between p-3 rounded-xl bg-muted/50 hover:bg-muted transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`h-10 w-10 rounded-xl flex items-center justify-center ${
                      t.type === "income" ? "bg-green-500/10" : "bg-red-500/10"
                    }`}
                  >
                    {t.type === "income" ? (
                      <ArrowUpRight className="h-5 w-5 text-green-500" />
                    ) : (
                      <ArrowDownRight className="h-5 w-5 text-red-500" />
                    )}
                  </div>
                  <div>
                    <p className="text-sm font-medium">{t.label}</p>
                    <p className="text-xs text-muted-foreground">{t.desc || t.date}</p>
                  </div>
                </div>
                <p
                  className={`text-sm font-semibold ${
                    t.type === "income" ? "text-green-500" : "text-red-500"
                  }`}
                >
                  {t.type === "income" ? "+" : "-"}
                  {formatCurrency(t.amount)}
                </p>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
