'use client';

import { useUser } from '@auth0/nextjs-auth0/client';

const Navbar: React.FC = () => {
 const { user, error, isLoading } = useUser();

  return (
    <nav>
      <h1>My App</h1>
      {user ? (
        <div className='flex gap-x-3'>
          <span>Welcome, {user.name}</span>
          <a href="/api/auth/logout">Logout</a>
                  <a href="/pages/dashboard">Dashboard</a>
        </div>
      ) : (
     <>
         <a href="/api/auth/login">Login</a>
     </>
      )}
    </nav>
  );
};

export default Navbar;
