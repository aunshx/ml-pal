// // src/app/auth/get-user/page.tsx
// "use client";

// import { useContext, useEffect, useState } from 'react';
// import { useRouter } from 'next/navigation';
// import axios from 'axios';
// import { useUser } from '@auth0/nextjs-auth0/client';

// const GetUser = () => {
//   const [error, setError] = useState<string | null>(null);
//   const { user } = useUser();

//   const router = useRouter();

//   useEffect(() => {
//     const fetchUserDetails = async () => {
//       const accessToken = localStorage.getItem('accessToken');
//       if (!accessToken) {
//         router.push('/auth/login');
//         return;
//       }

//       try {
//         const response = await axios.get('http://localhost:8000/get-user', {
//           headers: {
//             Authorization: `Bearer ${accessToken}`
//           }
//         });
//         setUser(response.data);
//         router.push('/pages/dashboard');
//       } catch (error) {
//         console.error('Error fetching user details:', error);
//         setError('Failed to fetch user details.');
//         localStorage.removeItem('accessToken');
//         router.push('/auth/login');
//       }
//     };

//     fetchUserDetails();
//   // eslint-disable-next-line react-hooks/exhaustive-deps
//   }, []);

//   if (error) {
//     return <div>{error}</div>;
//   }

//   return <div>Loading...</div>;
// };

// export default GetUser;
