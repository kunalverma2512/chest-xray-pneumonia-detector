import { Upload, Cpu, FileText } from 'lucide-react';

const STEPS = [
  {
    n: '01',
    icon: <Upload size={28} />,
    title: 'Upload the X-Ray',
    body: 'Drag-and-drop or browse a JPEG/PNG chest X-ray. Max 10 MB. No PHI stored — images are processed in-memory only.',
  },
  {
    n: '02',
    icon: <Cpu size={28} />,
    title: 'AI Inference',
    body: 'MobileNetV2 (fine-tuned on 5,000+ balanced samples) runs inference with 224×224 resize and [0,1] normalisation.',
  },
  {
    n: '03',
    icon: <FileText size={28} />,
    title: 'Review the Report',
    body: 'Receive diagnosis (PNEUMONIA / NORMAL), a calibrated confidence score, clinical recommendation, and validation provenance.',
  },
];

export default function HowItWorksSection() {
  return (
    <section style={{
      minHeight: '100vh',
      width: '100%',
      background: '#fff',
      display: 'flex',
      alignItems: 'center',
      boxSizing: 'border-box',
      padding: '7rem 0',
    }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 1.5rem', width: '100%' }}>

        {/* Header */}
        <div style={{ marginBottom: '5rem' }}>
          <span className="label" style={{ marginBottom: '1.5rem', display: 'inline-flex' }}>How it works</span>
          <h2 style={{
            fontSize: 'clamp(2rem, 5vw, 3.5rem)',
            fontWeight: 800,
            letterSpacing: '-0.03em',
            color: '#000',
            margin: '1rem 0 1rem',
            lineHeight: 1.1,
          }}>
            From X-ray to insight<br />in three steps.
          </h2>
          <p style={{ fontSize: '1rem', color: '#777', maxWidth: '400px', lineHeight: 1.7, margin: 0 }}>
            No account, no waiting. The full pipeline runs server-side in under 2 seconds.
          </p>
        </div>

        {/* Steps grid */}
        <div className="steps-grid">
          {STEPS.map(({ n, icon, title, body }) => (
            <div key={n} style={{
              background: '#fff',
              padding: '3rem 2.5rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '1.5rem',
              boxSizing: 'border-box',
            }}>
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
                <div style={{ width: '56px', height: '56px', border: '1px solid #e5e5e5', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  {icon}
                </div>
                <span style={{ fontSize: '4rem', fontWeight: 900, color: '#f0f0f0', lineHeight: 1, userSelect: 'none' }}>{n}</span>
              </div>
              <div>
                <h3 style={{ fontWeight: 700, color: '#000', fontSize: '1.1rem', margin: '0 0 0.5rem 0' }}>{title}</h3>
                <p style={{ fontSize: '0.8125rem', color: '#777', lineHeight: 1.7, margin: 0 }}>{body}</p>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}
