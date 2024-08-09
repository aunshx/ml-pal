"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter, usePathname } from "next/navigation";
import {
  CircleUser,
  Menu,
  Package as PackageIcon,
  Home as HomeIcon,
  Layers as LayersIcon,
  Moon,
  Sun,
  MoveUp as MoveUpIcon,
  PlaneTakeoff as PlaneTakeoffIcon,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import {
  TooltipProvider,
  Tooltip,
  TooltipTrigger,
  TooltipContent,
} from "@/components/ui/tooltip";
import { Toggle } from "@/components/ui/toggle";
import { useTheme } from "next-themes";
import { useViewContext } from "@/context/ViewContext";

const Header = () => {
  const router = useRouter();
  const pathname = usePathname();
  const { activeView, setActiveView } = useViewContext();
  const { theme, setTheme } = useTheme();
  const [liftMode, setLiftMode] = useState(false);

  const toggleLiftMode = () => {
    setLiftMode((prevLiftMode) => !prevLiftMode);
  };

  useEffect(() => {
    if (pathname === "/dashboard") {
      setActiveView("home");
    } else if (pathname === "/dashboard/infra") {
      setActiveView("infra");
    }
  }, [pathname, setActiveView]);

  const handleNavigation = (view: "home" | "infra") => {
    setActiveView(view);
    router.push(view === "home" ? "/dashboard" : "/dashboard/infra");
  };

  const handleSettingsClick = () => {
    router.push("/settings");
  };

  return (
    <TooltipProvider>
      <header className="sticky top-0 z-50 flex h-16 w-full items-center justify-between px-4 md:px-6 border-b border-border bg-background/50 backdrop-blur-lg shadow-sm dark:bg-darkBackground/50">
        <div className="flex-shrink-0">
          <Link
            href="/dashboard"
            className="flex items-center gap-2 text-lg font-semibold md:text-base whitespace-nowrap text-foreground"
            onClick={() => setActiveView("home")}
          >
            <PackageIcon className="h-6 w-6" />
            <span className="ml-2">MLpal</span>
          </Link>
        </div>
        <div className="flex-1 flex justify-center">
          <nav className="hidden md:flex items-center gap-6 text-lg font-medium md:gap-5 md:text-sm lg:gap-6">
            <button
              onClick={() => handleNavigation("home")}
              className={`flex items-center gap-2 transition-colors duration-300 whitespace-nowrap ${
                activeView === "home"
                  ? "text-foreground"
                  : "text-muted-foreground"
              }`}
            >
              <HomeIcon className="h-5 w-5" />
              Home
            </button>
            <button
              onClick={() => handleNavigation("infra")}
              className={`flex items-center gap-2 transition-colors duration-300 whitespace-nowrap ${
                activeView === "infra"
                  ? "text-foreground"
                  : "text-muted-foreground"
              }`}
            >
              <LayersIcon className="h-5 w-5" />
              Infra Management
            </button>
          </nav>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Tooltip>
              <TooltipTrigger asChild>
                <Toggle
                  aria-label="Toggle lift mode"
                  onClick={toggleLiftMode}
                  className={`rounded-full p-1 transition-colors ${
                    liftMode
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-muted-foreground"
                  }`}
                >
                  {liftMode ? (
                    <MoveUpIcon className="h-4 w-4" />
                  ) : (
                    <PlaneTakeoffIcon className="h-4 w-4" />
                  )}
                </Toggle>
              </TooltipTrigger>
              <TooltipContent>
                {liftMode ? "Lift Mode On" : "Lift Mode Off"}
              </TooltipContent>
            </Tooltip>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" size="icon">
                  <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                  <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
                  <span className="sr-only">Toggle theme</span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={() => setTheme("light")}>
                  Light
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setTheme("dark")}>
                  Dark
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setTheme("system")}>
                  System
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="secondary" size="icon" className="rounded-full">
                <CircleUser className="h-5 w-5" />
                <span className="sr-only">Toggle user menu</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>My Account</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={handleSettingsClick}>Settings</DropdownMenuItem>
              <DropdownMenuItem>Support</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => window.open("/api/auth/logout","_self")}
              >
                Logout
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
        <Sheet>
          <SheetTrigger asChild>
            <Button
              variant="outline"
              size="icon"
              className="shrink-0 md:hidden ml-4"
            >
              <Menu className="h-5 w-5" />
              <span className="sr-only">Toggle navigation menu</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="left">
            <nav className="grid gap-6 text-lg font-medium">
              <Link
                href="/dashboard"
                className="flex items-center gap-2 text-lg font-semibold whitespace-nowrap text-foreground"
                onClick={() => setActiveView("home")}
              >
                <PackageIcon className="h-6 w-6" />
                <span className="ml-2">MLpal</span>
              </Link>
              <button
                onClick={() => handleNavigation("home")}
                className={`flex items-center gap-2 hover:text-foreground whitespace-nowrap ${
                  activeView === "home"
                    ? "text-foreground"
                    : "text-muted-foreground"
                }`}
              >
                <HomeIcon className="h-5 w-5" />
                Home
              </button>
              <button
                onClick={() => handleNavigation("infra")}
                className={`flex items-center gap-2 hover:text-foreground whitespace-nowrap ${
                  activeView === "infra"
                    ? "text-foreground"
                    : "text-muted-foreground"
                }`}
              >
                <LayersIcon className="h-5 w-5" />
                Infra Management
              </button>
            </nav>
          </SheetContent>
        </Sheet>
      </header>
    </TooltipProvider>
  );
};

export default Header;
