"use client";

import { createPipeline } from "@/api";
import HomeView from "@/components/dashboard/HomeView";
import { useAuthContext } from "@/context/AuthContext";
import { useEffect } from "react";


export default function DashboardPage() {
  const { token } = useAuthContext();  

  return (
    <>
      <HomeView />
      <div className="flex items-center justify-center w-100p h-8" onClick={() => createPipeline(token)}>
        Hello
      </div>
    </>
  );
}
