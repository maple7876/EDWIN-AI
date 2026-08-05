interface StatusCardProps {
  title: string;
  value: string;
}

function StatusCard({ title, value }: StatusCardProps) {
  return (
    <div className="status-card">
      <span>{title}</span>
      <strong>{value}</strong>
    </div>
  );
}

export default StatusCard;