const METRICS = [
  { value: '82.7%', label: 'Cross-Operator Accuracy',  sub: '485 independent samples' },
  { value: '97.6%', label: 'Sensitivity (Recall)',      sub: 'Pneumonia detection rate' },
  { value: '66.7%', label: 'Specificity (TNR)',          sub: 'True normal detection' },
  { value: '75.9%', label: 'Precision (PPV)',            sub: 'Positive predictive value' },
  { value: '0.854', label: 'F1 Score',                  sub: 'Harmonic mean P & R' },
  { value: '0.961', label: 'ROC-AUC',                   sub: 'Area under ROC curve' },
];

export default function MetricsSection() {
  return (
    <section style={{
      minHeight: '100vh',
      width: '100%',
      background: '#000',
      display: 'flex',
      alignItems: 'center',
      boxSizing: 'border-box',
      padding: '7rem 0',
    }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 1.5rem', width: '100%' }}>

        {/* Header */}
        <div style={{ marginBottom: '4rem' }}>
          <span className="label label-inverted" style={{ marginBottom: '1.5rem', display: 'inline-flex' }}>Performance</span>
          <h2 style={{
            fontSize: 'clamp(2rem, 5vw, 3.5rem)',
            fontWeight: 800,
            letterSpacing: '-0.03em',
            color: '#fff',
            margin: '1rem 0 1rem',
            lineHeight: 1.1,
          }}>
            Rigorously validated.<br />Honestly reported.
          </h2>
          <p style={{ fontSize: '1rem', color: '#777', maxWidth: '450px', lineHeight: 1.7, margin: 0 }}>
            Evaluated on a held-out cross-operator cohort — fully separate from training —
            to simulate real-world clinical deployment.
          </p>
        </div>

        {/* Metrics grid */}
        <div className="metrics-grid">
          {METRICS.map(({ value, label, sub }) => (
            <div key={label} style={{ background: '#111', padding: '2.5rem', display: 'flex', flexDirection: 'column', gap: '6px', boxSizing: 'border-box' }}>
              <span style={{ fontSize: 'clamp(1.75rem, 4vw, 2.75rem)', fontWeight: 900, letterSpacing: '-0.03em', color: '#fff' }}>
                {value}
              </span>
              <span style={{ fontSize: '0.875rem', fontWeight: 600, color: '#ccc' }}>{label}</span>
              <span style={{ fontSize: '0.75rem', color: '#555' }}>{sub}</span>
            </div>
          ))}
        </div>

        <p style={{ fontSize: '0.75rem', color: '#444', marginTop: '2rem' }}>
          * Cross-operator validation on 485 independent pediatric chest X-ray samples.
          Internal validation accuracy: 94.8%.
        </p>
      </div>
    </section>
  );
}
