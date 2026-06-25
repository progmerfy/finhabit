"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import { useTelegram } from "./use-telegram"

export function useInit() {
  const { user } = useTelegram()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const init = async () => {
      if (!user) {
        setLoading(false)
        return
      }
      try {
        const result = await api.login({
          telegram_id: user.id,
          username: user.username,
          first_name: user.first_name,
          last_name: user.last_name,
          photo_url: user.photo_url,
        })
        api.setToken(result.id)
        await api.updateStreak()
      } catch (e: any) {
        console.error("Auth error:", e)
        setError(e.message)
      } finally {
        setLoading(false)
      }
    }
    init()
  }, [user])

  return { loading, error }
}
