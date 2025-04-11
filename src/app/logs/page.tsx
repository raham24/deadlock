"use client";

import { Sheet, SheetContent, SheetTrigger, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { Menu } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function LogsPage() {
  return (
    <div className="flex min-h-screen w-full bg-muted/40">
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
              Dashboard
            </Link>
            <Link href="/logs" className="text-muted-foreground hover:text-black font-medium">
              Logs
            </Link>
          </nav>
        </SheetContent>
      </Sheet>

      <main className="flex-1 p-10 flex items-center justify-center">
        <h1 className="text-3xl font-semibold text-muted-foreground">📄 Logs page coming soon...</h1>
      </main>
    </div>
  );
}
