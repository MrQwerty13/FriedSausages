
import { useState } from "react";
import { Dashboard } from "./components/Dashboard";
import { Header } from "./components/Header";
import { Sidebar } from "./components/Sidebar";

type NavigationKey =
  | "monitoring"
  | "devices"
  | "reports"
  | "events"
  | "settings"
  | "flows";

const pageTitles: Record<NavigationKey, string> = {
  monitoring: "Мониторинг",
  devices: "Устройства",
  reports: "Отчёты",
  events: "События",
  settings: "Настройки",
  flows: "Потоки",
};

const pageSubtitles: Record<NavigationKey, string> = {
  monitoring: "Сводная панель контроля конфигураций и безопасности",
  devices: "Инвентаризация и состояние контролируемых объектов",
  reports: "Формирование отчётов по изменениям и проверкам",
  events: "Журнал событий, уведомлений и инцидентов",
  settings: "Параметры системы, модулей и пользователей",
  flows: "Сетевые потоки и взаимодействия устройств",
};

export default function App() {
  const [activeNavigationItem, setActiveNavigationItem] =
    useState<NavigationKey>("monitoring");

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar
        activeItem={activeNavigationItem}
        onNavigate={setActiveNavigationItem}
      />

      <div className="min-w-0 flex-1">
        <Header
          title={pageTitles[activeNavigationItem]}
          subtitle={pageSubtitles[activeNavigationItem]}
        />

        {activeNavigationItem === "monitoring" ? (
          <Dashboard />
        ) : (
          <main className="min-h-screen bg-slate-100 p-6">
            <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
              <h2 className="text-xl font-semibold text-slate-950">
                {pageTitles[activeNavigationItem]}
              </h2>

              <p className="mt-2 max-w-2xl text-sm text-slate-500">
                Раздел подготовлен как часть визуального каркаса. Команда может
                подключить сюда реальные данные, таблицы, формы и API-запросы.
              </p>
            </section>
          </main>
        )}
      </div>
    </div>
  );
}