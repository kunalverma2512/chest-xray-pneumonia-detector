export default function UploadLayout({ children }) {
  return (
    <section className="section section-white min-h-screen">
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1.5rem' }}>
        <div style={{ marginBottom: '3rem' }}>
          <span className="label mb-6 inline-flex">AI Screening Tool</span>
          <h1 className="text-headline text-black mt-4">
            Chest X-Ray Analysis.
          </h1>
          <p className="text-body text-muted mt-4 max-w-lg">
            Upload a pediatric chest X-ray (JPEG / PNG, ≤ 10 MB) to receive an
            AI-powered pneumonia screening report.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          {children}
        </div>

        <div
          style={{
            marginTop: '2.5rem',
            padding: '1.25rem 1.5rem',
            background: '#fafafa',
            border: '1px solid var(--border)',
          }}
        >
          <p style={{ fontSize: '0.8125rem', color: '#666' }}>
            ⚠ This tool is for <strong style={{ color: '#000' }}>preliminary screening only</strong>.
            Results must be reviewed by a qualified clinician before any clinical decision.
            No images are stored server-side.
          </p>
        </div>
      </div>
    </section>
  );
}
