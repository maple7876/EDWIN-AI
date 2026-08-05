import StatusCard from "./StatusCard";
import HardwarePanel from "./HardwarePanel";

import type { Status } from "../types/status";
import type { HardwareData } from "../types/hardware";


interface HeaderProps {
  status: Status;
  hardware: HardwareData | null;
}


function Header({ status, hardware }: HeaderProps) {

  return (
    <header className="header">

      <div>

        <h2>
          EDWIN Alpha
        </h2>

        <p>
          Local Intelligence System
        </p>


        {hardware && (
          <HardwarePanel hardware={hardware} />
        )}

      </div>


      <div className="status">

        <StatusCard
          title="Model"
          value={status.model}
        />


        <StatusCard
          title="Memory"
          value={
            status.memory
              ? "Enabled"
              : "Disabled"
          }
        />

      </div>


    </header>
  );
}


export default Header;