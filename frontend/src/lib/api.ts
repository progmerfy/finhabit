const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

class ApiClient {
  private token: string | null = null

  setToken(token: string) {
    this.token = token
    if (typeof window !== "undefined") {
      localStorage.setItem("token", token)
    }
  }

  getToken(): string | null {
    if (typeof window !== "undefined") {
      return localStorage.getItem("token")
    }
    return this.token
  }

  private async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const token = this.getToken()
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    }
    if (token) {
      headers["Authorization"] = `Bearer ${token}`
    }

    const res = await fetch(`${API_URL}${path}`, { ...options, headers })

    if (!res.ok) {
      const error = await res.text()
      throw new Error(error || `HTTP ${res.status}`)
    }

    if (res.status === 204) return undefined as T
    return res.json()
  }

  // Auth
  login(telegramData: { telegram_id: number; username?: string; first_name?: string; last_name?: string; photo_url?: string }) {
    return this.request<any>("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify(telegramData),
    })
  }

  // Dashboard
  getDashboard() {
    return this.request<any>("/api/v1/dashboard")
  }

  // Income
  getIncomes() {
    return this.request<any[]>("/api/v1/income")
  }

  getIncomeCategories() {
    return this.request<any[]>("/api/v1/income/categories")
  }

  createIncome(data: { category_id: string; amount: number; comment?: string; date: string }) {
    return this.request<any>("/api/v1/income", {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  updateIncome(id: string, data: any) {
    return this.request<any>(`/api/v1/income/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    })
  }

  deleteIncome(id: string) {
    return this.request<void>(`/api/v1/income/${id}`, { method: "DELETE" })
  }

  // Expenses
  getExpenses() {
    return this.request<any[]>("/api/v1/expenses")
  }

  getExpenseCategories() {
    return this.request<any[]>("/api/v1/expenses/categories")
  }

  createExpense(data: { category_id: string; amount: number; description?: string; date: string }) {
    return this.request<any>("/api/v1/expenses", {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  updateExpense(id: string, data: any) {
    return this.request<any>(`/api/v1/expenses/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    })
  }

  deleteExpense(id: string) {
    return this.request<void>(`/api/v1/expenses/${id}`, { method: "DELETE" })
  }

  // Goals
  getGoals() {
    return this.request<any[]>("/api/v1/goals")
  }

  createGoal(data: { name: string; target_amount: number; current_amount?: number; deadline?: string }) {
    return this.request<any>("/api/v1/goals", {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  updateGoal(id: string, data: any) {
    return this.request<any>(`/api/v1/goals/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    })
  }

  deleteGoal(id: string) {
    return this.request<void>(`/api/v1/goals/${id}`, { method: "DELETE" })
  }

  addGoalTransaction(goalId: string, data: { amount: number; type: string }) {
    return this.request<any>(`/api/v1/goals/${goalId}/transactions`, {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  // Budgets
  getBudgets(month?: number, year?: number) {
    const params = new URLSearchParams()
    if (month) params.set("month", String(month))
    if (year) params.set("year", String(year))
    return this.request<any[]>(`/api/v1/budgets?${params}`)
  }

  createBudget(data: { category_name: string; month: number; year: number; limit_amount: number }) {
    return this.request<any>("/api/v1/budgets", {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  updateBudget(id: string, data: { limit_amount: number }) {
    return this.request<any>(`/api/v1/budgets/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    })
  }

  deleteBudget(id: string) {
    return this.request<void>(`/api/v1/budgets/${id}`, { method: "DELETE" })
  }

  // Analytics
  getAnalytics(period: string = "month") {
    return this.request<any>(`/api/v1/analytics?period=${period}`)
  }

  getBalanceHistory(months: number = 6) {
    return this.request<any[]>(`/api/v1/analytics/balance-history?months=${months}`)
  }

  getMonthlyAnalytics(months: number = 6) {
    return this.request<any[]>(`/api/v1/analytics/monthly?months=${months}`)
  }

  // Notifications
  getNotifications() {
    return this.request<any[]>("/api/v1/notifications")
  }

  getDailyReport() {
    return this.request<any>("/api/v1/notifications/daily", { method: "POST" })
  }

  markNotificationRead(id: string) {
    return this.request<any>(`/api/v1/notifications/${id}/read`, { method: "PUT" })
  }

  // AI Advisor
  getAIReport() {
    return this.request<{ report: string }>("/api/v1/ai-advisor/report")
  }

  // Achievements
  getAchievements() {
    return this.request<any[]>("/api/v1/achievements")
  }

  checkAchievements() {
    return this.request<any>("/api/v1/achievements/check", { method: "POST" })
  }

  updateStreak() {
    return this.request<any>("/api/v1/achievements/streak", { method: "POST" })
  }
}

export const api = new ApiClient()
