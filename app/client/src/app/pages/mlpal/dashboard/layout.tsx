// app/layout.tsx
"use client";

import { ReactNode } from "react";
import Header from "@/components/custom/Header";
import { UserProvider } from "@auth0/nextjs-auth0/client";
import { ViewProvider } from "@/context/ViewContext";

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <UserProvider>
      <ViewProvider>
        <div className="flex min-h-screen w-full flex-col">
            <Header />
            <main className="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-8">
            {children}
            </main>
        </div>
      </ViewProvider>
    </UserProvider>
  );
};

export default Layout;
