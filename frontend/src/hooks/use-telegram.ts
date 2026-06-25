"use client"

import { useEffect, useState } from "react"

interface TelegramWebApp {
  initData: string
  initDataUnsafe: {
    user?: {
      id: number
      first_name: string
      last_name?: string
      username?: string
      photo_url?: string
    }
  }
  ready: () => void
  expand: () => void
  close: () => void
  setHeaderColor: (color: string) => void
  setBackgroundColor: (color: string) => void
  disableVerticalSwipes: () => void
  MainButton: {
    setText: (text: string) => void
    show: () => void
    hide: () => void
    onClick: (cb: () => void) => void
    showProgress: () => void
    hideProgress: () => void
  }
  themeParams: {
    bg_color?: string
    text_color?: string
    hint_color?: string
    link_color?: string
    button_color?: string
    button_text_color?: string
    secondary_bg_color?: string
  }
}

declare global {
  interface Window {
    Telegram?: {
      WebApp: TelegramWebApp
    }
  }
}

export function useTelegram() {
  const [webApp, setWebApp] = useState<TelegramWebApp | null>(null)
  const [user, setUser] = useState<{
    id: number
    first_name: string
    last_name?: string
    username?: string
    photo_url?: string
  } | null>(null)

  useEffect(() => {
    const tg = window.Telegram?.WebApp
    if (tg) {
      tg.ready()
      tg.expand()
      tg.disableVerticalSwipes()
      setWebApp(tg)
      setUser(tg.initDataUnsafe.user || null)

      if (tg.themeParams.bg_color) {
        document.documentElement.style.setProperty("--tg-bg-color", tg.themeParams.bg_color)
      }
      if (tg.themeParams.text_color) {
        document.documentElement.style.setProperty("--tg-text-color", tg.themeParams.text_color)
      }
      if (tg.themeParams.button_color) {
        document.documentElement.style.setProperty("--tg-button-color", tg.themeParams.button_color)
      }
    }
  }, [])

  return { webApp, user }
}
