import { createContext, useState, useEffect, type ReactNode } from "react";
import Loading from "../pages/Loading";

interface UserData {
  username: string;
  first_name: string;
  last_name: string;
  role: string;
  is_superuser: boolean;
}

interface AuthContextType {
  token: string | null;
  user: UserData | null;
  loading: boolean;
  loginUser: (token: string, user: UserData) => void;
  logoutUser: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined,
);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token"),
  );
  const [user, setUser] = useState<UserData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const loginUser = (newToken: string, userData: UserData) => {
    localStorage.setItem("token", newToken);
    localStorage.setItem("user", JSON.stringify(userData));
    setToken(newToken);
    setUser(userData);
  };

  const logoutUser = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ token, user, loading, loginUser, logoutUser }}
    >
      {loading && <Loading />}
      {!loading && children}
    </AuthContext.Provider>
  );
};
