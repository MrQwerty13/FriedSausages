import { useMemo, useState } from "react";
import {
  AlertTriangle,
  CheckCircle2,
  ChevronDown,
  Download,
  Filter,
  MoreHorizontal,
  RefreshCw,
  ShieldAlert,
  ShieldCheck,
  SlidersHorizontal,
  TrendingUp,
} from "lucide-react";
import type {
  Device,
  DeviceStatus,
  EventLog,
  MetricCard,
  SecurityRule,
  Severity,
} from "../types";

type DashboardTab = "overview" | "devices" | "security" | "events";

const metricCards: MetricCard[] = [
  {
    id: "changes",
    title: "Контроль изменений",
    value: 16,
    description: "отчётов с нарушениями",
    trend: 76,
    color: "red",
  },
  {
    id: "security",
    title: "Проверки безопасности",
    value: "1274 / 2585",
    description: "выполнено правил",
    trend: 49,
    color: "green",
  },
  {
    id: "vulnerabilities",
    title: "Уязвимые устройства",
    value: 12,
    description: "требуют внимания",
    trend: 64,
    color: "yellow",
  },
  {
    id: "available",
    title: "Состояние устройств",
    value: 126,
    description: "доступны в сети",
    trend: 82,
    color: "blue",
  },
];

const mockDevices: Device[] = [
  {
    id: "dev-1",
    name: "Windows localhost",
    ipAddress: "127.0.0.1",
    type: "Windows",
    vendor: "Microsoft",
    status: "available",
    securityScore: 58,
    vulnerabilityLevel: "high",
    criticalVulnerabilities: 0,
    highVulnerabilities: 20,
    mediumVulnerabilities: 58,
    lowVulnerabilities: 13,
    lastScanAt: "30.09.2021 15:56",
    configChanged: true,
  },
  {
    id: "dev-2",
    name: "Cisco 10.72.14.190",
    ipAddress: "10.72.14.190",
    type: "Cisco IOS",
    vendor: "Cisco",
    status: "critical",
    securityScore: 63,
    vulnerabilityLevel: "critical",
    criticalVulnerabilities: 1,
    highVulnerabilities: 2,
    mediumVulnerabilities: 1,
    lowVulnerabilities: 1,
    lastScanAt: "16.09.2021 14:59",
    configChanged: true,
  },
  {
    id: "dev-3",
    name: "Cisco ASA 10.72.10.142",
    ipAddress: "10.72.10.142",
    type: "Cisco ASA",
    vendor: "Cisco",
    status: "warning",
    securityScore: 64,
    vulnerabilityLevel: "high",
    criticalVulnerabilities: 0,
    highVulnerabilities: 14,
    mediumVulnerabilities: 8,
    lowVulnerabilities: 0,
    lastScanAt: "18.09.2021 12:20",
    configChanged: false,
  },
  {
    id: "dev-4",
    name: "Fortinet Fortigate",
    ipAddress: "10.10.8.148",
    type: "Fortinet",
    vendor: "Fortinet",
    status: "available",
    securityScore: 63,
    vulnerabilityLevel: "medium",
    criticalVulnerabilities: 0,
    highVulnerabilities: 7,
    mediumVulnerabilities: 14,
    lowVulnerabilities: 0,
    lastScanAt: "18.09.2021 13:45",
    configChanged: false,
  },
  {
    id: "dev-5",
    name: "JunOS",
    ipAddress: "10.72.10.144",
    type: "JunOS",
    vendor: "Juniper",
    status: "offline",
    securityScore: 65,
    vulnerabilityLevel: "low",
    criticalVulnerabilities: 0,
    highVulnerabilities: 4,
    mediumVulnerabilities: 2,
    lowVulnerabilities: 3,
    lastScanAt: "19.09.2021 09:00",
    configChanged: false,
  },
  {
    id: "dev-6",
    name: "Smart R80",
    ipAddress: "10.72.10.137",
    type: "Check Point",
    vendor: "Check Point",
    status: "auth_error",
    securityScore: 62,
    vulnerabilityLevel: "high",
    criticalVulnerabilities: 0,
    highVulnerabilities: 66,
    mediumVulnerabilities: 6,
    lowVulnerabilities: 3,
    lastScanAt: "20.09.2021 10:15",
    configChanged: true,
  },
];

const mockSecurityRules: SecurityRule[] = [
  {
    id: "rule-1",
    name: "Запрет Telnet",
    deviceName: "Cisco 10.72.14.190",
    status: "failed",
    severity: "critical",
    description: "Обнаружен небезопасный удалённый доступ через Telnet.",
    checkedAt: "30.09.2021 15:56",
  },
  {
    id: "rule-2",
    name: "Проверка SNMP community",
    deviceName: "Cisco ASA 10.72.10.142",
    status: "failed",
    severity: "high",
    description: "Используется небезопасная community-строка public/private.",
    checkedAt: "30.09.2021 15:55",
  },
  {
    id: "rule-3",
    name: "Пароли в открытом виде",
    deviceName: "Windows localhost",
    status: "warning",
    severity: "medium",
    description: "Обнаружены потенциально слабые параметры хранения паролей.",
    checkedAt: "30.09.2021 15:52",
  },
  {
    id: "rule-4",
    name: "Наличие централизованного логирования",
    deviceName: "Fortinet Fortigate",
    status: "passed",
    severity: "none",
    description: "Передача логов на внешний сервер настроена.",
    checkedAt: "30.09.2021 15:50",
  },
];

const mockEvents: EventLog[] = [
  {
    id: "event-1",
    timestamp: "30.09.2021 15:56",
    deviceName: "Windows localhost",
    eventType: "config_change",
    severity: "high",
    message: "Зафиксировано изменение конфигурации.",
    accepted: false,
  },
  {
    id: "event-2",
    timestamp: "16.09.2021 14:59",
    deviceName: "Cisco 10.72.14.190",
    eventType: "security_check",
    severity: "critical",
    message: "Нарушено правило безопасности Cisco IOS show running.",
    accepted: true,
  },
  {
    id: "event-3",
    timestamp: "16.09.2021 14:40",
    deviceName: "Smart R80",
    eventType: "auth_error",
    severity: "medium",
    message: "Ошибка аутентификации при сборе конфигурации.",
    accepted: false,
  },
];

const tabs: Array<{ id: DashboardTab; label: string }> = [
  {
    id: "overview",
    label: "Обзор",
  },
  {
    id: "devices",
    label: "Устройства",
  },
  {
    id: "security",
    label: "Проверки безопасности",
  },
  {
    id: "events",
    label: "События",
  },
];

const statusLabels: Record<DeviceStatus, string> = {
  available: "Доступен",
  offline: "Нет связи",
  auth_error: "Ошибка авторизации",
  warning: "Предупреждение",
  critical: "Критично",
  service_mode: "Сервисный режим",
};

const statusStyles: Record<DeviceStatus, string> = {
  available: "bg-emerald-50 text-emerald-700 ring-emerald-200",
  offline: "bg-slate-100 text-slate-700 ring-slate-200",
  auth_error: "bg-orange-50 text-orange-700 ring-orange-200",
  warning: "bg-yellow-50 text-yellow-700 ring-yellow-200",
  critical: "bg-red-50 text-red-700 ring-red-200",
  service_mode: "bg-blue-50 text-blue-700 ring-blue-200",
};

const severityLabels: Record<Severity, string> = {
  critical: "Критическая",
  high: "Высокая",
  medium: "Средняя",
  low: "Низкая",
  none: "Нет",
};

const severityStyles: Record<Severity, string> = {
  critical: "bg-red-600 text-white",
  high: "bg-red-100 text-red-700",
  medium: "bg-yellow-100 text-yellow-800",
  low: "bg-sky-100 text-sky-700",
  none: "bg-emerald-100 text-emerald-700",
};

const cardColorStyles: Record<MetricCard["color"], string> = {
  blue: "border-blue-100 bg-blue-50",
  green: "border-emerald-100 bg-emerald-50",
  red: "border-red-100 bg-red-50",
  yellow: "border-yellow-100 bg-yellow-50",
  purple: "border-purple-100 bg-purple-50",
  gray: "border-slate-100 bg-slate-50",
};

function getScoreBarColor(score: number): string {
  if (score < 60) {
    return "bg-red-500";
  }

  if (score < 75) {
    return "bg-yellow-400";
  }

  return "bg-emerald-500";
}

function getSecurityRuleStatusLabel(status: SecurityRule["status"]): string {
  const labels: Record<SecurityRule["status"], string> = {
    passed: "Пройдено",
    failed: "Ошибка",
    warning: "Предупреждение",
    not_checked: "Не проверено",
  };

  return labels[status];
}

function getSecurityRuleStatusStyle(status: SecurityRule["status"]): string {
  const styles: Record<SecurityRule["status"], string> = {
    passed: "bg-emerald-100 text-emerald-700",
    failed: "bg-red-100 text-red-700",
    warning: "bg-yellow-100 text-yellow-800",
    not_checked: "bg-slate-100 text-slate-700",
  };

  return styles[status];
}

export function Dashboard() {
  const [activeTab, setActiveTab] = useState<DashboardTab>("overview");
  const [selectedDeviceIds, setSelectedDeviceIds] = useState<Set<string>>(
    () => new Set()
  );
  const [acceptedEventIds, setAcceptedEventIds] = useState<Set<string>>(
    () => new Set(mockEvents.filter((event) => event.accepted).map((event) => event.id))
  );
  const [isFilterOpen, setIsFilterOpen] = useState(false);

  const isAllSelected =
    mockDevices.length > 0 && selectedDeviceIds.size === mockDevices.length;

  const selectedDevicesCount = selectedDeviceIds.size;

  const vulnerableDevicesCount = useMemo(
    () =>
      mockDevices.filter(
        (device) =>
          device.vulnerabilityLevel === "critical" ||
          device.vulnerabilityLevel === "high"
      ).length,
    []
  );

  const handleToggleDevice = (deviceId: string) => {
    setSelectedDeviceIds((currentIds) => {
      const nextIds = new Set(currentIds);

      if (nextIds.has(deviceId)) {
        nextIds.delete(deviceId);
      } else {
        nextIds.add(deviceId);
      }

      return nextIds;
    });
  };

  const handleToggleAllDevices = () => {
    setSelectedDeviceIds(() => {
      if (isAllSelected) {
        return new Set();
      }

      return new Set(mockDevices.map((device) => device.id));
    });
  };

  const handleToggleEventAccepted = (eventId: string) => {
    setAcceptedEventIds((currentIds) => {
      const nextIds = new Set(currentIds);

      if (nextIds.has(eventId)) {
        nextIds.delete(eventId);
      } else {
        nextIds.add(eventId);
      }

      return nextIds;
    });
  };

  return (
    <main className="min-h-screen bg-slate-100 p-6">
      <div className="mx-auto max-w-7xl space-y-6">
        <section className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
          {metricCards.map((card) => (
            <article
              key={card.id}
              className={[
                "rounded-2xl border p-5 shadow-sm",
                cardColorStyles[card.color],
              ].join(" ")}
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-sm font-medium text-slate-600">{card.title}</p>
                  <p className="mt-3 text-3xl font-bold text-slate-950">
                    {card.value}
                  </p>
                  <p className="mt-1 text-sm text-slate-500">{card.description}</p>
                </div>

                <div className="rounded-xl bg-white/80 p-2 shadow-sm">
                  {card.color === "red" && (
                    <ShieldAlert className="h-5 w-5 text-red-500" />
                  )}
                  {card.color === "green" && (
                    <ShieldCheck className="h-5 w-5 text-emerald-500" />
                  )}
                  {card.color === "yellow" && (
                    <AlertTriangle className="h-5 w-5 text-yellow-500" />
                  )}
                  {card.color === "blue" && (
                    <TrendingUp className="h-5 w-5 text-blue-500" />
                  )}
                </div>
              </div>

              {typeof card.trend === "number" && (
                <div className="mt-5">
                  <div className="flex justify-between text-xs text-slate-500">
                    <span>Прогресс</span>
                    <span>{card.trend}%</span>
                  </div>

                  <div className="mt-2 h-2 overflow-hidden rounded-full bg-white">
                    <div
                      className="h-full rounded-full bg-slate-800"
                      style={{ width: `${card.trend}%` }}
                    />
                  </div>
                </div>
              )}
            </article>
          ))}
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white shadow-sm">
          <div className="flex flex-col gap-4 border-b border-slate-200 p-5 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <h2 className="text-lg font-semibold text-slate-950">
                Мониторинг инфраструктуры
              </h2>
              <p className="mt-1 text-sm text-slate-500">
                Контроль конфигураций, проверок безопасности и состояния устройств.
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <button
                type="button"
                className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
              >
                <RefreshCw className="h-4 w-4" />
                Обновить
              </button>

              <button
                type="button"
                className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
              >
                <Download className="h-4 w-4" />
                Экспорт
              </button>

              <div className="relative">
                <button
                  type="button"
                  onClick={() => setIsFilterOpen((value) => !value)}
                  className="inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800"
                >
                  <Filter className="h-4 w-4" />
                  Фильтр
                  <ChevronDown className="h-4 w-4" />
                </button>

                {isFilterOpen && (
                  <div className="absolute right-0 top-12 z-20 w-72 rounded-2xl border border-slate-200 bg-white p-4 shadow-xl">
                    <p className="text-sm font-semibold text-slate-900">
                      Быстрые фильтры
                    </p>

                    <div className="mt-3 space-y-2">
                      {["Критичные", "С изменениями", "Нет связи", "Ошибки авторизации"].map(
                        (filterName) => (
                          <label
                            key={filterName}
                            className="flex items-center gap-2 text-sm text-slate-600"
                          >
                            <input
                              type="checkbox"
                              className="h-4 w-4 rounded border-slate-300 text-sky-600 focus:ring-sky-500"
                            />
                            {filterName}
                          </label>
                        )
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="border-b border-slate-200 px-5">
            <div className="flex gap-2 overflow-x-auto">
              {tabs.map((tab) => {
                const isActive = activeTab === tab.id;

                return (
                  <button
                    key={tab.id}
                    type="button"
                    onClick={() => setActiveTab(tab.id)}
                    className={[
                      "border-b-2 px-4 py-3 text-sm font-medium transition",
                      isActive
                        ? "border-sky-500 text-sky-600"
                        : "border-transparent text-slate-500 hover:text-slate-900",
                    ].join(" ")}
                  >
                    {tab.label}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="p-5">
            {activeTab === "overview" && (
              <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
                <div className="rounded-2xl border border-slate-200 p-5">
                  <div className="mb-5 flex items-center justify-between">
                    <div>
                      <h3 className="font-semibold text-slate-950">
                        Самые уязвимые устройства
                      </h3>
                      <p className="text-sm text-slate-500">
                        {vulnerableDevicesCount} устройств требуют приоритетной проверки.
                      </p>
                    </div>

                    <MoreHorizontal className="h-5 w-5 text-slate-400" />
                  </div>

                  <div className="space-y-4">
                    {mockDevices.slice(0, 5).map((device) => (
                      <div key={device.id} className="space-y-2">
                        <div className="flex items-center justify-between gap-3">
                          <div>
                            <p className="text-sm font-medium text-slate-800">
                              {device.name}
                            </p>
                            <p className="text-xs text-slate-500">
                              {device.type} · {device.ipAddress}
                            </p>
                          </div>

                          <span
                            className={[
                              "rounded-full px-2.5 py-1 text-xs font-medium",
                              severityStyles[device.vulnerabilityLevel],
                            ].join(" ")}
                          >
                            {severityLabels[device.vulnerabilityLevel]}
                          </span>
                        </div>

                        <div className="h-2 overflow-hidden rounded-full bg-slate-100">
                          <div
                            className={["h-full rounded-full", getScoreBarColor(device.securityScore)].join(
                              " "
                            )}
                            style={{ width: `${device.securityScore}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="rounded-2xl border border-slate-200 p-5">
                  <div className="mb-5 flex items-center justify-between">
                    <div>
                      <h3 className="font-semibold text-slate-950">
                        Состояние устройств
                      </h3>
                      <p className="text-sm text-slate-500">
                        Доступность и ошибки подключения.
                      </p>
                    </div>

                    <SlidersHorizontal className="h-5 w-5 text-slate-400" />
                  </div>

                  <div className="space-y-4">
                    {mockDevices.map((device) => (
                      <div
                        key={device.id}
                        className="flex items-center justify-between rounded-xl border border-slate-100 p-3"
                      >
                        <div>
                          <p className="text-sm font-medium text-slate-800">
                            {device.name}
                          </p>
                          <p className="text-xs text-slate-500">
                            {device.vendor} · {device.type}
                          </p>
                        </div>

                        <span
                          className={[
                            "rounded-full px-2.5 py-1 text-xs font-medium ring-1",
                            statusStyles[device.status],
                          ].join(" ")}
                        >
                          {statusLabels[device.status]}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activeTab === "devices" && (
              <div className="overflow-hidden rounded-2xl border border-slate-200">
                <div className="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-4 py-3">
                  <p className="text-sm font-medium text-slate-700">
                    Выбрано устройств: {selectedDevicesCount}
                  </p>

                  <button
                    type="button"
                    className="rounded-lg bg-slate-900 px-3 py-1.5 text-xs font-medium text-white hover:bg-slate-800"
                  >
                    Запустить проверку
                  </button>
                </div>

                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-slate-200">
                    <thead className="bg-slate-50">
                      <tr>
                        <th className="w-12 px-4 py-3 text-left">
                          <input
                            type="checkbox"
                            checked={isAllSelected}
                            onChange={handleToggleAllDevices}
                            className="h-4 w-4 rounded border-slate-300 text-sky-600 focus:ring-sky-500"
                          />
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                          Устройство
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                          Тип
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                          Статус
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                          Защищённость
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                          Уязвимости
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                          Последняя проверка
                        </th>
                      </tr>
                    </thead>

                    <tbody className="divide-y divide-slate-100 bg-white">
                      {mockDevices.map((device) => {
                        const isSelected = selectedDeviceIds.has(device.id);

                        return (
                          <tr
                            key={device.id}
                            className={isSelected ? "bg-sky-50/60" : "hover:bg-slate-50"}
                          >
                            <td className="px-4 py-4">
                              <input
                                type="checkbox"
                                checked={isSelected}
                                onChange={() => handleToggleDevice(device.id)}
                                className="h-4 w-4 rounded border-slate-300 text-sky-600 focus:ring-sky-500"
                              />
                            </td>

                            <td className="px-4 py-4">
                              <div>
                                <p className="text-sm font-medium text-slate-900">
                                  {device.name}
                                </p>
                                <p className="text-xs text-slate-500">
                                  {device.ipAddress}
                                </p>
                              </div>
                            </td>

                            <td className="px-4 py-4 text-sm text-slate-600">
                              {device.type}
                            </td>

                            <td className="px-4 py-4">
                              <span
                                className={[
                                  "rounded-full px-2.5 py-1 text-xs font-medium ring-1",
                                  statusStyles[device.status],
                                ].join(" ")}
                              >
                                {statusLabels[device.status]}
                              </span>
                            </td>

                            <td className="px-4 py-4">
                              <div className="flex items-center gap-3">
                                <div className="h-2 w-24 overflow-hidden rounded-full bg-slate-100">
                                  <div
                                    className={[
                                      "h-full rounded-full",
                                      getScoreBarColor(device.securityScore),
                                    ].join(" ")}
                                    style={{ width: `${device.securityScore}%` }}
                                  />
                                </div>
                                <span className="text-sm font-medium text-slate-700">
                                  {device.securityScore}%
                                </span>
                              </div>
                            </td>

                            <td className="px-4 py-4">
                              <div className="flex items-center gap-2 text-xs">
                                <span className="text-red-600">
                                  {device.criticalVulnerabilities}
                                </span>
                                <span className="text-red-400">
                                  {device.highVulnerabilities}
                                </span>
                                <span className="text-yellow-500">
                                  {device.mediumVulnerabilities}
                                </span>
                                <span className="text-sky-500">
                                  {device.lowVulnerabilities}
                                </span>
                              </div>
                            </td>

                            <td className="px-4 py-4 text-sm text-slate-500">
                              {device.lastScanAt}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {activeTab === "security" && (
              <div className="grid grid-cols-1 gap-4">
                {mockSecurityRules.map((rule) => (
                  <article
                    key={rule.id}
                    className="rounded-2xl border border-slate-200 p-5 transition hover:border-slate-300 hover:shadow-sm"
                  >
                    <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                      <div>
                        <div className="flex flex-wrap items-center gap-2">
                          <h3 className="font-semibold text-slate-950">{rule.name}</h3>

                          <span
                            className={[
                              "rounded-full px-2.5 py-1 text-xs font-medium",
                              getSecurityRuleStatusStyle(rule.status),
                            ].join(" ")}
                          >
                            {getSecurityRuleStatusLabel(rule.status)}
                          </span>

                          <span
                            className={[
                              "rounded-full px-2.5 py-1 text-xs font-medium",
                              severityStyles[rule.severity],
                            ].join(" ")}
                          >
                            {severityLabels[rule.severity]}
                          </span>
                        </div>

                        <p className="mt-2 text-sm text-slate-600">
                          {rule.description}
                        </p>

                        <p className="mt-2 text-xs text-slate-500">
                          Устройство: {rule.deviceName} · Проверено: {rule.checkedAt}
                        </p>
                      </div>

                      {rule.status === "passed" ? (
                        <CheckCircle2 className="h-6 w-6 text-emerald-500" />
                      ) : (
                        <AlertTriangle className="h-6 w-6 text-red-500" />
                      )}
                    </div>
                  </article>
                ))}
              </div>
            )}

            {activeTab === "events" && (
              <div className="space-y-3">
                {mockEvents.map((event) => {
                  const isAccepted = acceptedEventIds.has(event.id);

                  return (
                    <article
                      key={event.id}
                      className={[
                        "rounded-2xl border p-5 transition",
                        isAccepted
                          ? "border-emerald-200 bg-emerald-50/40"
                          : "border-slate-200 bg-white",
                      ].join(" ")}
                    >
                      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                        <div>
                          <div className="flex flex-wrap items-center gap-2">
                            <span
                              className={[
                                "rounded-full px-2.5 py-1 text-xs font-medium",
                                severityStyles[event.severity],
                              ].join(" ")}
                            >
                              {severityLabels[event.severity]}
                            </span>

                            <span className="text-xs text-slate-500">
                              {event.timestamp}
                            </span>
                          </div>

                          <p className="mt-2 text-sm font-medium text-slate-900">
                            {event.deviceName}
                          </p>

                          <p className="mt-1 text-sm text-slate-600">
                            {event.message}
                          </p>
                        </div>

                        <label className="flex items-center gap-2 text-sm text-slate-600">
                          <input
                            type="checkbox"
                            checked={isAccepted}
                            onChange={() => handleToggleEventAccepted(event.id)}
                            className="h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500"
                          />
                          Принято
                        </label>
                      </div>
                    </article>
                  );
                })}
              </div>
            )}
          </div>
        </section>
      </div>
    </main>
  );
}