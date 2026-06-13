export default function Badge({ children, variant = 'default', className = '' }) {
  const styles = {
    default:  { background: '#f0f0f0',  color: '#333',     border: '1px solid #e5e5e5' },
    danger:   { background: '#fff1f2',  color: '#e11d48',  border: '1px solid #fecdd3' },
    success:  { background: '#f0fdf4',  color: '#15803d',  border: '1px solid #bbf7d0' },
    warning:  { background: '#fffbeb',  color: '#92400e',  border: '1px solid #fde68a' },
    dark:     { background: '#000',     color: '#fff',     border: '1px solid #000'    },
  };
  const s = styles[variant] || styles.default;

  return (
    <span
      className={className}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '4px',
        padding: '3px 10px',
        fontSize: '0.7rem',
        fontWeight: 700,
        letterSpacing: '0.06em',
        textTransform: 'uppercase',
        ...s,
      }}
    >
      {children}
    </span>
  );
}
