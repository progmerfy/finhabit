"use client"

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts"

interface PieChartData {
  name: string
  value: number
  color?: string
}

const COLORS = [
  "hsl(142.1, 76.2%, 36.3%)",
  "hsl(24.6, 95%, 53.1%)",
  "hsl(217.2, 91.2%, 59.8%)",
  "hsl(271, 91%, 65.1%)",
  "hsl(330, 81%, 60%)",
  "hsl(45, 93%, 47.1%)",
  "hsl(0, 84%, 60%)",
  "hsl(200, 80%, 50%)",
]

interface Props {
  data: PieChartData[]
  title?: string
}

export function PieChartComponent({ data, title }: Props) {
  if (data.length === 0) {
    return (
      <div className="flex items-center justify-center h-[300px] text-muted-foreground">
        Нет данных
      </div>
    )
  }

  return (
    <div className="w-full">
      {title && <h3 className="text-sm font-medium mb-3">{title}</h3>}
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            paddingAngle={2}
            dataKey="value"
          >
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              background: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "12px",
            }}
            formatter={(value: number) => [`${value.toFixed(1)}%`, ""]}
          />
          <Legend
            verticalAlign="bottom"
            height={36}
            formatter={(value: string) => (
              <span style={{ color: "hsl(var(--foreground))", fontSize: "12px" }}>{value}</span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
