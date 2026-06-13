export default function MetricSummaryCard({ label, value, delta, important = false }) {
  return (
    <div
      style={{
        background: important ? '#000' : '#fff',
        border: '1px solid var(--border)',
        padding: '1.5rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '4px',
      }}
    >
      <span
        style={{
          fontSize: '1.75rem',
          fontWeight: 900,
          letterSpacing: '-0.03em',
          color: important ? '#fff' : '#000',
        }}
      >
        {value}
      </span>
      <span style={{ fontSize: '0.825rem', fontWeight: 600, color: important ? '#ccc' : '#333' }}>
        {label}
      </span>
      {delta && (
        <span style={{ fontSize: '0.7rem', color: important ? '#666' : '#999', lineHeight: 1.4 }}>
          {delta}
        </span>
      )}
    </div>
  );
}
