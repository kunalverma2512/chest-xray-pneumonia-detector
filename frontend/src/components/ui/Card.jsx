export default function Card({ children, className = '', dark = false }) {
  return (
    <div
      className={className}
      style={{
        background: dark ? '#000' : '#fff',
        border: '1px solid',
        borderColor: dark ? '#222' : 'var(--border)',
        padding: '1.5rem',
        color: dark ? '#fff' : '#000',
      }}
    >
      {children}
    </div>
  );
}
