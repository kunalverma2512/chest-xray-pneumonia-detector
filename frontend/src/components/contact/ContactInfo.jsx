import { Code2, ExternalLink, Mail } from 'lucide-react';

const INFO = [
  {
    icon: <Code2 size={16} />,
    label: 'Open Source',
    value: 'GitHub Repository',
    href: 'https://github.com/kunalverma2512/chest-xray-pneumonia-detector',
  },
  {
    icon: <ExternalLink size={16} />,
    label: 'API Documentation',
    value: 'localhost:8000/docs',
    href: 'http://localhost:8000/docs',
  },
  {
    icon: <Mail size={16} />,
    label: 'Response Time',
    value: 'Within 48 hours',
  },
];

export default function ContactInfo() {
  return (
    <aside className="lg:col-span-2" style={{ display: 'flex', flexDirection: 'column', gap: '1px', background: 'var(--border)' }}>
      {INFO.map(({ icon, label, value, href }) => (
        <div
          key={label}
          style={{ background: '#fff', padding: '1.5rem', display: 'flex', gap: '1rem', alignItems: 'flex-start' }}
        >
          <div style={{ width: '36px', height: '36px', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
            {icon}
          </div>
          <div>
            <p style={{ fontSize: '0.7rem', color: '#999', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '4px' }}>
              {label}
            </p>
            {href ? (
              <a
                href={href}
                target="_blank"
                rel="noreferrer"
                style={{ fontSize: '0.875rem', fontWeight: 600, color: '#000', textDecoration: 'none' }}
                onMouseEnter={e => e.currentTarget.style.textDecoration = 'underline'}
                onMouseLeave={e => e.currentTarget.style.textDecoration = 'none'}
              >
                {value}
              </a>
            ) : (
              <p style={{ fontSize: '0.875rem', fontWeight: 600, color: '#000' }}>{value}</p>
            )}
          </div>
        </div>
      ))}

      <div style={{ background: '#fafafa', padding: '1.5rem', border: '1px solid var(--border)' }}>
        <p style={{ fontSize: '0.8125rem', color: '#666', lineHeight: 1.6 }}>
          For clinical partnerships, institutional deployments, or research collaborations,
          please include your institution and a brief description of your use case.
        </p>
      </div>
    </aside>
  );
}
