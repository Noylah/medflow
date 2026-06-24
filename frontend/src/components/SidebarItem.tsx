import { type LucideIcon } from "lucide-react";
import { Link } from "react-router-dom";

interface SidebarItemProps {
  icon: LucideIcon;
  isActive: boolean;
  children?: React.ReactNode;
  to: string;
}

export default function SidebarItem({
  icon: Icon,
  children,
  isActive,
  to,
}: SidebarItemProps) {
  return (
    <Link
      to={to}
      className={`flex cursor-pointer gap-3 text-sm font-semibold transition-all duration-400 hover:translate-x-1 ${
        isActive
          ? "text-primary hover:text-primary-dark"
          : "text-background hover:text-primary"
      }`}
    >
      <Icon size={24} />
      <span>{children}</span>
    </Link>
  );
}
