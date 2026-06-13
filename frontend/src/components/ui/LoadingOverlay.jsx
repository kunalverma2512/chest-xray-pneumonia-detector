export default function LoadingOverlay({ message = 'Analysing X-ray…' }) {
  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 50,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'rgba(255,255,255,0.9)',
        backdropFilter: 'blur(4px)',
        gap: '1.5rem',
      }}
    >
      <div
        style={{
          width: '48px',
          height: '48px',
          border: '3px solid #e5e5e5',
          borderTopColor: '#000',
          borderRadius: '50%',
          animation: 'spin 0.8s linear infinite',
        }}
      />
      <p style={{ fontSize: '1rem', fontWeight: 500, color: '#555' }}>{message}</p>
    </div>
  );
}
