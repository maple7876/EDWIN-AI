import { useEffect, useState } from "react";
import { getHardware } from "../api/hardware";
import { completeOnboarding } from "../services/api";

type ModelChoice = {
  name: string;
  model: string;
  description: string;
};

type HardwareData = {
  system: {
    cpu: string;
    cores: number;
    ram: number;
    gpu: boolean;
  };
  choices: ModelChoice[];
};

type ModelSelectionProps = {
  onComplete: () => void;
};

export default function ModelSelection({
  onComplete,
}: ModelSelectionProps) {
  const [hardware, setHardware] = useState<HardwareData | null>(null);
  const [selectingModel, setSelectingModel] = useState<string | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getHardware()
      .then((data) => setHardware(data))
      .catch(() => {
        setError("Unable to analyze this computer's hardware.");
      });
  }, []);

  async function handleModelSelection(model: string) {
    try {
      setSelectingModel(model);
      setError("");

      await completeOnboarding(model);

      onComplete();
    } catch (error) {
      console.error(error);
      setError("Unable to save model selection.");
      setSelectingModel(null);
    }
  }

  if (error) {
    return (
      <div style={{ padding: 40 }}>
        <h1>EDWIN Setup</h1>
        <p>{error}</p>
      </div>
    );
  }

  if (!hardware) {
    return (
      <div style={{ padding: 40 }}>
        <h1>Analyzing your computer...</h1>
        <p>EDWIN is determining which AI models this system can run.</p>
      </div>
    );
  }

  return (
    <div style={{ padding: 40 }}>
      <h1>Choose Your AI Model</h1>

      <p>
        EDWIN has analyzed your system and selected models suitable for this
        computer.
      </p>

      <h3>Detected Hardware</h3>

      <p>
        <strong>CPU:</strong> {hardware.system.cpu}
      </p>

      <p>
        <strong>Cores:</strong> {hardware.system.cores}
      </p>

      <p>
        <strong>RAM:</strong> {hardware.system.ram} GB
      </p>

      <p>
        <strong>GPU:</strong>{" "}
        {hardware.system.gpu ? "Detected" : "Not Detected"}
      </p>

      <hr />

      <h3>Recommended Models</h3>

      {hardware.choices.map((model) => (
        <div
          key={model.model}
          style={{
            marginTop: 20,
            padding: 20,
            border: "1px solid #444",
            borderRadius: 12,
          }}
        >
          <h3>{model.name}</h3>

          <p>
            <strong>Model:</strong> {model.model}
          </p>

          <p>{model.description}</p>
<button
  type="button"
  onClick={() => handleModelSelection(model.model)}
  disabled={selectingModel !== null}
>
  {selectingModel === model.model
    ? "Setting up..."
    : `Use ${model.name}`}
</button>
        </div>
      ))}

      {error && (
        <p style={{ marginTop: 20 }}>
          {error}
        </p>
      )}
    </div>
  );
}