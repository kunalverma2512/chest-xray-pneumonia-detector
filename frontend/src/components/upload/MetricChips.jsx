import { diagnosisBadge, confidenceLevelBadge, formatConfidence } from '../../utils/formatters.js';

function Chip({ label, value, inverted = false }) {
  return (
    <div
      style={{
        border: '1px solid var(--border)',
        padding: '0.75rem 1rem',
        background: inverted ? '#000' : '#fff',
        display: 'flex',
        flexDirection: 'column',
        gap: '4px',
      }}
    >
      <span style={{ fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: inverted ? '#888' : '#999' }}>{label}</span>
      <span style={{ fontWeight: 800, fontSize: '1rem', color: inverted ? '#fff' : '#000' }}>{value}</span>
    </div>
  );
}

export default function MetricChips({ data }) {
  if (!data) return null;
  const { diagnosis, confidence, confidence_level } = data;
  return (
    <div className="grid grid-cols-3 gap-px" style={{ background: 'var(--border)' }}>
      <Chip label="Diagnosis"  value={diagnosis}                inverted={diagnosis === 'PNEUMONIA'} />
      <Chip label="Confidence" value={formatConfidence(confidence)} />
      <Chip label="Level"      value={confidence_level} />
    </div>
  );
}
