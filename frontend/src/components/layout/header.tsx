"use client"

import { useTelegram } from "@/hooks/use-telegram"
import { useTheme } from "@/app/providers"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Moon, Sun, Menu } from "lucide-react"

interface HeaderProps {
  onMenuClick: () => void
}

export function Header({ onMenuClick }: HeaderProps) {
  const { user } = useTelegram()
  const { theme, toggleTheme } = useTheme()

  return (
    <header className="sticky top-0 z-30 flex h-14 items-center gap-4 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 px-4 md:px-6">
      <Button variant="ghost" size="icon" className="md:hidden" onClick={onMenuClick}>
        <Menu className="h-5 w-5" />
      </Button>
      <div className="flex-1" />
      <Button variant="ghost" size="icon" onClick={toggleTheme}>
        {theme === "dark" ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
      </Button>
      {user && (
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium hidden sm:block">
            {user.first_name}
          </span>
          <Avatar className="h-8 w-8">
            {user.photo_url && <AvatarImage src={user.photo_url} />}
            <AvatarFallback>
              {user.first_name?.[0] || "U"}
            </AvatarFallback>
          </Avatar>
        </div>
      )}
    </header>
  )
}
