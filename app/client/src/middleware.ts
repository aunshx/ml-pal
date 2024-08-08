import { getAccessToken, withMiddlewareAuthRequired } from "@auth0/nextjs-auth0/edge";
import { NextApiRequest } from "next";
import { NextResponse } from "next/server";

export default withMiddlewareAuthRequired(async function middleware(req) {
  const res = NextResponse.next();
  const { accessToken } = await getAccessToken();
  console.log("ACCESS TOKEN", accessToken);
  // res.cookies.set('hl', user.language);
  return res;
});

export const config = {
  matcher: ["/pages/mlpal/:path*"],
};
