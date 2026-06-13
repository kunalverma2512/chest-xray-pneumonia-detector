import { useState } from 'react';
import { ChevronDown } from 'lucide-react';

export default function FaqItem({ question, answer }) {
  const [open, setOpen] = useState(false);

  return (
    <div style={{ borderBottom: '1px solid var(--border)' }}>
      <button
        onClick={() => setOpen(v => !v)}
        style={{
          width: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '1.5rem 0',
          background: 'none',
          border: 'none',
          cursor: 'pointer',
          textAlign: 'left',
          gap: '1.5rem',
        }}
      >
        <span style={{ fontWeight: 600, color: '#000', fontSize: '0.9375rem', lineHeight: 1.4 }}>
          {question}
        </span>
        <ChevronDown
          size={18}
          style={{
            flexShrink: 0,
            color: '#999',
            transition: 'transform 0.25s',
            transform: open ? 'rotate(180deg)' : 'rotate(0deg)',
          }}
        />
      </button>
      <div
        style={{
          overflow: 'hidden',
          maxHeight: open ? '500px' : '0',
          transition: 'max-height 0.3s ease',
        }}
      >
        <p style={{ fontSize: '0.875rem', color: '#555', lineHeight: 1.8, paddingBottom: '1.5rem' }}>
          {answer}
        </p>
      </div>
    </div>
  );
}
