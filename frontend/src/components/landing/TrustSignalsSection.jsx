import { ShieldCheck, Code2, BookOpen, Lock } from 'lucide-react';

const SIGNALS = [
  { icon: <ShieldCheck size={18} />, text: 'No PHI stored — images processed in-memory only' },
  { icon: <Code2 size={18} />,       text: 'Fully open-source — inspect every line' },
  { icon: <BookOpen size={18} />,    text: 'Cross-operator peer-reviewed validation methodology' },
  { icon: <Lock size={18} />,        text: 'API deployed with CORS controls and rate limiting' },
];

export default function TrustSignalsSection() {
  return (
    <section style={{ width: '100%', background: '#f9f9f9', padding: '0', boxSizing: 'border-box' }}>
      <div className="trust-grid" style={{ borderTop: '1px solid #e5e5e5', borderBottom: '1px solid #e5e5e5' }}>

        {/* Left — headline */}
        <div style={{ background: '#fff', padding: '5rem 3rem', boxSizing: 'border-box', borderRight: '1px solid #e5e5e5' }}>
          <span className="label" style={{ display: 'inline-flex', marginBottom: '1.5rem' }}>Trust & Transparency</span>
          <h2 style={{
            fontSize: 'clamp(1.75rem, 4vw, 3rem)',
            fontWeight: 800,
            letterSpacing: '-0.03em',
            color: '#000',
            margin: '1rem 0 1rem',
            lineHeight: 1.15,
          }}>
            Built for clinical<br />accountability.
          </h2>
          <p style={{ fontSize: '1rem', color: '#777', maxWidth: '360px', lineHeight: 1.7, margin: 0 }}>
            AI tools in clinical settings must be auditable, transparent, and safe.
            Every design decision reflects that principle.
          </p>
        </div>

        {/* Right — signal list */}
        <div style={{ background: '#fff', padding: '5rem 3rem', display: 'flex', alignItems: 'center', boxSizing: 'border-box' }}>
          <ul style={{ listStyle: 'none', margin: 0, padding: 0, display: 'flex', flexDirection: 'column', gap: '0', width: '100%' }}>
            {SIGNALS.map(({ icon, text }, i) => (
              <li
                key={text}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '1rem',
                  padding: '1.5rem 0',
                  borderBottom: i < SIGNALS.length - 1 ? '1px solid #e5e5e5' : 'none',
                }}
              >
                <div style={{ width: '36px', height: '36px', border: '1px solid #e5e5e5', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                  {icon}
                </div>
                <span style={{ fontSize: '0.9375rem', color: '#333', lineHeight: 1.5, marginTop: '8px' }}>{text}</span>
              </li>
            ))}
          </ul>
        </div>

      </div>
    </section>
  );
}
