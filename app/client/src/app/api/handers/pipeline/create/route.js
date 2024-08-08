import { NextResponse } from 'next/server';
import { getAccessToken, withApiAuthRequired } from '@auth0/nextjs-auth0';
import axios from 'axios';

const GET = withApiAuthRequired(async function GET(req) {
  const res = new NextResponse();

  try {
    const { accessToken } = await getAccessToken(req, res);

    console.log('ACCESS TOKEN', accessToken)

    const apiResponse = await axios.get('https://api.example.com/data', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    return NextResponse.json(apiResponse.data, res);

  } catch (error) {
    console.error('Error making external API request:', error);
    return NextResponse.error({ status: 500, statusText: 'Internal Server Error' });
  }
});

export { GET };