export interface SystemInfo {
  cpu: string;
  cores: number;
  ram: number;
  gpu: boolean;
}

export interface ModelChoice {
  name: string;
  model: string;
  description: string;
}

export interface HardwareData {
  system: SystemInfo;
  choices: ModelChoice[];
}