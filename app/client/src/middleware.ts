import { getAccessToken, withMiddlewareAuthRequired } from "@auth0/nextjs-auth0/edge";
import axios from "axios";
import { NextApiRequest } from "next";
import { NextResponse } from "next/server";

export default withMiddlewareAuthRequired(async function middleware(req) {
  const res = NextResponse.next();
  // const { accessToken } = await getAccessToken();
  return res;
});


export const config = {
  matcher: ["/pages/mlpal/:path*"],
};
