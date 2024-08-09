import type { NextApiRequest, NextApiResponse } from "next";
import { getAccessToken } from "@auth0/nextjs-auth0";
import axios from "axios";
import { NextResponse } from "next/server";

export async function GET(req: NextApiRequest, res: NextApiResponse) {
  const { accessToken } = await getAccessToken();

  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/pipeline/get-all`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
      }
    );
    console.log("PIPELINES", response.data);
    return NextResponse.json(response.data, { status: 200 });
  } catch (error: any) {
    console.error("Error fetching data: ", error);
    return NextResponse.json(
      {
        error: "Error fetching data",
      },
      { status: 500 }
    );
  }
}
