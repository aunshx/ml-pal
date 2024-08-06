import { withPageAuthRequired } from '@auth0/nextjs-auth0/client';
import { UserProfile } from '@auth0/nextjs-auth0/client';

interface DashboardProps {
    user: UserProfile
}

const Dashboard = ({ user }: DashboardProps) => {
  return <div>Hello {user.name}</div>;
}

export default withPageAuthRequired(Dashboard);
