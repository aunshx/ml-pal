"use client";

import { ReactNode } from "react";
import Header from "@/components/custom/Header";
import { AppContextProvider } from "@/context/AppContextProvider";

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <AppContextProvider>
      <div className="flex h-screen w-full flex-col">
        <Header />
        <main className="w-full h-full">
          {children}
        </main>
      </div>
    </AppContextProvider>
  );
};

export default Layout;