import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const auth = useContext(AuthContext);

  if (auth?.loading) {
    return (
      <div className="h-screen w-screen flex items-center justify-center font-mono">
        Loading...
      </div>
    );
  }

  if (!auth || !auth.user) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
