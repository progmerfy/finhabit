"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import { formatCurrency } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { BudgetProgress } from "@/components/budget/budget-progress"
import { Plus, PiggyBank } from "lucide-react"
import type { Budget, ExpenseCategory } from "@/types"

export default function BudgetPage() {
  const [budgets, setBudgets] = useState<Budget[]>([])
  const [categories, setCategories] = useState<ExpenseCategory[]>([])
  const [loading, setLoading] = useState(true)
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState({ category_name: "", limit_amount: "" })
  const today = new Date()

  const load = async () => {
    try {
      const [b, cats] = await Promise.all([
        api.getBudgets(today.getMonth() + 1, today.getFullYear()),
        api.getExpenseCategories(),
      ])
      setBudgets(b)
      setCategories(cats)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const handleSubmit = async () => {
    await api.createBudget({
      category_name: form.category_name,
      month: today.getMonth() + 1,
      year: today.getFullYear(),
      limit_amount: parseFloat(form.limit_amount),
    })
    setOpen(false)
    setForm({ category_name: "", limit_amount: "" })
    load()
  }

  const totalBudget = budgets.reduce((s, b) => s + b.limit_amount, 0)
  const totalSpent = budgets.reduce((s, b) => s + b.spent, 0)

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Бюджет</h1>
          <p className="text-muted-foreground text-sm">
            {formatCurrency(totalSpent)} / {formatCurrency(totalBudget)}
          </p>
        </div>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild>
            <Button className="gap-2">
              <Plus className="h-4 w-4" /> Лимит
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Новый лимит бюджета</DialogTitle>
            </DialogHeader>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label>Категория</Label>
                <Select
                  value={form.category_name}
                  onValueChange={(v) => setForm({ ...form, category_name: v })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Выберите категорию" />
                  </SelectTrigger>
                  <SelectContent>
                    {categories.map((c) => (
                      <SelectItem key={c.id} value={c.name}>
                        {c.icon} {c.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>Лимит (EUR)</Label>
                <Input
                  type="number"
                  placeholder="500"
                  value={form.limit_amount}
                  onChange={(e) => setForm({ ...form, limit_amount: e.target.value })}
                />
              </div>
              <Button className="w-full" onClick={handleSubmit}>
                Сохранить
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Месячные лимиты</CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary" />
            </div>
          ) : budgets.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">
              <PiggyBank className="h-12 w-12 mx-auto mb-3 opacity-50" />
              <p>Нет бюджетных лимитов</p>
              <p className="text-sm">Добавьте лимиты по категориям расходов</p>
            </div>
          ) : (
            <div className="space-y-3">
              {budgets.map((budget) => (
                <BudgetProgress key={budget.id} budget={budget} />
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
