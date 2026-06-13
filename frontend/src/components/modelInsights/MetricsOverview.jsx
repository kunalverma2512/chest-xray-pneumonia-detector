const OVERVIEW = [
  { label: 'Accuracy',           value: '82.7%', note: '485 independent samples', important: false },
  { label: 'Sensitivity (TPR)',  value: '97.6%', note: '9 false negatives / 251 positive', important: true },
  { label: 'Specificity (TNR)',  value: '66.7%', note: '78 false positives / 234 normal', important: false },
  { label: 'Precision (PPV)',    value: '75.9%', note: '242 true positives', important: false },
  { label: 'F1 Score',           value: '0.854', note: 'Harmonic mean of P & R', important: false },
  { label: 'False Positive Rate','value': '33.3%', note: 'FP / (FP + TN)', important: false },
  { label: 'False Negative Rate','value': '3.6%',  note: 'FN / (FN + TP)', important: false },
  { label: 'ROC-AUC',           value: '0.961', note: 'Excellent discrimination', important: true },
];

export default function MetricsOverview() {
  return (
    <div>
      <h2 className="text-heading text-black mb-8">
        Cross-Operator Validation Metrics
      </h2>

      <div
        className="grid grid-cols-2 md:grid-cols-4 gap-px"
        style={{ background: 'var(--border)' }}
      >
        {OVERVIEW.map(({ label, value, note, important }) => (
          <div
            key={label}
            style={{
              background: important ? '#000' : '#fff',
              padding: '1.5rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '4px',
            }}
          >
            <span
              style={{
                fontSize: '1.75rem',
                fontWeight: 900,
                letterSpacing: '-0.03em',
                color: important ? '#fff' : '#000',
              }}
            >
              {value}
            </span>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: important ? '#ccc' : '#333' }}>
              {label}
            </span>
            <span style={{ fontSize: '0.7rem', color: important ? '#666' : '#999' }}>
              {note}
            </span>
          </div>
        ))}
      </div>

      {/* Confusion Matrix */}
      <div style={{ marginTop: '2.5rem', border: '1px solid var(--border)', padding: '2rem' }}>
        <h3 className="font-bold text-black mb-6">Confusion Matrix (n=485)</h3>
        <div className="grid grid-cols-2 gap-px max-w-sm" style={{ background: 'var(--border)' }}>
          {[
            { label: 'True Negatives (TN)',  value: 156, good: true },
            { label: 'False Positives (FP)', value: 78,  good: false },
            { label: 'False Negatives (FN)', value: 6,   good: true },
            { label: 'True Positives (TP)',  value: 245, good: true },
          ].map(({ label, value, good }) => (
            <div
              key={label}
              style={{
                background: '#fff',
                padding: '1rem',
                textAlign: 'center',
              }}
            >
              <p style={{ fontSize: '1.5rem', fontWeight: 900, color: good ? '#000' : 'var(--red)' }}>{value}</p>
              <p style={{ fontSize: '0.65rem', color: '#999', textTransform: 'uppercase', letterSpacing: '0.06em', marginTop: '4px' }}>
                {label}
              </p>
            </div>
          ))}
        </div>
        <p className="text-caption text-muted mt-4">
          * Numbers are approximate from cross-operator validation results. Sensitivity = TP/(TP+FN) = 245/251 = 97.6%.
          Specificity = TN/(TN+FP) = 156/234 = 66.7%.
        </p>
      </div>
    </div>
  );
}
