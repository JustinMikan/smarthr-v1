import { Sidebar } from "@/components/sidebar"
import { SearchBar } from "@/components/search-bar"
import { QuickAccessCards } from "@/components/quick-access-cards"

export default function DashboardPage() {
  return (
    <div className="flex min-h-screen bg-background">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <main className="flex-1 flex flex-col">
        {/* Hero Section */}
        <div className="flex-1 flex flex-col items-center justify-center px-8 py-12">
          <div className="w-full max-w-4xl mx-auto space-y-12">
            {/* Greeting */}
            <div className="text-center space-y-4">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 text-primary rounded-full text-sm font-medium">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
                </span>
                AI 助理已就緒
              </div>
              <h1 className="text-4xl md:text-5xl font-bold text-foreground tracking-tight text-balance">
                Hello, Alex! <br className="md:hidden" />
                <span className="text-primary">有什麼我可以幫你的嗎？</span>
              </h1>
              <p className="text-lg text-muted-foreground max-w-xl mx-auto">
                我是您的智慧人資助理，可以回答任何關於公司規章制度的問題
              </p>
            </div>

            {/* Search Bar */}
            <SearchBar />

            {/* Quick Access Section */}
            <div className="space-y-6">
              <div className="text-center">
                <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
                  快速存取 Quick Access
                </h2>
              </div>
              <QuickAccessCards />
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="py-4 px-8 border-t border-border">
          <p className="text-center text-sm text-muted-foreground">© 2026 SmartHR. 由 AI 驅動的企業人資系統。</p>
        </footer>
      </main>
    </div>
  )
}
