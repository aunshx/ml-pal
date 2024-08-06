import { handleAuth, handleLogin, handleLogout, handleCallback, handleProfile } from '@auth0/nextjs-auth0';
import type { NextApiRequest, NextApiResponse } from 'next';

export const GET = handleAuth({
    login: handleLogin({
        returnTo: "/pages/pal/dashboard",
    }),
});