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

export function Sidebar({ open, onClose }: { open: boolean; onClose: () => void }) {
  const pathname = usePathname()

  return (
    <>
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
      </aside>

      {open && (
        <div className="fixed inset-0 z-50 md:hidden">
          <div className="fixed inset-0 bg-black/50" onClick={onClose} />
          <aside className="fixed top-0 left-0 bottom-0 w-72 bg-card z-50 p-4 animate-slide-up">
            <div className="flex items-center justify-between mb-6">
              <h1 className="text-xl font-bold flex items-center gap-2">
                <span className="text-2xl">💰</span>
                Finance
              </h1>
              <button onClick={onClose} className="text-muted-foreground text-xl">&times;</button>
            </div>
            <nav className="space-y-1">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = pathname === item.href
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={onClose}
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
          </aside>
        </div>
      )}

      <nav className="fixed bottom-0 left-0 right-0 z-40 md:hidden bg-card border-t safe-area-inset-bottom">
        <div className="flex items-center justify-around py-2 px-1">
          {navItems.slice(0, 5).map((item) => {
            const Icon = item.icon
            const isActive = pathname === item.href
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex flex-col items-center gap-0.5 px-2 py-1 rounded-xl text-xs font-medium transition-colors",
                  isActive
                    ? "text-primary"
                    : "text-muted-foreground"
                )}
              >
                <Icon className="h-5 w-5" />
                <span className="text-[10px]">{item.label}</span>
              </Link>
            )
          })}
        </div>
      </nav>
    </>
  )
}
