"use client";

import HomeView from "@/components/dashboard/HomeView";
import { useState } from "react";



export default function DashboardPage() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/pipeline/create');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const result = await response.json();
      setData(result);
    } catch (error:any) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <HomeView />
      <div className="flex items-center justify-center w-100p h-8 border-2p border-solid border-gray-900" onClick={fetchData}>
        Hello
      </div>
    </>
  );
}
