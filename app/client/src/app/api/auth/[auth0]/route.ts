import { handleAuth, handleLogin, handleLogout, handleCallback, handleProfile } from '@auth0/nextjs-auth0';
import type { NextApiRequest, NextApiResponse } from 'next';


export const GET = handleAuth({
  login: handleLogin((req) => {
    return {
      authorizationParams: {
        audience: "https://dev-mw81v5ryzhqlgb73.us.auth0.com/api/v2/",
      },
      returnTo: "/pages/mlpal/dashboard",
    };
  }),
});
