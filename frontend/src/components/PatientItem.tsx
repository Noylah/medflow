import { Ellipsis, User, Settings, Trash2, X } from "lucide-react"; // Cambiate icone per il contesto
import { useState } from "react";

interface PatientItemProps {
  first_name: string;
  last_name: string;
  fiscal_code: string;
  birth_date: string;
  last_encounter_status: string;
}

export default function PatientItem({
  first_name,
  last_name,
  fiscal_code,
  birth_date,
  last_encounter_status,
}: PatientItemProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="flex min-h-36 w-full max-w-sm flex-col justify-between rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-start justify-between">
        <div className="flex flex-col">
          <span className="text-base font-bold text-foreground">
            {last_name} {first_name}
          </span>
          <span className="mt-0.5 font-mono text-xs text-slate-400">
            {fiscal_code}
          </span>
        </div>

        <div className="relative">
          <div
            className="flex h-7 cursor-pointer items-center justify-center rounded-full bg-foreground px-2.5 text-[10px] font-bold tracking-wider text-background uppercase transition-all duration-300 hover:bg-foreground/80"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X size={18} /> : <Ellipsis size={18} />}
          </div>

          {isOpen && (
            <div
              className="absolute right-0 top-[calc(100%+6px)] z-50 min-w-37.5 rounded-2xl bg-foreground p-1.5 shadow-xl animate-in fade-in slide-in-from-top-2 duration-200"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex flex-col gap-0.5">
                <button className="flex w-full items-center gap-2.5 rounded-xl p-2 text-left text-xs font-medium text-background cursor-pointer hover:bg-background/10 transition-colors">
                  <User size={14} />
                  <span>Profile</span>
                </button>
                <button className="flex w-full items-center gap-2.5 rounded-xl p-2 text-left text-xs font-medium text-background cursor-pointer hover:bg-background/10 transition-colors">
                  <Settings size={14} />
                  <span>Modify</span>
                </button>
                <button className="flex w-full items-center gap-2.5 rounded-xl p-2 text-left text-xs font-medium text-red-400 cursor-pointer hover:bg-red-500/10 transition-colors">
                  <Trash2 size={14} />
                  <span>Delete</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="mt-4 flex justify-between border-t border-slate-100 pt-2 text-xs text-slate-400">
        <div className="flex flex-col">
          <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">
            Birth
          </span>
          <span className="font-medium text-foreground">{birth_date}</span>
        </div>
        <div className="flex flex-col text-right">
          <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">
            Last Encounter
          </span>
          <span className="font-bold text-green-600">
            {last_encounter_status}
          </span>
        </div>
      </div>
    </div>
  );
}
