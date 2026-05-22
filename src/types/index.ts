export type DeviceStatus =
  | "available"
  | "offline"
  | "auth_error"
  | "warning"
  | "critical"
  | "service_mode";

export type Severity = "critical" | "high" | "medium" | "low" | "none";

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

export type SecurityCheckStatus = "passed" | "failed" | "warning" | "not_checked";

export interface MetricCard {
  id: string;
  title: string;
  value: number | string;
  description: string;
  trend?: number;
  color: "blue" | "green" | "red" | "yellow" | "purple" | "gray";
}

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

export interface SecurityRule {
  id: string;
  name: string;
  deviceName: string;
  status: SecurityCheckStatus;
  severity: Severity;
  description: string;
  checkedAt: string;
}

export interface EventLog {
  id: string;
  timestamp: string;
  deviceName: string;
  eventType: "config_change" | "security_check" | "auth_error" | "device_down" | "system";
  severity: Severity;
  message: string;
  accepted: boolean;
}

export interface DashboardSummary {
  changedReports: number;
  securityRulesCompleted: number;
  totalSecurityRules: number;
  criticalDevices: number;
  availableDevices: number;
  offlineDevices: number;
  authErrorDevices: number;
}