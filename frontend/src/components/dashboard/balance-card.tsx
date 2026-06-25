"use client"

import { formatCurrency } from "@/lib/utils"
import { Card, CardContent } from "@/components/ui/card"
import { Wallet, ArrowUpRight, ArrowDownRight } from "lucide-react"

interface BalanceCardProps {
  balance: number
  todaySpent: number
  dailyLimit: number
  dailyRemaining: number
}

export function BalanceCard({ balance, todaySpent, dailyLimit, dailyRemaining }: BalanceCardProps) {
  return (
    <Card className="card-gradient border-0 text-white overflow-hidden relative">
      <CardContent className="p-6">
        <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-24 h-24 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2" />
        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-1">
            <Wallet className="h-5 w-5 text-white/80" />
            <span className="text-sm text-white/80">Текущий баланс</span>
          </div>
          <p className="text-3xl font-bold mb-4">
            {formatCurrency(balance)}
          </p>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <div className="flex items-center gap-1 text-xs text-white/70 mb-1">
                <ArrowDownRight className="h-3 w-3 text-red-300" />
                Потрачено
              </div>
              <p className="text-sm font-semibold">{formatCurrency(todaySpent)}</p>
            </div>
            <div>
              <div className="flex items-center gap-1 text-xs text-white/70 mb-1">
                Дневной лимит
              </div>
              <p className="text-sm font-semibold">{formatCurrency(dailyLimit)}</p>
            </div>
            <div>
              <div className="flex items-center gap-1 text-xs text-white/70 mb-1">
                <ArrowUpRight className="h-3 w-3 text-green-300" />
                Остаток
              </div>
              <p className="text-sm font-semibold">{formatCurrency(dailyRemaining)}</p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
