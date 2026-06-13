export default function InsightsLayout({ children }) {
  return (
    <section className="section section-white">
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1.5rem' }}>
        <div style={{ marginBottom: '4rem' }}>
          <span className="label mb-6 inline-flex">Model Insights</span>
          <h1 className="text-headline text-black mt-4">
            Validation performance<br />&amp; clinical metrics.
          </h1>
          <p className="text-body text-muted mt-4 max-w-lg">
            A complete breakdown of how the model performs on internal and
            cross-operator validation cohorts.
          </p>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '5rem' }}>
          {children}
        </div>
      </div>
    </section>
  );
}
