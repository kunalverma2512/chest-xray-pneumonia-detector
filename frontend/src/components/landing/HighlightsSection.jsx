import { Zap, ShieldCheck, BarChart2, Clock } from 'lucide-react';

const HIGHLIGHTS = [
  {
    icon: <Zap size={20} />,
    title: 'Instant Inference',
    body: 'Upload a JPEG or PNG chest X-ray and receive a prediction in under 2 seconds. No registration required.',
  },
  {
    icon: <ShieldCheck size={20} />,
    title: 'Cross-Operator Validated',
    body: '485 independent samples from a distinct operator cohort. 82.7% accuracy with a 97.6% sensitivity rate.',
  },
  {
    icon: <BarChart2 size={20} />,
    title: 'Transparent Metrics',
    body: 'Every prediction ships with raw confidence score and full cross-operator validation provenance.',
  },
  {
    icon: <Clock size={20} />,
    title: 'Clinician-First Design',
    body: 'Clean JSON API ready for EHR integration. Open React frontend for rapid clinical workflow prototyping.',
  },
];

export default function HighlightsSection() {
  return (
    <section style={{ width: '100%', background: '#f9f9f9', padding: '0', boxSizing: 'border-box' }}>
      <div className="highlights-grid" style={{ borderTop: '1px solid #e5e5e5', borderBottom: '1px solid #e5e5e5' }}>
        {HIGHLIGHTS.map(({ icon, title, body }) => (
          <div
            key={title}
            style={{
              background: '#fff',
              padding: '3rem 2.5rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '1.25rem',
              borderRight: '1px solid #e5e5e5',
              borderBottom: '1px solid #e5e5e5',
              boxSizing: 'border-box',
            }}
          >
            <div style={{ width: '40px', height: '40px', border: '1px solid #e5e5e5', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              {icon}
            </div>
            <div>
              <h3 style={{ fontWeight: 700, color: '#000', fontSize: '1rem', margin: '0 0 8px 0' }}>{title}</h3>
              <p style={{ fontSize: '0.8125rem', color: '#777', lineHeight: 1.7, margin: 0 }}>{body}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
