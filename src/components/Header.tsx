import { useState } from "react";
import {
  Bell,
  CheckCircle2,
  ChevronDown,
  LogOut,
  Menu,
  Search,
  Settings,
  User,
} from "lucide-react";

interface HeaderProps {
  title: string;
  subtitle?: string;
}

const systemStatus = {
  label: "Система работает",
  description: "Все основные службы доступны",
};

export function Header({ title, subtitle }: HeaderProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);

  const hasSearchValue = searchQuery.trim().length > 0;

  return (
    <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/95 backdrop-blur">
      <div className="flex h-16 items-center justify-between gap-4 px-6">
        <div className="flex items-center gap-4">
          <button
            type="button"
            className="rounded-lg p-2 text-slate-500 transition hover:bg-slate-100 hover:text-slate-900 lg:hidden"
            aria-label="Открыть меню"
          >
            <Menu className="h-5 w-5" />
          </button>

          <div>
            <h1 className="text-lg font-semibold text-slate-900">{title}</h1>
            {subtitle && <p className="text-xs text-slate-500">{subtitle}</p>}
          </div>
        </div>

        <div className="hidden flex-1 justify-center px-6 md:flex">
          <div className="relative w-full max-w-xl">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />

            <input
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
              type="text"
              placeholder="Поиск устройств, событий, правил..."
              className="h-10 w-full rounded-xl border border-slate-200 bg-slate-50 pl-10 pr-4 text-sm outline-none transition focus:border-sky-400 focus:bg-white focus:ring-4 focus:ring-sky-100"
            />

            {hasSearchValue && (
              <div className="absolute left-0 top-12 w-full rounded-xl border border-slate-200 bg-white p-3 shadow-xl">
                <p className="text-xs text-slate-500">
                  Поиск по запросу:{" "}
                  <span className="font-medium text-slate-900">{searchQuery}</span>
                </p>
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden items-center gap-2 rounded-xl border border-emerald-200 bg-emerald-50 px-3 py-2 md:flex">
            <CheckCircle2 className="h-4 w-4 text-emerald-600" />
            <div>
              <p className="text-xs font-medium text-emerald-700">
                {systemStatus.label}
              </p>
              <p className="text-[11px] text-emerald-600">
                {systemStatus.description}
              </p>
            </div>
          </div>

          <div className="relative">
            <button
              type="button"
              onClick={() => setIsNotificationsOpen((value) => !value)}
              className="relative rounded-xl border border-slate-200 p-2 text-slate-500 transition hover:bg-slate-50 hover:text-slate-900"
              aria-label="Уведомления"
            >
              <Bell className="h-5 w-5" />
              <span className="absolute right-1.5 top-1.5 h-2.5 w-2.5 rounded-full bg-red-500 ring-2 ring-white" />
            </button>

            {isNotificationsOpen && (
              <div className="absolute right-0 top-12 w-80 rounded-2xl border border-slate-200 bg-white p-3 shadow-xl">
                <p className="mb-3 text-sm font-semibold text-slate-900">
                  Уведомления
                </p>

                <div className="space-y-2">
                  <div className="rounded-xl bg-red-50 p-3">
                    <p className="text-xs font-medium text-red-700">
                      Критичное изменение конфигурации
                    </p>
                    <p className="mt-1 text-xs text-red-600">
                      Cisco 10.72.14.190 — изменён список доступа.
                    </p>
                  </div>

                  <div className="rounded-xl bg-yellow-50 p-3">
                    <p className="text-xs font-medium text-yellow-700">
                      Предупреждение безопасности
                    </p>
                    <p className="mt-1 text-xs text-yellow-600">
                      На Windows localhost обнаружены устаревшие правила.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="relative">
            <button
              type="button"
              onClick={() => setIsProfileMenuOpen((value) => !value)}
              className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm transition hover:bg-slate-50"
            >
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-800 text-white">
                <User className="h-4 w-4" />
              </div>
              <span className="hidden font-medium text-slate-700 sm:block">
                root
              </span>
              <ChevronDown className="h-4 w-4 text-slate-400" />
            </button>

            {isProfileMenuOpen && (
              <div className="absolute right-0 top-12 w-56 rounded-2xl border border-slate-200 bg-white p-2 shadow-xl">
                <button
                  type="button"
                  className="flex w-full items-center gap-2 rounded-xl px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50"
                >
                  <Settings className="h-4 w-4" />
                  Настройки профиля
                </button>

                <button
                  type="button"
                  className="flex w-full items-center gap-2 rounded-xl px-3 py-2 text-left text-sm text-red-600 hover:bg-red-50"
                >
                  <LogOut className="h-4 w-4" />
                  Выйти
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}