import { NavLink } from 'react-router-dom';
import { ExternalLink } from 'lucide-react';

const FOOTER_LINKS = [
  {
    group: 'Product',
    links: [
      { to: '/upload',         label: 'Analyse X-Ray' },
      { to: '/model-insights', label: 'Model Insights' },
      { to: '/faq',            label: 'FAQ' },
    ],
  },
  {
    group: 'Project',
    links: [
      { to: '/about',   label: 'About' },
      { to: '/contact', label: 'Contact' },
      { href: 'http://localhost:8000/docs', label: 'API Docs', external: true },
    ],
  },
];

export default function Footer() {
  return (
    <footer style={{ background: '#000', color: '#fff', borderTop: '1px solid #111' }}>
      <div
        style={{
          maxWidth: '1280px',
          margin: '0 auto',
          padding: '4rem 1.5rem',
        }}
      >
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr auto auto',
            gap: '4rem',
            alignItems: 'start',
          }}
          className="grid-cols-1 md:grid-cols-3"
        >
          {/* Brand */}
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '1rem' }}>
              <span
                style={{
                  width: '28px',
                  height: '28px',
                  background: '#fff',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M1 7h2.5l2-4 3 8 2-4H13" stroke="black" strokeWidth="1.5" strokeLinecap="square"/>
                </svg>
              </span>
              <span style={{ fontWeight: 800, fontSize: '0.95rem', letterSpacing: '-0.02em' }}>
                PneumoDetect<span style={{ color: '#e11d48' }}>AI</span>
              </span>
            </div>
            <p style={{ fontSize: '0.8125rem', color: '#666', lineHeight: 1.6, maxWidth: '240px' }}>
              Clinical-grade AI pneumonia screening.
              97.6% sensitivity on 485 independent samples.
            </p>
          </div>

          {/* Links */}
          {FOOTER_LINKS.map(({ group, links }) => (
            <div key={group}>
              <p style={{ fontSize: '0.7rem', fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', color: '#555', marginBottom: '1rem' }}>
                {group}
              </p>
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {links.map(({ to, href, label, external }) => (
                  <li key={label}>
                    {external ? (
                      <a
                        href={href}
                        target="_blank"
                        rel="noreferrer"
                        style={{ fontSize: '0.8125rem', color: '#888', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '4px' }}
                        onMouseEnter={e => e.currentTarget.style.color = '#fff'}
                        onMouseLeave={e => e.currentTarget.style.color = '#888'}
                      >
                        {label} <ExternalLink size={10} />
                      </a>
                    ) : (
                      <NavLink
                        to={to}
                        style={{ fontSize: '0.8125rem', color: '#888', textDecoration: 'none' }}
                        onMouseEnter={e => e.currentTarget.style.color = '#fff'}
                        onMouseLeave={e => e.currentTarget.style.color = '#888'}
                      >
                        {label}
                      </NavLink>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom bar */}
        <div
          style={{
            borderTop: '1px solid #111',
            marginTop: '3rem',
            paddingTop: '2rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '4px',
          }}
        >
          <p style={{ fontSize: '0.75rem', color: '#444' }}>
            © {new Date().getFullYear()} PneumoDetectAI. For research and clinical validation purposes only.
          </p>
          <p style={{ fontSize: '0.75rem', color: '#333' }}>
            MobileNetV2 · 82.7% cross-operator accuracy · 97.6% sensitivity · ROC-AUC 0.961
          </p>
        </div>
      </div>
    </footer>
  );
}
