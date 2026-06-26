import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import Login from "./pages/Login";
import Patients from "./pages/Patients";
import Dashboard from "./pages/Dashboard";
import { LayoutDashboard, Users } from "lucide-react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import ProtectedRoute from "./utils/ProtectedRoute";

const links = [
  {
    name: "Dashboard",
    route: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "Patients",
    route: "/patients",
    icon: Users,
  },
];

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="login" element={<Login />} />
        <Route
          path="*"
          element={
            <div className="h-screen w-full p-4 overflow-hidden">
              <div className="flex flex-col gap-6 md:flex-row h-full">
                <Sidebar links={links} />
                <main className="flex-1 flex-col min-w-0 overflow-y-auto">
                  <Navbar />
                  <Routes>
                    <Route
                      path="/"
                      element={<Navigate to="/dashboard" replace />}
                    />
                    <Route
                      path="/dashboard"
                      element={
                        <ProtectedRoute>
                          <Dashboard />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/patients"
                      element={
                        <ProtectedRoute>
                          <Patients />
                        </ProtectedRoute>
                      }
                    />
                    <Route path="*" element={<div>TODO: PAGINA 404</div>} />
                  </Routes>
                </main>
              </div>
            </div>
          }
        />
      </Routes>
    </Router>
  );
}
