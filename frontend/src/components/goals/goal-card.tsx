"use client"

import { formatCurrency } from "@/lib/utils"
import { Card, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Target, Calendar } from "lucide-react"
import type { Goal } from "@/types"

interface GoalCardProps {
  goal: Goal
  onAddMoney?: () => void
}

export function GoalCard({ goal, onAddMoney }: GoalCardProps) {
  const progress = Math.min(goal.progress_percent, 100)

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-5">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-2">
            <div className="h-10 w-10 rounded-xl bg-primary/10 flex items-center justify-center">
              <Target className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h3 className="font-semibold">{goal.name}</h3>
              {goal.deadline && (
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <Calendar className="h-3 w-3" />
                  {new Date(goal.deadline).toLocaleDateString("ru-RU")}
                </div>
              )}
            </div>
          </div>
          {goal.is_completed && (
            <Badge variant="success">Выполнено</Badge>
          )}
        </div>

        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Прогресс</span>
            <span className="font-medium">{progress}%</span>
          </div>
          <Progress value={progress} />
          <div className="flex justify-between text-sm pt-1">
            <span className="text-muted-foreground">
              {formatCurrency(goal.current_amount)}
            </span>
            <span className="font-medium">
              {formatCurrency(goal.target_amount)}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
