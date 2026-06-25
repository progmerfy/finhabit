"use client"

import { type LucideIcon } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"

interface StatsCardProps {
  title: string
  value: string
  icon: LucideIcon
  gradient: string
}

export function StatsCard({ title, value, icon: Icon, gradient }: StatsCardProps) {
  return (
    <Card className={`${gradient} border-0 text-white overflow-hidden relative`}>
      <CardContent className="p-4">
        <div className="relative z-10">
          <Icon className="h-5 w-5 text-white/80 mb-2" />
          <p className="text-xs text-white/70 mb-1">{title}</p>
          <p className="text-lg font-bold">{value}</p>
        </div>
      </CardContent>
    </Card>
  )
}
