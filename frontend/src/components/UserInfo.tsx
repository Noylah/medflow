import {
  User,
  ChevronDown,
  Settings,
  LogOut,
  UserRoundPen,
} from "lucide-react";
import { useState } from "react";

interface UserInfoProps {}

export default function UserInfo({}: UserInfoProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div
      className="relative flex h-12 w-full min-w-48 shrink-0 items-center justify-between gap-3 rounded-2xl bg-foreground px-4 sm:w-auto cursor-pointer hover:bg-foreground/90 transition-colors duration-400 group"
      onClick={() => {
        setIsOpen(!isOpen);
      }}
    >
      <div className="flex shrink-0 items-center justify-center text-background">
        <User />
      </div>
      <div className="flex flex-1 flex-col justify-center sm:flex-initial">
        <span className="mb-1 text-[10px] leading-none font-bold tracking-wider text-background/50">
          DOCTOR
        </span>
        <span className="text-sm leading-none font-medium text-background">
          Mario Rossi
        </span>
      </div>
      <div
        className={`shrink-0 text-background group-hover:translate-y-0.5 transition-all duration-200 ${isOpen ? "rotate-180" : ""}`}
      >
        <ChevronDown />
      </div>
      {isOpen && (
        <div
          className="absolute left-0 top-[calc(100%+8px)] z-50 w-full rounded-2xl bg-foreground p-2 shadow-xl animate-in fade-in slide-in-from-top-2 duration-200"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex flex-col gap-1">
            <button className="flex w-full items-center gap-3 rounded-xl p-3 text-sm font-medium text-background cursor-pointer hover:bg-background/10 transition-colors">
              <UserRoundPen size={18} />
              <span>Profile</span>
            </button>
            <button className="flex w-full items-center gap-3 rounded-xl p-3 text-sm font-medium text-background cursor-pointer hover:bg-background/10 transition-colors">
              <Settings size={18} />
              <span>Settings</span>
            </button>
            <button className="flex w-full items-center gap-3 rounded-xl p-3 text-sm font-medium text-red-400 cursor-pointer hover:bg-red-500/10 transition-colors">
              <LogOut size={18} />
              <span>Log out</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
