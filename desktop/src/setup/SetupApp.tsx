import { useEffect, useState } from "react";
import { setupApi } from "./api";
import type { Detection, ModelChoice, SetupError, SetupStatus } from "./types";

type Props = { onComplete: () => void };

const size = (bytes: number) => `${(bytes / 1_000_000_000).toFixed(bytes < 10_000_000_000 ? 1 : 0)} GB`;

export default function SetupApp({ onComplete }: Props) {
  const [status, setStatus] = useState<SetupStatus>("detecting_system");
  const [detection, setDetection] = useState<Detection | null>(null);
  const [selected, setSelected] = useState<ModelChoice | null>(null);
  const [error, setError] = useState<SetupError | null>(null);
  const [progress, setProgress] = useState<number | null>(null);
  const [message, setMessage] = useState("Analyzing this Mac...");

  const detect = async () => {
    setStatus("detecting_system"); setError(null); setMessage("Analyzing this Mac...");
    try { const data = await setupApi.detect(); setDetection(data); setStatus("choose_model"); }
    catch (caught) { setError(caught as SetupError); setStatus("failed"); }
  };

  useEffect(() => {
    const timer = window.setTimeout(() => { void detect(); }, 0);
    return () => window.clearTimeout(timer);
  }, []);

  const select = async (model: ModelChoice) => {
    setError(null);
    try { await setupApi.select(model.model_id); setSelected(model); }
    catch (caught) { setError(caught as SetupError); }
  };

  const install = async () => {
    setError(null); setStatus("downloading"); setProgress(null); setMessage("Preparing model download...");
    try { await setupApi.install(); }
    catch (caught) { setError(caught as SetupError); setStatus("failed"); }
  };

  useEffect(() => {
    if (status !== "downloading") return;
    const timer = window.setInterval(async () => {
      try {
        const data = await setupApi.installStatus();
        if (data.installation) { setProgress(data.installation.progress.percent); setMessage(data.installation.message); }
        if (data.setup_status === "verifying") { window.clearInterval(timer); setStatus("verifying"); }
        if (data.installation?.status === "failed") { window.clearInterval(timer); setError(data.installation.error); setStatus("failed"); }
      } catch (caught) { window.clearInterval(timer); setError(caught as SetupError); setStatus("failed"); }
    }, 800);
    return () => window.clearInterval(timer);
  }, [status]);

  useEffect(() => {
    if (status !== "verifying") return;
    const timer = window.setTimeout(() => {
      setMessage("Verifying the installed model...");
      void setupApi.verify().then(() => { setStatus("completed"); }).catch((caught) => { setError(caught as SetupError); setStatus("failed"); });
    }, 0);
    return () => window.clearTimeout(timer);
  }, [status]);

  const retry = () => {
    if (error?.code.includes("RUNTIME")) void detect();
    else if (selected) void install();
    else void detect();
  };

  if (status === "detecting_system") return <section className="setup-screen"><div className="setup-orb" /><p className="setup-kicker">EDWIN ALPHA SETUP</p><h1>Getting to know your Mac</h1><p>{message}</p></section>;
  if (status === "downloading" || status === "verifying") return <section className="setup-screen"><p className="setup-kicker">EDWIN ALPHA SETUP</p><h1>{status === "verifying" ? "Verifying your model" : "Downloading your model"}</h1><p>{message}</p><div className="setup-progress"><span style={{ width: `${progress ?? 8}%` }} /></div><p>{progress === null ? "Progress will appear as Ollama reports it." : `${progress}%`}</p></section>;
  if (status === "completed") return <section className="setup-screen"><p className="setup-kicker">SETUP COMPLETE</p><h1>EDWIN is ready.</h1><p>{selected?.display_name ?? "Your verified local model"} is prepared for private, local conversations.</p><button onClick={onComplete}>Open EDWIN</button></section>;
  if (status === "failed") return <section className="setup-screen"><p className="setup-kicker">SETUP NEEDS ATTENTION</p><h1>{error?.code ?? "Setup failed"}</h1><p>{error?.message ?? "EDWIN could not complete setup."}</p><button onClick={retry}>{error?.retryable ? "Retry" : "Check system again"}</button></section>;
  return <section className="setup-screen setup-selection"><p className="setup-kicker">EDWIN ALPHA SETUP</p><h1>Choose your local intelligence</h1>{detection && <p className="setup-hardware">{detection.hardware.cpu.model ?? "Apple Silicon"} · {detection.hardware.memory.total_gib} GB unified memory · {detection.hardware.storage.available_gib} GB free</p>}{detection?.runtime.status !== "available" && <div className="setup-warning"><strong>Ollama is required.</strong><br />{detection?.runtime.error?.message ?? "Start Ollama, then retry system detection."}<button onClick={detect}>Check again</button></div>}<div className="model-grid">{detection?.models.choices.map((model) => <article className={`model-card ${selected?.model_id === model.model_id ? "selected" : ""}`} key={model.model_id}><p>{model.tier.toUpperCase()}</p><h2>{model.display_name}</h2><small>{model.provider_model} · {size(model.download_size_bytes)}</small><strong className={`compatibility ${model.compatibility.status}`}>{model.compatibility.status.replace("_", " ")}</strong>{model.compatibility.reasons.map((reason) => <p className="model-reason" key={reason.code}>{reason.message}</p>)}<button disabled={model.compatibility.status === "incompatible"} onClick={() => select(model)}>{selected?.model_id === model.model_id ? "Selected" : "Select"}</button></article>)}</div>{selected && <button className="setup-primary" disabled={detection?.runtime.status !== "available"} onClick={install}>Download {selected.display_name}</button>}</section>;
}
