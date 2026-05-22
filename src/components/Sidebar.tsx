import { useState } from "react";
import {
  BarChart3,
  CalendarDays,
  ChevronLeft,
  ChevronRight,
  FileText,
  GitBranch,
  MonitorCog,
  Network,
  Settings,
  ShieldCheck,
} from "lucide-react";

type NavigationKey =
  | "monitoring"
  | "devices"
  | "reports"
  | "events"
  | "settings"
  | "flows";

interface NavigationItem {
  id: NavigationKey;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
}

const navigationItems: NavigationItem[] = [
  {
    id: "monitoring",
    label: "Мониторинг",
    icon: BarChart3,
  },
  {
    id: "devices",
    label: "Устройства",
    icon: Network,
  },
  {
    id: "reports",
    label: "Отчёты",
    icon: FileText,
  },
  {
    id: "events",
    label: "События",
    icon: CalendarDays,
  },
  {
    id: "settings",
    label: "Настройки",
    icon: Settings,
  },
  {
    id: "flows",
    label: "Потоки",
    icon: GitBranch,
  },
];

interface SidebarProps {
  activeItem: NavigationKey;
  onNavigate: (item: NavigationKey) => void;
}

export function Sidebar({ activeItem, onNavigate }: SidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <aside
      className={[
        "flex min-h-screen flex-col border-r border-slate-700 bg-slate-800 text-slate-200 transition-all duration-300",
        isCollapsed ? "w-20" : "w-64",
      ].join(" ")}
    >
      <div className="flex h-16 items-center justify-between border-b border-slate-700 px-4">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-sky-500/20">
            <ShieldCheck className="h-5 w-5 text-sky-300" />
          </div>

          {!isCollapsed && (
            <div>
              <p className="text-sm font-semibold leading-none text-white">
                Config Inspector
              </p>
              <p className="mt-1 text-xs text-slate-400">Security Console</p>
            </div>
          )}
        </div>

        <button
          type="button"
          onClick={() => setIsCollapsed((value) => !value)}
          className="rounded-md p-1.5 text-slate-400 transition hover:bg-slate-700 hover:text-white"
          aria-label={isCollapsed ? "Развернуть меню" : "Свернуть меню"}
        >
          {isCollapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <ChevronLeft className="h-4 w-4" />
          )}
        </button>
      </div>

      <nav className="flex-1 space-y-1 px-3 py-5">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeItem === item.id;

          return (
            <button
              key={item.id}
              type="button"
              onClick={() => onNavigate(item.id)}
              className={[
                "group flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm transition",
                isActive
                  ? "bg-sky-500/20 text-white shadow-sm"
                  : "text-slate-400 hover:bg-slate-700/70 hover:text-white",
              ].join(" ")}
            >
              <Icon
                className={[
                  "h-5 w-5 shrink-0",
                  isActive ? "text-sky-300" : "text-slate-400 group-hover:text-white",
                ].join(" ")}
              />

              {!isCollapsed && <span>{item.label}</span>}
            </button>
          );
        })}
      </nav>

      <div className="border-t border-slate-700 p-3">
        <div
          className={[
            "flex items-center gap-3 rounded-xl bg-slate-900/60 p-3",
            isCollapsed ? "justify-center" : "",
          ].join(" ")}
        >
          <MonitorCog className="h-5 w-5 text-emerald-300" />

          {!isCollapsed && (
            <div>
              <p className="text-xs font-medium text-white">Core online</p>
              <p className="text-xs text-slate-400">WIN-L6TT7UGB9QJ</p>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}