"use client"

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

const Login = () => {
  const router = useRouter();

  useEffect(() => {
    router.push(`${process.env.NEXT_PUBLIC_LOGIN_REDIRECT_URI}`);
  }, [router]);

  return <div>Redirecting to login...</div>;
};

export default Login;
