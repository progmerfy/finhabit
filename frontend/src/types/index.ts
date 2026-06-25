export interface User {
  id: string
  telegram_id: number
  username: string | null
  first_name: string | null
  last_name: string | null
  photo_url: string | null
  level: string
  experience: number
  streak_days: number
  preferred_currency: string
  created_at: string
}

export interface DashboardData {
  balance: number
  monthly_income: number
  monthly_expense: number
  total_savings: number
  savings_percent: number
  financial_rating: number
  today_spent: number
  daily_limit: number
  daily_remaining: number
}

export interface IncomeCategory {
  id: string
  name: string
  icon: string
}

export interface Income {
  id: string
  user_id: string
  category_id: string
  category: IncomeCategory | null
  amount: number
  comment: string | null
  date: string
  created_at: string
}

export interface ExpenseCategory {
  id: string
  name: string
  icon: string
}

export interface Expense {
  id: string
  user_id: string
  category_id: string
  category: ExpenseCategory | null
  amount: number
  description: string | null
  date: string
  created_at: string
}

export interface Goal {
  id: string
  user_id: string
  name: string
  target_amount: number
  current_amount: number
  deadline: string | null
  is_completed: boolean
  progress_percent: number
  created_at: string
}

export interface Budget {
  id: string
  user_id: string
  category_name: string
  month: number
  year: number
  limit_amount: number
  spent: number
  usage_percent: number
}

export interface CategoryBreakdown {
  category_name: string
  icon: string
  amount: number
  percentage: number
  transaction_count: number
}

export interface AnalyticsData {
  total_income: number
  total_expense: number
  net_savings: number
  average_check: number
  transaction_count: number
  top_categories: CategoryBreakdown[]
  change_vs_last_period: number
}

export interface BalanceHistoryItem {
  date: string
  balance: number
  income: number
  expense: number
}

export interface MonthlyAnalytics {
  month: string
  income: number
  expense: number
  savings: number
}

export interface Notification {
  id: string
  user_id: string
  type: string
  title: string
  message: string
  is_read: boolean
  created_at: string
}

export interface Achievement {
  id: string
  name: string
  description: string
  icon: string
  unlocked: boolean
  unlocked_at: string | null
}
