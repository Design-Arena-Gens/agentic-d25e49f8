import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'PerplexiPlay',
  description: 'Agent Playground and Testing Environment',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
