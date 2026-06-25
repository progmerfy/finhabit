"use client"

import { formatCurrency, getProgressColor } from "@/lib/utils"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import type { Budget } from "@/types"

interface BudgetProgressProps {
  budget: Budget
}

export function BudgetProgress({ budget }: BudgetProgressProps) {
  const color = getProgressColor(budget.usage_percent)

  return (
    <div className="space-y-2 p-4 rounded-xl bg-muted/50">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium">{budget.category_name}</span>
        <Badge
          variant={
            budget.usage_percent >= 100
              ? "destructive"
              : budget.usage_percent >= 80
              ? "warning"
              : "secondary"
          }
        >
          {budget.usage_percent}%
        </Badge>
      </div>
      <Progress value={Math.min(budget.usage_percent, 100)} />
      <div className="flex justify-between text-xs text-muted-foreground">
        <span>{formatCurrency(budget.spent)}</span>
        <span>{formatCurrency(budget.limit_amount)}</span>
      </div>
    </div>
  )
}
