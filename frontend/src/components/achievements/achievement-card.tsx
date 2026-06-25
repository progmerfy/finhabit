"use client"

import { Card, CardContent } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import type { Achievement } from "@/types"

interface AchievementCardProps {
  achievement: Achievement
}

export function AchievementCard({ achievement }: AchievementCardProps) {
  return (
    <Card
      className={cn(
        "transition-all duration-300",
        achievement.unlocked ? "opacity-100" : "opacity-50 grayscale"
      )}
    >
      <CardContent className="p-4 text-center">
        <div className="text-3xl mb-2">{achievement.icon}</div>
        <h3 className="text-sm font-semibold mb-1">{achievement.name}</h3>
        <p className="text-xs text-muted-foreground">{achievement.description}</p>
        {achievement.unlocked_at && (
          <p className="text-xs text-primary mt-2">
            {new Date(achievement.unlocked_at).toLocaleDateString("ru-RU")}
          </p>
        )}
      </CardContent>
    </Card>
  )
}
