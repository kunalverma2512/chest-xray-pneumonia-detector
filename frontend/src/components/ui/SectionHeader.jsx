export default function SectionHeader({ label, title, subtitle, centered = true, className = '' }) {
  return (
    <div
      className={className}
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
        marginBottom: '3rem',
        alignItems: centered ? 'center' : 'flex-start',
        textAlign: centered ? 'center' : 'left',
      }}
    >
      {label && <span className="label">{label}</span>}
      <h2 className="text-heading text-black" style={{ maxWidth: '600px' }}>{title}</h2>
      {subtitle && (
        <p className="text-body text-muted" style={{ maxWidth: '500px', lineHeight: 1.7 }}>{subtitle}</p>
      )}
    </div>
  );
}
