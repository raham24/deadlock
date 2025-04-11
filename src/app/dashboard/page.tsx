"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Menu } from "lucide-react";
import { Sheet, SheetContent, SheetTrigger, SheetHeader, SheetTitle } from "@/components/ui/sheet";

export default function DashboardPage() {
  const [projectType, setProjectType] = useState("");
  const [logs, setLogs] = useState("🛳️ Ready to begin...");
  const [progress, setProgress] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  const simulateRun = () => {
    setIsRunning(true);
    setProgress(10);
    setLogs("🟡 Starting vessel dockerization...\n");

    setTimeout(() => setLogs((l) => l + "🔍 Detecting project type...\n"), 1000);
    setTimeout(() => setProgress(30), 1200);
    setTimeout(() => setLogs((l) => l + "📦 Preparing Docker templates...\n"), 1800);
    setTimeout(() => setProgress(60), 2400);
    setTimeout(() => setLogs((l) => l + "🐳 Building Docker image...\n"), 3200);
    setTimeout(() => setProgress(90), 4000);
    setTimeout(() => {
      setLogs((l) => l + "✅ Dockerization complete!\n🚀 Container ready.");
      setProgress(100);
      setIsRunning(false);
    }, 5000);
  };

  return (
    <div className="flex min-h-screen w-full bg-muted/40">
      {/* Sheet Sidebar */}
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="ghost" size="sm" className="absolute top-4 left-4 z-50 text-muted-foreground">
            <Menu size={18} />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-64 bg-white shadow-md z-50">
          <SheetHeader>
            <SheetTitle className="text-xl font-bold p-4">🛳️ Vessel</SheetTitle>
          </SheetHeader>
          <nav className="flex flex-col space-y-2 p-4">
            <Link href="/dashboard" className="text-muted-foreground hover:text-black font-medium">
              Dockerize
            </Link>
            <Link href="/logs" className="text-muted-foreground hover:text-black font-medium">
              New page coming soon...
            </Link>
          </nav>
        </SheetContent>
      </Sheet>

      {/* Main Content */}
      <main className="flex-1 p-6 sm:p-10 space-y-10">
        <div className="space-y-2">
          <h1 className="text-4xl font-bold">🛳️ Vessel Dashboard</h1>
          <p className="text-muted-foreground text-lg">
            Automate secure Dockerization for your web projects in seconds.
          </p>
        </div>

        <Card className="max-w-4xl">
          <CardHeader className="flex justify-between items-center">
            <CardTitle>Project Setup</CardTitle>
            <Badge variant="outline">Status: {isRunning ? "Processing" : "Idle"}</Badge>
          </CardHeader>
          <CardContent className="flex flex-col sm:flex-row gap-4">
            <Input
              placeholder="Enter project type (e.g. react, node, flask)"
              value={projectType}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setProjectType(e.target.value)}
              className="flex-1"
            />
            <Button disabled={isRunning || !projectType} onClick={simulateRun}>
              {isRunning ? "Running..." : "Dockerize"}
            </Button>
          </CardContent>
        </Card>

        {isMounted && (
          <Card className="max-w-4xl">
            <CardHeader>
              <CardTitle>Build Logs</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Progress value={progress} className="h-2" />
              <pre className="whitespace-pre-wrap text-sm bg-black text-green-400 p-4 rounded-md min-h-[150px]">
                {logs}
              </pre>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  );
}
