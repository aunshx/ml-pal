"use client";

import { useEffect } from "react";
import useSWR from 'swr';
import { useUser } from "@auth0/nextjs-auth0/client";
import { getAccessToken  } from "@auth0/nextjs-auth0";
import HomeView from "@/components/dashboard/HomeView";
import { NextResponse } from "next/server";
import axios from "axios";


export default function DashboardPage() {
  const { user  } = useUser();

  return (
    <HomeView />
  );
}
