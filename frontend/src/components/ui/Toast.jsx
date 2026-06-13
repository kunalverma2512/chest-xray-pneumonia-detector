import { useEffect, useState } from 'react';
import { CheckCircle, XCircle, AlertCircle, X } from 'lucide-react';

const ICONS = {
  success: <CheckCircle size={18} style={{ color: '#15803d' }} />,
  error:   <XCircle    size={18} style={{ color: 'var(--red)' }} />,
  warning: <AlertCircle size={18} style={{ color: '#92400e' }} />,
};

export default function Toast({ message, type = 'success', onDismiss, duration = 4000 }) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const t = setTimeout(() => {
      setVisible(false);
      setTimeout(onDismiss, 300);
    }, duration);
    return () => clearTimeout(t);
  }, [duration, onDismiss]);

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '1.5rem',
        right: '1.5rem',
        zIndex: 50,
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        background: '#fff',
        border: '1px solid var(--border)',
        boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
        padding: '0.875rem 1.25rem',
        opacity: visible ? 1 : 0,
        transform: visible ? 'translateY(0)' : 'translateY(12px)',
        transition: 'opacity 0.3s, transform 0.3s',
      }}
    >
      {ICONS[type]}
      <p style={{ fontSize: '0.875rem', color: '#000', flex: 1 }}>{message}</p>
      <button
        onClick={onDismiss}
        style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#999', marginLeft: '8px', display: 'flex' }}
      >
        <X size={16} />
      </button>
    </div>
  );
}
