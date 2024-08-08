"use client";

import { getAccessToken } from "@auth0/nextjs-auth0/edge";
import {
  createContext,
  FC,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from "react";


interface AuthContextProps {
  token: string;
  handleTokenChange: (token: string) => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
  return null;
}

export const AuthProvider: FC<AuthProviderProps> = ({ children }) => {
  const [token, setToken] = useState<string>("");

  const handleTokenChange = (val: string) => setToken(val);

  useEffect(() => {
    const cookieToken = getCookie('x-access-token');
    if (cookieToken) {
      setToken(cookieToken);
      console.log(cookieToken)
    }

  }, []);

  return (
    <AuthContext.Provider value={{ token, handleTokenChange }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuthContext = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuthContext must be used within an AuthProvider");
  }
  return context;
};
