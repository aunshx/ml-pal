"use client";

import Header from "@/components/custom/Header";
import { AppContextProvider } from "@/context/AppContextProvider";
import { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <AppContextProvider>
        <div className="flex min-h-screen w-full flex-col">
            <Header />
            <main className="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-8">
            {children}
            </main>
        </div>
    </AppContextProvider>
  );
};

export default Layout;
