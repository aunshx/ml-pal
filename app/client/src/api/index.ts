import axios from "axios";

export const createPipeline = async (token: string) => {
  try {
    const apiResponse = await axios.post(
      `http://localhost:8000/pipeline/create`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    return apiResponse.data;
  } catch (e: any) {
    console.error("Error making external API request:", e);
  }
};