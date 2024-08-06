'use client'

import { authOptions } from '@/constants';
import { withPageAuthRequired, UserProfile, useUser} from '@auth0/nextjs-auth0/client';

interface DashboardProps {
    user: UserProfile
}

const Dashboard = () => {
  const { user } = useUser();

  return <div className='flex flex-col gap-y-3'>
    <div>
      Hello {user?.name}
    </div>
    <div>
      <a href="/api/auth/logout">Logout</a>
    </div>
  </div>;
}

export default Dashboard;
