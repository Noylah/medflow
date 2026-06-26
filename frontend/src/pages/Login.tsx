import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

interface LoginProps {}

export default function Login({}: LoginProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const auth = useContext(AuthContext);
  return (
    <div className="w-screen h-screen flex items-center justify-evenly bg-slate-50">
      <div className="w-full max-w-md min-h-137.5 bg-foreground text-background rounded-3xl flex flex-col p-8 shadow-2xl justify-between">
        <div className="w-full text-center flex flex-col items-center gap-1">
          <span className="text-4xl font-black tracking-wider text-background">
            MedFlow
          </span>
          <span className="text-sm font-mono tracking-widest text-background/60 uppercase">
            Authentication
          </span>
        </div>
        <div className="flex-1 flex flex-col justify-center">
          <form
            className="flex flex-1 flex-col justify-center gap-5 my-6 w-full"
            onSubmit={(e) => {
              e.preventDefault();
              fetch("http://127.0.0.1:8000/api/login/", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  username: username,
                  password: password,
                }),
              })
                .then((response) => {
                  if (response.ok) {
                    return response.json();
                  }
                  return response.json().then((errorData) => {
                    throw new Error(errorData.detail || "Errore sconosciuto.");
                  });
                })
                .then((data) => {
                  if (auth) {
                    auth.loginUser(data.token, {
                      username: data.username,
                      first_name: data.first_name,
                      last_name: data.last_name,
                      role: data.role,
                      is_superuser: data.is_superuser,
                    });
                  }
                  navigate("/dashboard");
                })
                .catch((error) => {
                  console.error(error);
                });
            }}
          >
            <div className="flex flex-col gap-1.5">
              <label className="text-[11px] font-mono uppercase tracking-wider text-background/60 pl-1">
                Username
              </label>
              <input
                type="text"
                placeholder="doctor.medflow12"
                className="h-11 w-full rounded-xl bg-background/5 border border-background/10 px-4 text-sm text-background placeholder:text-background/30 outline-none transition-all duration-300 focus:border-primary focus:bg-background/10 focus:ring-1 focus:ring-primary"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <div className="flex justify-between items-center px-1">
                <label className="text-[11px] font-mono uppercase tracking-wider text-background/60">
                  Password
                </label>
                <a
                  href="#"
                  className="text-[11px] text-primary/80 hover:text-primary transition-colors"
                >
                  Forgot?
                </a>
              </div>
              <input
                type="password"
                placeholder="••••••••"
                className="h-11 w-full rounded-xl bg-background/5 border border-background/10 px-4 text-sm text-background placeholder:text-background/30 outline-none transition-all duration-300 focus:border-primary focus:bg-background/10 focus:ring-1 focus:ring-primary"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <button
              type="submit"
              className="mt-2 flex h-11 w-full cursor-pointer items-center justify-center rounded-xl bg-primary font-semibold text-foreground transition-all duration-300 hover:opacity-90 active:scale-[0.98] shadow-lg shadow-primary/20"
            >
              Sign In
            </button>
          </form>
        </div>

        <div className="text-center text-[10px] font-mono text-background/30">
          &copy; 2026 MedFlow Inc. All rights reserved.
        </div>
      </div>
    </div>
  );
}
