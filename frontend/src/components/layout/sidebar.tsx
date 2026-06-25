"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard,
  TrendingUp,
  TrendingDown,
  Target,
  PiggyBank,
  BarChart3,
  Brain,
  Trophy,
  Bell,
} from "lucide-react"

const navItems = [
  { href: "/", label: "Дашборд", icon: LayoutDashboard },
  { href: "/income", label: "Доходы", icon: TrendingUp },
  { href: "/expenses", label: "Расходы", icon: TrendingDown },
  { href: "/goals", label: "Цели", icon: Target },
  { href: "/budget", label: "Бюджет", icon: PiggyBank },
  { href: "/analytics", label: "Аналитика", icon: BarChart3 },
  { href: "/advisor", label: "AI Советник", icon: Brain },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="hidden md:flex w-64 flex-col border-r bg-card">
      <div className="p-6">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <span className="text-2xl">💰</span>
          Finance
        </h1>
      </div>
      <nav className="flex-1 px-3 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-200",
                isActive
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              )}
            >
              <Icon className="h-5 w-5" />
              {item.label}
            </Link>
          )
        })}
      </nav>
      <div className="p-4 border-t">
        <Link
          href="/advisor"
          className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-muted-foreground hover:bg-accent hover:text-accent-foreground transition-all"
        >
          <Bell className="h-5 w-5" />
          Уведомления
        </Link>
        <Link
          href="/goals"
          className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-muted-foreground hover:bg-accent hover:text-accent-foreground transition-all"
        >
          <Trophy className="h-5 w-5" />
          Достижения
        </Link>
      </div>
    </aside>
  )
}
