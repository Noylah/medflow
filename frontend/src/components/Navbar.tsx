import { Menu, SearchIcon } from "lucide-react";
import UserInfo from "./UserInfo";

interface NavbarProps {}

export default function Navbar({}: NavbarProps) {
  return (
    <nav>
      <div className="flex min-h-12 w-full flex-col items-center gap-3 md:flex-row">
        <div className="flex w-full items-center gap-3 md:hidden md:w-auto">
          <div className="h-fit w-fit shrink-0 cursor-pointer rounded-full bg-primary p-3 transition-all duration-300 hover:bg-primary/80">
            <Menu />
          </div>
          <span className="text-2xl font-semibold">MedFlow</span>
        </div>

        <div className="flex w-full flex-1 flex-col items-center gap-3 sm:flex-row">
          <div className="hidden h-fit w-fit shrink-0 cursor-pointer rounded-full bg-primary p-3 transition-all duration-300 hover:translate-x-1 hover:bg-primary/60 lg:block text-background">
            <SearchIcon />
          </div>
          <div className="flex h-12 w-full min-w-37.5 items-center rounded-2xl border-3 border-primary px-4 text-slate-500 sm:flex-1">
            Search for patients
          </div>
          <UserInfo />
        </div>
      </div>
    </nav>
  );
}
