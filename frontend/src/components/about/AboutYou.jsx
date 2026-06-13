import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

const AUDIENCES = [
  {
    role: 'Clinicians & Radiologists',
    desc: 'Use the upload tool as a rapid second opinion on chest X-rays. The model flags high-risk cases for prioritised human review.',
  },
  {
    role: 'Hospital Administrators',
    desc: 'Evaluate AI-augmented triage workflows. Assess sensitivity/specificity trade-offs for your patient population.',
  },
  {
    role: 'ML Researchers',
    desc: 'Explore cross-operator validation methodology, model architecture, and training pipeline via the open-source repository.',
  },
];

export default function AboutYou() {
  return (
    <section className="section section-white">
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1.5rem' }}>
        <div style={{ marginBottom: '3rem' }}>
          <span className="label mb-6 inline-flex">Audiences</span>
          <h2 className="text-headline text-black mt-4">Who is this for?</h2>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1px', background: 'var(--border)' }}>
          {AUDIENCES.map(({ role, desc }) => (
            <div
              key={role}
              style={{
                background: '#fff',
                padding: '2rem 2.5rem',
                display: 'grid',
                gridTemplateColumns: '220px 1fr',
                gap: '3rem',
                alignItems: 'start',
              }}
              className="grid-cols-1 sm:grid-cols-2"
            >
              <p style={{ fontWeight: 700, color: '#000', fontSize: '0.95rem' }}>{role}</p>
              <p style={{ fontSize: '0.875rem', color: '#666', lineHeight: 1.7 }}>{desc}</p>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div
          style={{
            marginTop: '4rem',
            background: '#000',
            padding: '3rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem',
            alignItems: 'flex-start',
          }}
          className="sm:flex-row sm:items-center sm:justify-between"
        >
          <div>
            <p style={{ fontWeight: 700, fontSize: '1.25rem', color: '#fff' }}>Ready to start?</p>
            <p style={{ fontSize: '0.875rem', color: '#888', marginTop: '4px' }}>Upload a chest X-ray for AI analysis — free and instant.</p>
          </div>
          <Link
            to="/upload"
            className="btn-primary"
            style={{ background: '#fff', color: '#000', borderColor: '#fff', flexShrink: 0 }}
          >
            Run an X-Ray Analysis <ArrowRight size={16} />
          </Link>
        </div>
      </div>
    </section>
  );
}
