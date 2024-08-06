"use client";

import { useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

const Callback = () => {
  const router = useRouter();
  
  const searchParams = useSearchParams();

  useEffect(() => {
    const handleCallbackRedirect = async () => {
      console.log('HELLO WORLD')
      const accessToken = searchParams.get('access_token');
            console.log(accessToken)
      if (accessToken) {
        localStorage.setItem('accessToken', accessToken);
        router.push('/auth/get-user');
      }
    };

    handleCallbackRedirect();
  }, [router, searchParams]);

  return <div>Redirecting...</div>;
};

export default Callback;
