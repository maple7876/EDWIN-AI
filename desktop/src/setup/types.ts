export type SetupStatus =
  | "not_started" | "detecting_system" | "choose_model" | "downloading"
  | "verifying" | "completed" | "failed";

export type SetupError = { code: string; message: string; detail?: string; retryable: boolean };

export type ModelChoice = {
  model_id: string;
  display_name: string;
  provider_model: string;
  parameter_count_billions: number;
  download_size_bytes: number;
  tier: "fast" | "balanced" | "smart";
  compatibility: { status: "recommended" | "compatible" | "not_recommended" | "incompatible"; reasons: Array<{ code: string; message: string }> };
};

export type Detection = {
  hardware: { cpu: { model: string | null; logical_cores: number | null }; memory: { total_gib: number }; storage: { available_gib: number }; architecture: { is_apple_silicon: boolean } };
  runtime: { status: string; executable: { version: string | null; found: boolean }; error: SetupError | null };
  models: { choices: ModelChoice[] };
};
