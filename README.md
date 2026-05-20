# Config Inspector Frontend — подробный README

Этот документ описывает frontend-проект для интерфейса корпоративной ИБ-системы класса **Config Inspector**.

Проект предназначен для хакатона/демонстрации и показывает визуальный каркас системы мониторинга устройств, контроля конфигураций, проверок безопасности, событий, уязвимостей и состояния инфраструктуры.

---

# 0. Самое важное по текущей структуре

По текущему виду проекта у тебя структура примерно такая:

```text
XAKATON/
├── scr/
│   ├── components/
│   │   ├── Dashboard.tsx
│   │   ├── Header.tsx
│   │   └── Sidebar.tsx
│   ├── types/
│   │   └── index.ts
│   └── App.tsx
├── LICENSE
└── README.md
```

## Критическая ошибка

Папка называется:

```text
scr
```

А должна называться:

```text
src
```

Для Vite/React стандартная папка исходников — `src`.

Нужно переименовать:

```text
scr -> src
```

Итоговая правильная структура должна быть такой:

```text
XAKATON/
├── src/
│   ├── components/
│   │   ├── Dashboard.tsx
│   │   ├── Header.tsx
│   │   └── Sidebar.tsx
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── README.md
└── LICENSE
```

Если `src/main.tsx`, `src/index.css`, `package.json`, `index.html` или `vite.config.ts` отсутствуют — проект не запустится.

---

# 1. Что это за проект

Это frontend-интерфейс системы мониторинга и контроля ИТ-инфраструктуры.

Смысл интерфейса:

- показывать состояние устройств;
- показывать изменения конфигураций;
- показывать уязвимые устройства;
- показывать проверки безопасности;
- отображать события и уведомления;
- давать оператору удобную панель мониторинга;
- подготовить основу для будущей интеграции с backend API.

Сейчас это **визуальный каркас без реального backend**.

Все данные пока находятся внутри frontend-файлов как mock-данные.

---

# 2. Что такое mock-данные

Mock-данные — это временные тестовые данные, которые лежат прямо в коде.

Они нужны, чтобы интерфейс работал без backend.

Пример mock-устройства:

```ts
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
];
```

Потом, когда backend будет готов, эти mock-данные нужно заменить на реальные запросы:

```text
GET /api/devices
GET /api/events
GET /api/dashboard/metrics
GET /api/security/rules/results
GET /api/system/status
```

---

# 3. Технологии

Проект использует:

```text
React 18+
TypeScript
Vite
Tailwind CSS
Lucide React
```

## React

Используется для создания компонентов интерфейса.

## TypeScript

Используется для строгого описания данных.

Например, устройство должно иметь поля:

```text
id
name
ipAddress
type
vendor
status
securityScore
vulnerabilityLevel
lastScanAt
```

## Vite

Используется для запуска и сборки frontend-проекта.

Команды:

```bash
npm run dev
npm run build
npm run preview
```

## Tailwind CSS

Используется для стилей через классы:

```tsx
<div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
```

## Lucide React

Используется для иконок:

```tsx
import { Bell, Search, Settings } from "lucide-react";
```

---

# 4. Что уже реализовано

```text
[+] Боковое меню Sidebar
[+] Верхняя панель Header
[+] Главный Dashboard
[+] Карточки метрик
[+] Вкладки Dashboard
[+] Таблица устройств
[+] Checkbox выбора одного устройства
[+] Checkbox выбора всех устройств
[+] События с checkbox "Принято"
[+] Цветные статусы устройств
[+] Цветные уровни критичности
[+] Прогресс-бары защищённости
[+] Mock-данные
[+] TypeScript-типы
[+] Подготовка к подключению API
```

---

# 5. Что пока не реализовано

```text
[-] Реальный backend
[-] Реальные API-запросы
[-] Реальная база данных
[-] Авторизация пользователей
[-] Реальный сбор конфигураций
[-] Реальное сравнение конфигураций
[-] Реальная проверка уязвимостей
[-] Реальная генерация PDF-отчётов
[-] Реальные WebSocket-уведомления
[-] Реальная интеграция с сетевыми устройствами
```

Это нормально для текущего этапа. Сейчас цель — запустить и показать frontend-каркас.

---

# 6. Полная структура проекта

Правильная структура:

```text
XAKATON/
├── src/
│   ├── components/
│   │   ├── Dashboard.tsx
│   │   ├── Header.tsx
│   │   └── Sidebar.tsx
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── README.md
└── LICENSE
```

---

# 7. Описание каждого файла

## 7.1. `src/types/index.ts`

Файл с TypeScript-типами.

Он описывает структуру данных, которые используются в интерфейсе.

В нём находятся:

```text
DeviceStatus
Severity
DeviceType
SecurityCheckStatus
MetricCard
Device
SecurityRule
EventLog
DashboardSummary
```

Этот файл критически важен, потому что именно он задаёт контракт данных между frontend и будущим backend.

Если backend будет отдавать другие поля — нужно либо изменить этот файл, либо написать mapper-функции.

---

## 7.2. `src/components/Sidebar.tsx`

Файл отвечает за левое меню.

Содержит:

- логотип/название системы;
- пункты навигации;
- иконки;
- активный пункт меню;
- кнопку сворачивания меню;
- блок состояния Core online.

Использует `useState`:

```ts
const [isCollapsed, setIsCollapsed] = useState(false);
```

Это состояние отвечает за сворачивание и разворачивание бокового меню.

---

## 7.3. `src/components/Header.tsx`

Файл отвечает за верхнюю панель.

Содержит:

- заголовок текущей страницы;
- подзаголовок;
- поиск;
- статус системы;
- уведомления;
- профиль пользователя;
- выпадающее меню профиля.

Использует состояния:

```ts
const [searchQuery, setSearchQuery] = useState("");
const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
```

Что они делают:

```text
searchQuery              — текст в поиске
isProfileMenuOpen        — открыто ли меню профиля
isNotificationsOpen      — открыта ли панель уведомлений
```

---

## 7.4. `src/components/Dashboard.tsx`

Главный файл интерфейса.

Содержит:

- карточки метрик;
- mock-устройства;
- mock-проверки безопасности;
- mock-события;
- вкладки;
- таблицу устройств;
- обработку checkbox;
- статусы;
- бейджи критичности;
- фильтры;
- overview-блоки.

Это самый большой и важный компонент проекта.

---

## 7.5. `src/App.tsx`

Корневой компонент.

Он собирает всё приложение:

```text
Sidebar + Header + Dashboard
```

Также отвечает за переключение разделов:

```ts
const [activeNavigationItem, setActiveNavigationItem] =
  useState<NavigationKey>("monitoring");
```

Если выбран раздел `monitoring`, отображается `Dashboard`.

Если выбран другой раздел, отображается временная заглушка.

---

## 7.6. `src/main.tsx`

Точка входа React-приложения.

Именно этот файл подключает `App` к HTML-элементу `root`.

Пример:

```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

---

## 7.7. `src/index.css`

Файл глобальных стилей.

Для Tailwind CSS должен содержать:

```css
@import "tailwindcss";
```

---

## 7.8. `index.html`

HTML-точка входа.

Должна быть в корне проекта.

Пример:

```html
<!doctype html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Config Inspector Frontend</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

Самая важная строка:

```html
<script type="module" src="/src/main.tsx"></script>
```

Она говорит Vite, откуда запускать React.

---

## 7.9. `package.json`

Файл зависимостей и команд запуска.

Минимальный пример:

```json
{
  "name": "config-inspector-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@vitejs/plugin-react": "latest",
    "lucide-react": "latest",
    "react": "latest",
    "react-dom": "latest"
  },
  "devDependencies": {
    "typescript": "latest",
    "vite": "latest",
    "tailwindcss": "latest",
    "@tailwindcss/vite": "latest"
  }
}
```

---

## 7.10. `vite.config.ts`

Конфиг Vite.

Пример:

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

---

## 7.11. `tsconfig.json`

Конфигурация TypeScript.

Обычно создаётся автоматически при создании проекта через Vite.

Если файла нет, лучше создать проект заново через:

```bash
npm create vite@latest config-inspector-frontend -- --template react-ts
```

---

# 8. Подробно про `src/types/index.ts`

## 8.1. `DeviceStatus`

```ts
export type DeviceStatus =
  | "available"
  | "offline"
  | "auth_error"
  | "warning"
  | "critical"
  | "service_mode";
```

Значения:

```text
available      — устройство доступно
offline        — устройство недоступно
auth_error     — ошибка авторизации
warning        — предупреждение
critical       — критическое состояние
service_mode   — сервисный режим
```

---

## 8.2. `Severity`

```ts
export type Severity = "critical" | "high" | "medium" | "low" | "none";
```

Значения:

```text
critical — критическая проблема
high     — высокая важность
medium   — средняя важность
low      — низкая важность
none     — проблем нет
```

---

## 8.3. `DeviceType`

```ts
export type DeviceType =
  | "Windows"
  | "Linux"
  | "Cisco IOS"
  | "Cisco ASA"
  | "Fortinet"
  | "JunOS"
  | "VM"
  | "Check Point"
  | "Huawei VRP"
  | "Unknown";
```

Типы устройств, которые frontend умеет отображать.

---

## 8.4. `SecurityCheckStatus`

```ts
export type SecurityCheckStatus =
  | "passed"
  | "failed"
  | "warning"
  | "not_checked";
```

Значения:

```text
passed      — проверка пройдена
failed      — проверка провалена
warning     — есть предупреждение
not_checked — проверка ещё не выполнялась
```

---

## 8.5. `MetricCard`

```ts
export interface MetricCard {
  id: string;
  title: string;
  value: number | string;
  description: string;
  trend?: number;
  color: "blue" | "green" | "red" | "yellow" | "purple" | "gray";
}
```

Отвечает за карточки сверху на Dashboard.

Поля:

```text
id           — уникальный ID карточки
title        — заголовок карточки
value        — основное значение
description  — описание
trend        — процент прогресса
color        — цветовая тема карточки
```

---

## 8.6. `Device`

```ts
export interface Device {
  id: string;
  name: string;
  ipAddress: string;
  type: DeviceType;
  vendor: string;
  status: DeviceStatus;
  securityScore: number;
  vulnerabilityLevel: Severity;
  criticalVulnerabilities: number;
  highVulnerabilities: number;
  mediumVulnerabilities: number;
  lowVulnerabilities: number;
  lastScanAt: string;
  configChanged: boolean;
  selected?: boolean;
}
```

Главный интерфейс устройства.

Поля:

```text
id                         — уникальный ID устройства
name                       — название
ipAddress                  — IP-адрес
type                       — тип устройства
vendor                     — производитель
status                     — текущий статус
securityScore              — процент защищённости
vulnerabilityLevel         — общий уровень уязвимости
criticalVulnerabilities    — критические уязвимости
highVulnerabilities        — уязвимости высокой важности
mediumVulnerabilities      — уязвимости средней важности
lowVulnerabilities         — уязвимости низкой важности
lastScanAt                 — последняя проверка
configChanged              — изменился ли конфиг
selected                   — выбрано ли устройство
```

---

## 8.7. `SecurityRule`

```ts
export interface SecurityRule {
  id: string;
  name: string;
  deviceName: string;
  status: SecurityCheckStatus;
  severity: Severity;
  description: string;
  checkedAt: string;
}
```

Интерфейс проверки безопасности.

Поля:

```text
id          — ID правила
name        — название проверки
deviceName  — устройство
status      — результат проверки
severity    — критичность
description — описание проблемы
checkedAt   — дата проверки
```

---

## 8.8. `EventLog`

```ts
export interface EventLog {
  id: string;
  timestamp: string;
  deviceName: string;
  eventType:
    | "config_change"
    | "security_check"
    | "auth_error"
    | "device_down"
    | "system";
  severity: Severity;
  message: string;
  accepted: boolean;
}
```

Интерфейс события.

Поля:

```text
id          — ID события
timestamp   — время события
deviceName  — устройство
eventType   — тип события
severity    — критичность
message     — текст события
accepted    — принято ли событие оператором
```

---

## 8.9. `DashboardSummary`

```ts
export interface DashboardSummary {
  changedReports: number;
  securityRulesCompleted: number;
  totalSecurityRules: number;
  criticalDevices: number;
  availableDevices: number;
  offlineDevices: number;
  authErrorDevices: number;
}
```

Сводная информация для Dashboard.

Пока этот интерфейс может не использоваться напрямую, но пригодится при подключении backend.

---

# 9. Подробно про `Sidebar.tsx`

## 9.1. Назначение

`Sidebar.tsx` отвечает за боковую панель навигации.

Она находится слева и содержит основные разделы системы.

---

## 9.2. Основные разделы

```text
Мониторинг
Устройства
Отчёты
События
Настройки
Потоки
```

---

## 9.3. Тип `NavigationKey`

```ts
type NavigationKey =
  | "monitoring"
  | "devices"
  | "reports"
  | "events"
  | "settings"
  | "flows";
```

Это технические ID разделов.

---

## 9.4. Интерфейс `NavigationItem`

```ts
interface NavigationItem {
  id: NavigationKey;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
}
```

Поля:

```text
id    — технический ID раздела
label — текст на русском
icon  — иконка из lucide-react
```

---

## 9.5. Массив `navigationItems`

```ts
const navigationItems: NavigationItem[] = [
  {
    id: "monitoring",
    label: "Мониторинг",
    icon: BarChart3,
  },
  ...
];
```

Если нужно добавить новый раздел, добавлять его нужно сюда.

---

## 9.6. Props компонента

```ts
interface SidebarProps {
  activeItem: NavigationKey;
  onNavigate: (item: NavigationKey) => void;
}
```

Поля:

```text
activeItem — активный пункт меню
onNavigate — функция переключения раздела
```

---

## 9.7. Состояние `isCollapsed`

```ts
const [isCollapsed, setIsCollapsed] = useState(false);
```

Отвечает за то, свернуто меню или раскрыто.

---

## 9.8. Что можно менять в Sidebar

Можно менять:

```text
название системы
подпись Security Console
список разделов
иконки
цвета меню
блок Core online
```

---

# 10. Подробно про `Header.tsx`

## 10.1. Назначение

`Header.tsx` отвечает за верхнюю панель.

---

## 10.2. Что отображает Header

```text
заголовок страницы
подзаголовок страницы
поиск
статус системы
уведомления
профиль пользователя
```

---

## 10.3. Props компонента

```ts
interface HeaderProps {
  title: string;
  subtitle?: string;
}
```

Поля:

```text
title    — заголовок
subtitle — подзаголовок
```

---

## 10.4. Mock-статус системы

```ts
const systemStatus = {
  label: "Система работает",
  description: "Все основные службы доступны",
};
```

Позже заменить на запрос:

```text
GET /api/system/status
```

---

## 10.5. Состояния Header

```ts
const [searchQuery, setSearchQuery] = useState("");
const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
```

Что делают:

```text
searchQuery            — текст поиска
isProfileMenuOpen      — меню профиля открыто/закрыто
isNotificationsOpen    — уведомления открыты/закрыты
```

---

## 10.6. Что можно менять в Header

Можно менять:

```text
статус системы
уведомления
имя пользователя
поиск
кнопки
тексты
цвета
```

---

# 11. Подробно про `Dashboard.tsx`

## 11.1. Назначение

`Dashboard.tsx` — главный экран интерфейса.

Он показывает:

```text
карточки метрик
обзор инфраструктуры
уязвимые устройства
состояние устройств
таблицу устройств
проверки безопасности
события
```

---

## 11.2. Тип вкладок Dashboard

```ts
type DashboardTab = "overview" | "devices" | "security" | "events";
```

Вкладки:

```text
overview — Обзор
devices  — Устройства
security — Проверки безопасности
events   — События
```

---

## 11.3. `metricCards`

Mock-данные карточек метрик.

```ts
const metricCards: MetricCard[] = [
  {
    id: "changes",
    title: "Контроль изменений",
    value: 16,
    description: "отчётов с нарушениями",
    trend: 76,
    color: "red",
  },
  ...
];
```

Используется в верхних карточках Dashboard.

Заменить на backend:

```text
GET /api/dashboard/metrics
```

---

## 11.4. `mockDevices`

Mock-данные устройств.

```ts
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
];
```

Используется:

```text
в таблице устройств
в блоке самых уязвимых устройств
в блоке состояния устройств
для подсчёта выбранных устройств
```

Заменить на backend:

```text
GET /api/devices
```

---

## 11.5. `mockSecurityRules`

Mock-данные проверок безопасности.

```ts
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
];
```

Заменить на backend:

```text
GET /api/security/rules/results
```

---

## 11.6. `mockEvents`

Mock-данные событий.

```ts
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
];
```

Заменить на backend:

```text
GET /api/events
```

---

## 11.7. `tabs`

Список вкладок:

```ts
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
```

---

# 12. Справочники стилей в Dashboard

## 12.1. `statusLabels`

Переводит технический статус устройства в русский текст.

```ts
const statusLabels: Record<DeviceStatus, string> = {
  available: "Доступен",
  offline: "Нет связи",
  auth_error: "Ошибка авторизации",
  warning: "Предупреждение",
  critical: "Критично",
  service_mode: "Сервисный режим",
};
```

---

## 12.2. `statusStyles`

Задаёт цвет бейджа статуса устройства.

```ts
const statusStyles: Record<DeviceStatus, string> = {
  available: "bg-emerald-50 text-emerald-700 ring-emerald-200",
  offline: "bg-slate-100 text-slate-700 ring-slate-200",
  auth_error: "bg-orange-50 text-orange-700 ring-orange-200",
  warning: "bg-yellow-50 text-yellow-700 ring-yellow-200",
  critical: "bg-red-50 text-red-700 ring-red-200",
  service_mode: "bg-blue-50 text-blue-700 ring-blue-200",
};
```

Если нужно поменять цвета статусов — менять здесь.

---

## 12.3. `severityLabels`

Переводит уровень критичности в русский текст.

```ts
const severityLabels: Record<Severity, string> = {
  critical: "Критическая",
  high: "Высокая",
  medium: "Средняя",
  low: "Низкая",
  none: "Нет",
};
```

---

## 12.4. `severityStyles`

Цвета уровней критичности.

```ts
const severityStyles: Record<Severity, string> = {
  critical: "bg-red-600 text-white",
  high: "bg-red-100 text-red-700",
  medium: "bg-yellow-100 text-yellow-800",
  low: "bg-sky-100 text-sky-700",
  none: "bg-emerald-100 text-emerald-700",
};
```

---

## 12.5. `cardColorStyles`

Цвета карточек метрик.

```ts
const cardColorStyles: Record<MetricCard["color"], string> = {
  blue: "border-blue-100 bg-blue-50",
  green: "border-emerald-100 bg-emerald-50",
  red: "border-red-100 bg-red-50",
  yellow: "border-yellow-100 bg-yellow-50",
  purple: "border-purple-100 bg-purple-50",
  gray: "border-slate-100 bg-slate-50",
};
```

---

# 13. Функции в Dashboard

## 13.1. `getScoreBarColor`

```ts
function getScoreBarColor(score: number): string {
  if (score < 60) {
    return "bg-red-500";
  }

  if (score < 75) {
    return "bg-yellow-400";
  }

  return "bg-emerald-500";
}
```

Назначение:

выбирает цвет прогресс-бара защищённости.

Логика:

```text
score < 60        — красный
60 <= score < 75  — жёлтый
score >= 75       — зелёный
```

---

## 13.2. `getSecurityRuleStatusLabel`

```ts
function getSecurityRuleStatusLabel(status: SecurityRule["status"]): string
```

Назначение:

переводит технический статус проверки в русский текст.

Пример:

```text
passed      -> Пройдено
failed      -> Ошибка
warning     -> Предупреждение
not_checked -> Не проверено
```

---

## 13.3. `getSecurityRuleStatusStyle`

```ts
function getSecurityRuleStatusStyle(status: SecurityRule["status"]): string
```

Назначение:

выбирает цвет для результата проверки безопасности.

Пример:

```text
passed      -> зелёный
failed      -> красный
warning     -> жёлтый
not_checked -> серый
```

---

# 14. Состояния в Dashboard

## 14.1. `activeTab`

```ts
const [activeTab, setActiveTab] = useState<DashboardTab>("overview");
```

Отвечает за активную вкладку.

---

## 14.2. `selectedDeviceIds`

```ts
const [selectedDeviceIds, setSelectedDeviceIds] = useState<Set<string>>(
  () => new Set()
);
```

Хранит ID выбранных устройств.

Используется для checkbox в таблице.

---

## 14.3. `acceptedEventIds`

```ts
const [acceptedEventIds, setAcceptedEventIds] = useState<Set<string>>(
  () => new Set(mockEvents.filter((event) => event.accepted).map((event) => event.id))
);
```

Хранит ID принятых событий.

Используется во вкладке `События`.

---

## 14.4. `isFilterOpen`

```ts
const [isFilterOpen, setIsFilterOpen] = useState(false);
```

Отвечает за открытие и закрытие фильтра.

---

# 15. Вычисляемые значения в Dashboard

## 15.1. `isAllSelected`

```ts
const isAllSelected =
  mockDevices.length > 0 && selectedDeviceIds.size === mockDevices.length;
```

Проверяет, выбраны ли все устройства.

---

## 15.2. `selectedDevicesCount`

```ts
const selectedDevicesCount = selectedDeviceIds.size;
```

Количество выбранных устройств.

---

## 15.3. `vulnerableDevicesCount`

```ts
const vulnerableDevicesCount = useMemo(
  () =>
    mockDevices.filter(
      (device) =>
        device.vulnerabilityLevel === "critical" ||
        device.vulnerabilityLevel === "high"
    ).length,
  []
);
```

Считает количество устройств с критической или высокой уязвимостью.

---

# 16. Обработчики событий в Dashboard

## 16.1. `handleToggleDevice`

```ts
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
```

Назначение:

выбрать или снять выбор с одного устройства.

---

## 16.2. `handleToggleAllDevices`

```ts
const handleToggleAllDevices = () => {
  setSelectedDeviceIds(() => {
    if (isAllSelected) {
      return new Set();
    }

    return new Set(mockDevices.map((device) => device.id));
  });
};
```

Назначение:

выбрать все устройства или снять выбор со всех устройств.

---

## 16.3. `handleToggleEventAccepted`

```ts
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
```

Назначение:

переключить событие между состояниями:

```text
принято
не принято
```

---

# 17. Подробно про `App.tsx`

## 17.1. Назначение

`App.tsx` — главный компонент приложения.

Он отвечает за:

```text
общую структуру страницы
Sidebar
Header
Dashboard
переключение разделов меню
```

---

## 17.2. `NavigationKey`

```ts
type NavigationKey =
  | "monitoring"
  | "devices"
  | "reports"
  | "events"
  | "settings"
  | "flows";
```

Тип разделов приложения.

---

## 17.3. `pageTitles`

```ts
const pageTitles: Record<NavigationKey, string> = {
  monitoring: "Мониторинг",
  devices: "Устройства",
  reports: "Отчёты",
  events: "События",
  settings: "Настройки",
  flows: "Потоки",
};
```

Заголовки страниц.

---

## 17.4. `pageSubtitles`

```ts
const pageSubtitles: Record<NavigationKey, string> = {
  monitoring: "Сводная панель контроля конфигураций и безопасности",
  devices: "Инвентаризация и состояние контролируемых объектов",
  reports: "Формирование отчётов по изменениям и проверкам",
  events: "Журнал событий, уведомлений и инцидентов",
  settings: "Параметры системы, модулей и пользователей",
  flows: "Сетевые потоки и взаимодействия устройств",
};
```

Подзаголовки страниц.

---

## 17.5. `activeNavigationItem`

```ts
const [activeNavigationItem, setActiveNavigationItem] =
  useState<NavigationKey>("monitoring");
```

Хранит текущий выбранный раздел.

---

## 17.6. Логика отображения

```tsx
{activeNavigationItem === "monitoring" ? (
  <Dashboard />
) : (
  <main>...</main>
)}
```

Если выбран мониторинг — показывается Dashboard.

Если выбран другой раздел — показывается заглушка.

---

# 18. Минимальные файлы, если их нет

Если проект не был создан через Vite, добавь эти файлы.

---

## 18.1. `package.json`

```json
{
  "name": "config-inspector-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@vitejs/plugin-react": "latest",
    "lucide-react": "latest",
    "react": "latest",
    "react-dom": "latest"
  },
  "devDependencies": {
    "typescript": "latest",
    "vite": "latest",
    "tailwindcss": "latest",
    "@tailwindcss/vite": "latest"
  }
}
```

---

## 18.2. `vite.config.ts`

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

---

## 18.3. `index.html`

```html
<!doctype html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Config Inspector Frontend</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

---

## 18.4. `src/main.tsx`

```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

---

## 18.5. `src/index.css`

```css
@import "tailwindcss";
```

---

# 19. Как запустить проект в Visual Studio Code

## Шаг 1. Открыть VS Code

Открой Visual Studio Code.

---

## Шаг 2. Открыть папку проекта

В верхнем меню:

```text
File -> Open Folder
```

Выбери папку:

```text
XAKATON
```

Важно: открывать нужно **корень проекта**, а не папку `src`.

---

## Шаг 3. Проверить структуру

В левой панели должно быть примерно так:

```text
XAKATON/
├── src/
├── package.json
├── vite.config.ts
├── index.html
├── README.md
└── LICENSE
```

Если папка называется `scr`, переименуй её в `src`.

---

## Шаг 4. Открыть терминал

В VS Code:

```text
Terminal -> New Terminal
```

Или горячая клавиша:

```text
Ctrl + `
```

---

## Шаг 5. Проверить Node.js

В терминале:

```bash
node -v
```

Потом:

```bash
npm -v
```

Если версии показались — Node.js установлен.

Если команда не найдена — установи Node.js.

---

## Шаг 6. Установить зависимости

В терминале, находясь в корне проекта:

```bash
npm install
```

Эта команда установит:

```text
react
react-dom
vite
typescript
tailwindcss
lucide-react
```

---

## Шаг 7. Запустить проект

```bash
npm run dev
```

После запуска появится адрес:

```text
http://localhost:5173/
```

Открой его в браузере.

---

# 20. Как понять, что всё запустилось правильно

Ты должен увидеть:

```text
боковое меню слева
верхнюю панель
карточки метрик
Dashboard
вкладки
таблицу устройств
цветные бейджи
checkbox
уведомления
профиль root
```

---

# 21. Ручная проверка интерфейса

## 21.1. Sidebar

Проверь:

```text
[ ] меню отображается слева
[ ] активный пункт подсвечивается
[ ] кнопка сворачивания работает
[ ] пункты меню кликаются
[ ] заголовок страницы меняется
```

---

## 21.2. Header

Проверь:

```text
[ ] заголовок отображается
[ ] подзаголовок отображается
[ ] поиск принимает текст
[ ] при вводе появляется блок поиска
[ ] уведомления открываются
[ ] профиль открывается
```

---

## 21.3. Dashboard

Проверь:

```text
[ ] карточки метрик отображаются
[ ] вкладки переключаются
[ ] обзор отображается
[ ] таблица устройств отображается
[ ] checkbox устройства работает
[ ] checkbox "выбрать все" работает
[ ] счётчик выбранных устройств меняется
[ ] бейджи статусов отображаются
[ ] прогресс-бары отображаются
```

---

## 21.4. Вкладка "Проверки безопасности"

Проверь:

```text
[ ] правила отображаются
[ ] статусы правил отображаются
[ ] критичность отображается цветом
[ ] failed/passed/warning различаются
```

---

## 21.5. Вкладка "События"

Проверь:

```text
[ ] события отображаются
[ ] checkbox "Принято" работает
[ ] принятое событие меняет визуальный вид
```

---

# 22. Частые ошибки

## 22.1. Папка называется `scr`

Ошибка:

```text
Failed to resolve import "./App"
```

или приложение просто не запускается.

Решение:

```text
переименовать scr в src
```

---

## 22.2. Нет `package.json`

Ошибка:

```text
npm ERR! enoent Could not read package.json
```

Решение:

создать `package.json` в корне проекта.

---

## 22.3. Нет `main.tsx`

Ошибка:

```text
Failed to load url /src/main.tsx
```

Решение:

создать файл:

```text
src/main.tsx
```

---

## 22.4. Нет `index.html`

Ошибка:

Vite не находит точку входа.

Решение:

создать `index.html` в корне проекта.

---

## 22.5. Не работает Tailwind

Симптом:

страница без нормальных стилей.

Проверить:

```text
src/index.css
vite.config.ts
package.json
```

В `src/index.css` должно быть:

```css
@import "tailwindcss";
```

В `vite.config.ts` должен быть tailwind plugin:

```ts
import tailwindcss from "@tailwindcss/vite";
```

---

## 22.6. Ошибка `Cannot find module lucide-react`

Решение:

```bash
npm install lucide-react
```

---

## 22.7. Ошибка `Cannot find module react`

Решение:

```bash
npm install
```

---

## 22.8. Порт 5173 занят

Vite может запустить проект на другом порту:

```text
http://localhost:5174/
```

Смотри адрес в терминале.

---

# 23. Где менять mock-данные

## 23.1. Метрики

Файл:

```text
src/components/Dashboard.tsx
```

Искать:

```ts
const metricCards: MetricCard[] = [...]
```

---

## 23.2. Устройства

Файл:

```text
src/components/Dashboard.tsx
```

Искать:

```ts
const mockDevices: Device[] = [...]
```

---

## 23.3. Проверки безопасности

Файл:

```text
src/components/Dashboard.tsx
```

Искать:

```ts
const mockSecurityRules: SecurityRule[] = [...]
```

---

## 23.4. События

Файл:

```text
src/components/Dashboard.tsx
```

Искать:

```ts
const mockEvents: EventLog[] = [...]
```

---

## 23.5. Статус системы

Файл:

```text
src/components/Header.tsx
```

Искать:

```ts
const systemStatus = {
  label: "Система работает",
  description: "Все основные службы доступны",
};
```

---

# 24. Будущие backend endpoint-ы

Минимальный backend должен реализовать:

```text
GET /api/system/status
GET /api/dashboard/metrics
GET /api/devices
GET /api/security/rules/results
GET /api/events
```

---

# 25. API-контракт

## 25.1. `GET /api/system/status`

Ответ:

```json
{
  "label": "Система работает",
  "description": "Все основные службы доступны",
  "status": "ok"
}
```

---

## 25.2. `GET /api/dashboard/metrics`

Ответ:

```json
[
  {
    "id": "changes",
    "title": "Контроль изменений",
    "value": 16,
    "description": "отчётов с нарушениями",
    "trend": 76,
    "color": "red"
  },
  {
    "id": "security",
    "title": "Проверки безопасности",
    "value": "1274 / 2585",
    "description": "выполнено правил",
    "trend": 49,
    "color": "green"
  }
]
```

---

## 25.3. `GET /api/devices`

Ответ:

```json
[
  {
    "id": "dev-1",
    "name": "Windows localhost",
    "ipAddress": "127.0.0.1",
    "type": "Windows",
    "vendor": "Microsoft",
    "status": "available",
    "securityScore": 58,
    "vulnerabilityLevel": "high",
    "criticalVulnerabilities": 0,
    "highVulnerabilities": 20,
    "mediumVulnerabilities": 58,
    "lowVulnerabilities": 13,
    "lastScanAt": "30.09.2021 15:56",
    "configChanged": true
  }
]
```

---

## 25.4. `GET /api/security/rules/results`

Ответ:

```json
[
  {
    "id": "rule-1",
    "name": "Запрет Telnet",
    "deviceName": "Cisco 10.72.14.190",
    "status": "failed",
    "severity": "critical",
    "description": "Обнаружен небезопасный удалённый доступ через Telnet.",
    "checkedAt": "30.09.2021 15:56"
  }
]
```

---

## 25.5. `GET /api/events`

Ответ:

```json
[
  {
    "id": "event-1",
    "timestamp": "30.09.2021 15:56",
    "deviceName": "Windows localhost",
    "eventType": "config_change",
    "severity": "high",
    "message": "Зафиксировано изменение конфигурации.",
    "accepted": false
  }
]
```

---

# 26. Рекомендуемая структура API-слоя frontend

Когда появится backend, создать папку:

```text
src/api/
├── client.ts
├── dashboardApi.ts
├── devicesApi.ts
├── securityApi.ts
├── eventsApi.ts
└── systemApi.ts
```

---

## 26.1. `src/api/client.ts`

```ts
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export async function apiRequest<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}
```

---

## 26.2. `src/api/devicesApi.ts`

```ts
import type { Device } from "../types";
import { apiRequest } from "./client";

export function getDevices(): Promise<Device[]> {
  return apiRequest<Device[]>("/api/devices");
}
```

---

## 26.3. `src/api/dashboardApi.ts`

```ts
import type { MetricCard } from "../types";
import { apiRequest } from "./client";

export function getDashboardMetrics(): Promise<MetricCard[]> {
  return apiRequest<MetricCard[]>("/api/dashboard/metrics");
}
```

---

## 26.4. `src/api/securityApi.ts`

```ts
import type { SecurityRule } from "../types";
import { apiRequest } from "./client";

export function getSecurityRules(): Promise<SecurityRule[]> {
  return apiRequest<SecurityRule[]>("/api/security/rules/results");
}
```

---

## 26.5. `src/api/eventsApi.ts`

```ts
import type { EventLog } from "../types";
import { apiRequest } from "./client";

export function getEvents(): Promise<EventLog[]> {
  return apiRequest<EventLog[]>("/api/events");
}
```

---

## 26.6. `src/api/systemApi.ts`

```ts
import { apiRequest } from "./client";

export interface SystemStatus {
  label: string;
  description: string;
  status: "ok" | "warning" | "error";
}

export function getSystemStatus(): Promise<SystemStatus> {
  return apiRequest<SystemStatus>("/api/system/status");
}
```

---

# 27. `.env` для подключения backend

Создать файл в корне проекта:

```text
.env
```

Пример:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Если backend на другом порту:

```env
VITE_API_BASE_URL=http://localhost:5000
```

или:

```env
VITE_API_BASE_URL=http://localhost:8080
```

Важно:

```text
в Vite переменные окружения должны начинаться с VITE_
```

После изменения `.env` нужно перезапустить frontend:

```bash
npm run dev
```

---

# 28. Как заменить mockDevices на API

## Шаг 1. Импортировать `useEffect`

В `Dashboard.tsx` было:

```ts
import { useMemo, useState } from "react";
```

Стало:

```ts
import { useEffect, useMemo, useState } from "react";
```

---

## Шаг 2. Импортировать API-функцию

```ts
import { getDevices } from "../api/devicesApi";
```

---

## Шаг 3. Добавить состояния внутри `Dashboard`

```ts
const [devices, setDevices] = useState<Device[]>(mockDevices);
const [isDevicesLoading, setIsDevicesLoading] = useState(false);
const [devicesError, setDevicesError] = useState<string | null>(null);
```

---

## Шаг 4. Добавить загрузку

```ts
useEffect(() => {
  let isMounted = true;

  async function loadDevices() {
    try {
      setIsDevicesLoading(true);
      setDevicesError(null);

      const loadedDevices = await getDevices();

      if (isMounted) {
        setDevices(loadedDevices);
      }
    } catch (error) {
      if (isMounted) {
        setDevicesError(
          error instanceof Error
            ? error.message
            : "Не удалось загрузить список устройств"
        );
      }
    } finally {
      if (isMounted) {
        setIsDevicesLoading(false);
      }
    }
  }

  loadDevices();

  return () => {
    isMounted = false;
  };
}, []);
```

---

## Шаг 5. Заменить `mockDevices` на `devices`

Было:

```tsx
{mockDevices.map((device) => (
```

Стало:

```tsx
{devices.map((device) => (
```

Также заменить:

```ts
mockDevices.length
mockDevices.filter(...)
mockDevices.map(...)
```

на:

```ts
devices.length
devices.filter(...)
devices.map(...)
```

---

# 29. Как заменить остальные mock-данные

## 29.1. Метрики

Создать состояние:

```ts
const [metrics, setMetrics] = useState<MetricCard[]>(metricCards);
const [isMetricsLoading, setIsMetricsLoading] = useState(false);
const [metricsError, setMetricsError] = useState<string | null>(null);
```

Заменить:

```tsx
{metricCards.map((card) => (
```

на:

```tsx
{metrics.map((card) => (
```

---

## 29.2. Проверки безопасности

Создать состояние:

```ts
const [securityRules, setSecurityRules] =
  useState<SecurityRule[]>(mockSecurityRules);
```

Заменить:

```tsx
{mockSecurityRules.map((rule) => (
```

на:

```tsx
{securityRules.map((rule) => (
```

---

## 29.3. События

Создать состояние:

```ts
const [events, setEvents] = useState<EventLog[]>(mockEvents);
```

Заменить:

```tsx
{mockEvents.map((event) => (
```

на:

```tsx
{events.map((event) => (
```

---

# 30. Если backend отдаёт snake_case

Python backend часто отдаёт:

```json
{
  "ip_address": "127.0.0.1",
  "security_score": 58,
  "last_scan_at": "30.09.2021 15:56"
}
```

А frontend ожидает:

```json
{
  "ipAddress": "127.0.0.1",
  "securityScore": 58,
  "lastScanAt": "30.09.2021 15:56"
}
```

Можно решить двумя способами.

## Вариант 1. Backend отдаёт camelCase

Лучший вариант для frontend.

## Вариант 2. Frontend делает mapper

Файл:

```text
src/api/mappers.ts
```

Пример:

```ts
import type { Device } from "../types";

interface DeviceResponse {
  id: string;
  name: string;
  ip_address: string;
  type: Device["type"];
  vendor: string;
  status: Device["status"];
  security_score: number;
  vulnerability_level: Device["vulnerabilityLevel"];
  critical_vulnerabilities: number;
  high_vulnerabilities: number;
  medium_vulnerabilities: number;
  low_vulnerabilities: number;
  last_scan_at: string;
  config_changed: boolean;
}

export function mapDeviceResponse(device: DeviceResponse): Device {
  return {
    id: device.id,
    name: device.name,
    ipAddress: device.ip_address,
    type: device.type,
    vendor: device.vendor,
    status: device.status,
    securityScore: device.security_score,
    vulnerabilityLevel: device.vulnerability_level,
    criticalVulnerabilities: device.critical_vulnerabilities,
    highVulnerabilities: device.high_vulnerabilities,
    mediumVulnerabilities: device.medium_vulnerabilities,
    lowVulnerabilities: device.low_vulnerabilities,
    lastScanAt: device.last_scan_at,
    configChanged: device.config_changed,
  };
}
```

---

# 31. CORS

Если frontend работает на:

```text
http://localhost:5173
```

А backend работает на:

```text
http://localhost:8000
```

то backend должен разрешить CORS.

Без CORS браузер заблокирует запросы.

---

## 31.1. CORS для FastAPI

```py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 31.2. CORS для Express

```js
import express from "express";
import cors from "cors";

const app = express();

app.use(cors({
  origin: ["http://localhost:5173", "http://127.0.0.1:5173"],
  credentials: true,
}));
```

---

## 31.3. CORS для ASP.NET Core

```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("Frontend", policy =>
    {
        policy
            .WithOrigins("http://localhost:5173", "http://127.0.0.1:5173")
            .AllowAnyHeader()
            .AllowAnyMethod()
            .AllowCredentials();
    });
});

app.UseCors("Frontend");
```

---

# 32. Prompt для нейросети: интеграция backend и frontend

Этот prompt можно дать ChatGPT, Copilot, Cursor, Claude или другому AI-агенту.

```text
Ты — senior fullstack-разработчик. Нужно интегрировать существующий React + TypeScript + Vite frontend с backend API.

Контекст frontend:
- Проект называется Config Inspector Frontend.
- Используется React 18+, TypeScript, Vite, Tailwind CSS, Lucide React.
- Сейчас frontend работает без backend.
- Все данные находятся в mock-константах внутри файлов:
  1. src/components/Dashboard.tsx:
     - metricCards
     - mockDevices
     - mockSecurityRules
     - mockEvents
  2. src/components/Header.tsx:
     - systemStatus
- Типы данных находятся в src/types/index.ts.
- Нужно сохранить текущий UI и не сломать визуальную структуру.

Текущая структура frontend:
src/
├── components/
│   ├── Dashboard.tsx
│   ├── Header.tsx
│   └── Sidebar.tsx
├── types/
│   └── index.ts
├── App.tsx
├── main.tsx
└── index.css

Задача:
1. Создать папку src/api.
2. Создать универсальный API-клиент src/api/client.ts.
3. Создать отдельные API-файлы:
   - src/api/dashboardApi.ts
   - src/api/devicesApi.ts
   - src/api/securityApi.ts
   - src/api/eventsApi.ts
   - src/api/systemApi.ts
4. Добавить поддержку переменной окружения VITE_API_BASE_URL.
5. Заменить mock-данные на реальные запросы к backend.
6. Добавить loading/error/empty состояния.
7. Если backend временно недоступен, оставить fallback на mock-данные.
8. Не использовать Redux, Zustand, React Query и тяжёлые библиотеки.
9. Использовать только React useState и useEffect.
10. Не смешивать API-запросы с JSX-разметкой.
11. Все запросы должны быть типизированы через TypeScript.
12. Если backend отдаёт snake_case, создать mapper-функции в src/api/mappers.ts.
13. Код должен быть clean code, DRY, понятный для хакатонной команды.
14. После изменений объяснить, какие файлы были изменены и почему.

Ожидаемые backend endpoint-ы:
GET /api/system/status
GET /api/dashboard/metrics
GET /api/devices
GET /api/security/rules/results
GET /api/events

Ожидаемые frontend-типы:
- Device
- MetricCard
- SecurityRule
- EventLog

Если backend будет на Python FastAPI:
- добавить CORS для http://localhost:5173;
- сделать Pydantic-модели под frontend-типы;
- временно хранить данные в памяти или JSON-файлах;
- отдавать JSON в camelCase или добавить mapper на frontend.

Если backend будет на другом языке:
- сохранить тот же API-контракт;
- отдавать JSON в формате, совместимом с TypeScript-интерфейсами frontend.

Выдай готовый код по файлам и краткую инструкцию запуска frontend + backend.
```

---

# 33. Prompt для нейросети: backend на Python FastAPI

```text
Ты — senior Python FastAPI + React TypeScript разработчик.

Нужно создать backend на Python FastAPI и подключить его к существующему frontend.

Frontend:
- React
- TypeScript
- Vite
- Tailwind CSS
- Lucide React
- mock-данные сейчас находятся в Dashboard.tsx и Header.tsx
- типы находятся в src/types/index.ts

Backend должен реализовать endpoint-ы:
GET /api/system/status
GET /api/dashboard/metrics
GET /api/devices
GET /api/security/rules/results
GET /api/events

Требования к backend:
1. Использовать FastAPI.
2. Добавить CORS для http://localhost:5173.
3. Создать Pydantic-модели:
   - Device
   - MetricCard
   - SecurityRule
   - EventLog
   - SystemStatus
4. Временно хранить данные в Python-списках или JSON-файлах.
5. Вернуть JSON в формате, который frontend может использовать без сложных преобразований.
6. Добавить requirements.txt.
7. Добавить команду запуска через uvicorn.
8. Не использовать базу данных на первом этапе.
9. Код должен быть простым, чистым и понятным.
10. Добавить README-инструкцию запуска backend.

Требования к frontend:
1. Создать src/api/client.ts.
2. Создать:
   - src/api/dashboardApi.ts
   - src/api/devicesApi.ts
   - src/api/securityApi.ts
   - src/api/eventsApi.ts
   - src/api/systemApi.ts
3. Добавить .env:
   VITE_API_BASE_URL=http://localhost:8000
4. Заменить mock-данные на API-запросы.
5. Добавить loading/error/empty состояния.
6. Сохранить текущий интерфейс без визуальных поломок.

Выдай:
1. Структуру backend-проекта.
2. Код backend-файлов.
3. Код frontend API layer.
4. Точные изменения в Dashboard.tsx и Header.tsx.
5. Инструкцию запуска backend.
6. Инструкцию запуска frontend.
7. Чеклист проверки интеграции.
```

---

# 34. Prompt для нейросети: если язык backend неизвестен

```text
Ты — senior fullstack architect. Backend-язык пока неизвестен. Нужно подготовить frontend к интеграции с любым REST API.

Задача:
1. Не привязываться к конкретному backend-фреймворку.
2. Описать API-контракт.
3. Создать frontend API layer:
   - src/api/client.ts
   - src/api/dashboardApi.ts
   - src/api/devicesApi.ts
   - src/api/securityApi.ts
   - src/api/eventsApi.ts
   - src/api/systemApi.ts
4. Добавить mapper-функции на случай, если backend отдаёт snake_case, а frontend использует camelCase.
5. Добавить loading/error/empty состояния.
6. Добавить fallback на mock-данные, если API временно недоступен.
7. Сохранить существующий UI.
8. Не использовать Redux, Zustand, React Query или тяжёлые библиотеки.
9. Использовать только React useState/useEffect.
10. Сделать код понятным для хакатонной команды.

Frontend:
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Lucide React

Выдай структуру файлов, код и инструкцию подключения к backend.
```

---

# 35. Prompt для нейросети: если backend на C# ASP.NET Core

```text
Ты — senior ASP.NET Core + React TypeScript разработчик.

Нужно связать React frontend на Vite с backend на ASP.NET Core Web API.

Frontend:
- React 18
- TypeScript
- Vite
- Tailwind CSS
- mock-данные сейчас в Dashboard.tsx и Header.tsx

Backend:
- ASP.NET Core Web API
- C#
- REST endpoint-ы:
  GET /api/system/status
  GET /api/dashboard/metrics
  GET /api/devices
  GET /api/security/rules/results
  GET /api/events

Требуется:
1. Создать DTO-модели под frontend-типы.
2. Сделать контроллеры:
   - SystemController
   - DashboardController
   - DevicesController
   - SecurityController
   - EventsController
3. Временно отдавать mock-данные из backend.
4. Настроить CORS для http://localhost:5173.
5. Подготовить frontend API-клиент через fetch.
6. Использовать .env с VITE_API_BASE_URL.
7. Добавить loading/error состояния.
8. Сохранить текущий интерфейс.
9. Дать инструкцию запуска backend и frontend.
10. Выдать готовый код по файлам.
```

---

# 36. Как тестировать подключение backend

Когда backend появится:

## Шаг 1

Запустить backend.

Например FastAPI:

```bash
uvicorn main:app --reload --port 8000
```

## Шаг 2

Проверить backend в браузере:

```text
http://localhost:8000/api/devices
```

Если JSON открывается — backend работает.

## Шаг 3

Создать `.env` во frontend:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Шаг 4

Перезапустить frontend:

```bash
npm run dev
```

## Шаг 5

Открыть DevTools:

```text
F12 -> Network
```

## Шаг 6

Проверить запросы:

```text
/api/devices
/api/events
/api/dashboard/metrics
/api/security/rules/results
/api/system/status
```

---

# 37. Возможные ошибки backend-интеграции

## 37.1. Ошибка CORS

Симптом:

```text
Access to fetch at ... has been blocked by CORS policy
```

Решение:

настроить CORS на backend.

---

## 37.2. Ошибка 404

Симптом:

```text
GET /api/devices 404
```

Причина:

endpoint не создан или путь отличается.

Решение:

проверить backend route.

---

## 37.3. Ошибка 500

Симптом:

```text
GET /api/devices 500
```

Причина:

ошибка внутри backend.

Решение:

смотреть консоль backend.

---

## 37.4. Данные пришли, но frontend сломался

Причина:

JSON не совпадает с TypeScript-интерфейсом.

Например backend отдаёт:

```json
{
  "ip_address": "127.0.0.1"
}
```

А frontend ждёт:

```json
{
  "ipAddress": "127.0.0.1"
}
```

Решение:

```text
либо backend отдаёт camelCase
либо frontend добавляет mapper
```

---

# 38. Минимальный план работы команды

```text
1. Исправить структуру: scr -> src.
2. Проверить наличие package.json.
3. Проверить наличие index.html.
4. Проверить наличие vite.config.ts.
5. Проверить наличие src/main.tsx.
6. Проверить наличие src/index.css.
7. Запустить npm install.
8. Запустить npm run dev.
9. Проверить интерфейс.
10. Согласовать API-контракт.
11. Создать backend endpoint-ы.
12. Создать src/api на frontend.
13. Заменить mockDevices на getDevices().
14. Заменить metricCards на getDashboardMetrics().
15. Заменить mockSecurityRules на getSecurityRules().
16. Заменить mockEvents на getEvents().
17. Заменить systemStatus на getSystemStatus().
18. Проверить CORS.
19. Проверить Network в браузере.
20. Подготовить демо.
```

---

# 39. Демо-сценарий для защиты

Можно показывать так:

```text
1. Открываем Dashboard.
2. Показываем общее состояние инфраструктуры.
3. Показываем карточку "Контроль изменений".
4. Показываем карточку "Проверки безопасности".
5. Показываем блок "Самые уязвимые устройства".
6. Переходим во вкладку "Устройства".
7. Выбираем несколько устройств checkbox-ами.
8. Показываем статусы:
   - доступен;
   - нет связи;
   - ошибка авторизации;
   - критично.
9. Переходим во вкладку "Проверки безопасности".
10. Показываем проваленные проверки:
   - Telnet;
   - SNMP public/private;
   - слабые пароли;
   - отсутствие логирования.
11. Переходим во вкладку "События".
12. Показываем, как оператор принимает событие.
13. Объясняем, что backend потом будет собирать реальные конфигурации устройств.
14. Объясняем, что frontend уже готов к подключению API.
```

---

# 40. Что критически важно не забыть

```text
[!] Папка должна называться src, не scr.
[!] В корне должен быть package.json.
[!] В корне должен быть index.html.
[!] В корне должен быть vite.config.ts.
[!] В src должен быть main.tsx.
[!] В src должен быть index.css.
[!] Нужно выполнить npm install.
[!] Запускать через npm run dev.
[!] Адрес смотреть в терминале.
[!] Mock-данные лежат в Dashboard.tsx и Header.tsx.
[!] Backend должен отдавать JSON.
[!] Для backend нужен CORS.
[!] VITE_API_BASE_URL хранится в .env.
```

---

# 41. Быстрый запуск

```bash
npm install
npm run dev
```

Открыть:

```text
http://localhost:5173/
```

---

# 42. Краткая шпаргалка по файлам

```text
src/App.tsx
Главная сборка интерфейса. Соединяет Sidebar, Header и Dashboard.

src/components/Sidebar.tsx
Левое меню навигации.

src/components/Header.tsx
Верхняя панель: поиск, статус системы, уведомления, профиль.

src/components/Dashboard.tsx
Главный экран: метрики, вкладки, таблица устройств, проверки, события.

src/types/index.ts
Все TypeScript-типы данных.

src/main.tsx
Точка входа React-приложения.

src/index.css
Подключение Tailwind CSS.

package.json
Список зависимостей и команд запуска.

vite.config.ts
Конфигурация Vite.

index.html
HTML-точка входа приложения.

README.md
Документация проекта.
```

---

# 43. Итог

Этот frontend уже можно использовать как основу для демонстрации.

Сейчас он работает на mock-данных.

Дальше команда должна:

```text
1. Запустить проект.
2. Проверить интерфейс.
3. Согласовать backend API.
4. Добавить src/api.
5. Заменить mock-данные на API.
6. Добавить loading/error.
7. Подключить реальный backend.
8. Подготовить демо-сценарий.
```

Главная цель текущего README — чтобы любой участник команды открыл проект и сразу понял:

```text
где что лежит
что за что отвечает
как запустить
где mock-данные
как подключать backend
что делать при ошибках
какой prompt дать нейросети для интеграции
```
