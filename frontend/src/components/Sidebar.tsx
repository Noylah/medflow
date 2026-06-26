import { type LucideIcon } from "lucide-react";
import SidebarItem from "./SidebarItem";
import { useLocation } from "react-router-dom";

interface LinkItem {
  name: string;
  route: string;
  icon: LucideIcon;
}

interface SidebarProps {
  links: LinkItem[];
}

export default function Sidebar({ links }: SidebarProps) {
  const location = useLocation();
  return (
    <aside className="hidden h-full w-64 shrink-0 flex-col items-center rounded-3xl bg-foreground p-6 md:flex">
      <div className="mb-6 text-3xl font-bold text-background">MedFlow</div>
      <div className="flex flex-col justify-center gap-4 self-start">
        {links.map((link) => {
          return (
            <SidebarItem
              isActive={location.pathname === link.route}
              icon={link.icon}
              to={link.route}
              key={link.route}
            >
              {link.name}
            </SidebarItem>
          );
        })}
      </div>
    </aside>
  );
}
