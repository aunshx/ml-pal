import { UserProvider } from '@auth0/nextjs-auth0/client';
import './globals.css'

interface MyAppProps {
  children: any
}

function MyApp({ children }: Readonly<MyAppProps>) {
  return (
    <html lang="en">
      <body>
        <UserProvider>
          {children}
        </UserProvider>
      </body>
    </html>
  );
}

export default MyApp;

