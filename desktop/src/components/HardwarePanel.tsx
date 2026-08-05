import type { HardwareData } from "../types/hardware";

interface HardwarePanelProps {
  hardware: HardwareData;
}

function HardwarePanel({ hardware }: HardwarePanelProps) {
  return (
    <div className="hardware-panel">
      <div className="hardware-item">
        <span>CPU</span>
        <strong>{hardware.system.cpu}</strong>
      </div>

      <div className="hardware-item">
        <span>Cores</span>
        <strong>{hardware.system.cores}</strong>
      </div>

      <div className="hardware-item">
        <span>RAM</span>
        <strong>{hardware.system.ram} GB</strong>
      </div>

      <div className="hardware-item">
        <span>GPU</span>
        <strong>
          {hardware.system.gpu
            ? "Detected"
            : "Not Detected"}
        </strong>
      </div>
    </div>
  );
}

export default HardwarePanel;