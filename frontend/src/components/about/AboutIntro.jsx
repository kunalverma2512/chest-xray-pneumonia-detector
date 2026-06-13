import { Activity } from 'lucide-react';

export default function AboutIntro() {
  return (
    <section className="section section-white min-h-screen flex flex-col justify-center">
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1.5rem', width: '100%' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr auto', gap: '5rem', alignItems: 'center' }}
          className="grid-cols-1 md:grid-cols-2"
        >
          <div>
            <span className="label mb-8 inline-flex">About</span>
            <h1 className="text-headline text-black mt-4">
              A clinical AI tool<br />built for real-world<br />screening.
            </h1>
            <p className="text-body text-muted mt-6 max-w-lg leading-relaxed">
              PneumoDetectAI is an open-source AI screening tool designed to assist clinicians
              and researchers in identifying pneumonia from pediatric chest X-rays.
              It is not intended to replace clinical judgment — but to augment it with
              a fast, calibrated, and transparent second opinion.
            </p>
            <p className="text-body text-muted mt-4 max-w-lg leading-relaxed">
              The model was trained on a balanced 1:1 dataset of 5,216 images,
              internally validated to 94.8% accuracy, and cross-operator validated on
              485 independent samples — achieving 82.7% accuracy and 97.6% sensitivity
              in real-world generalisation tests.
            </p>
          </div>

          <div
            style={{
              width: '200px',
              height: '200px',
              border: '1px solid var(--border)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
            }}
            className="hidden md:flex"
          >
            <Activity size={72} style={{ color: '#e5e5e5' }} strokeWidth={1} />
          </div>
        </div>
      </div>
    </section>
  );
}
