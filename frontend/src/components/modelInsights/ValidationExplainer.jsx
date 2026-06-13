const EXPLAINERS = [
  {
    title: 'What is cross-operator validation?',
    body: `Cross-operator validation tests the model on data collected by a different clinical operator than those who produced the training set. This is a stronger test of generalisation than standard train/test splits — it simulates deploying the model to a new hospital, scanner, or radiologist.`,
  },
  {
    title: 'Why prioritise sensitivity over specificity?',
    body: `For a pneumonia screening tool, the cost of a false negative (missed diagnosis) vastly exceeds the cost of a false positive (unnecessary follow-up). A 97.6% sensitivity means the model misses only about 2.4% of true pneumonia cases. The 33.3% false-positive rate is acceptable in a screening context where all positives receive human review.`,
  },
  {
    title: 'How should the confidence score be interpreted?',
    body: `The confidence score is the raw sigmoid output. For PNEUMONIA predictions, it represents the model's estimated probability that the X-ray is pneumonia-positive. Scores above 80% are classified as "High" confidence, 60–80% as "Moderate", and below 60% as "Low".`,
  },
  {
    title: 'Internal vs. cross-operator performance',
    body: `Internal validation (held-out test split from the same distribution) achieved 94.8% accuracy. Cross-operator validation dropped accuracy to 82.7% — a 12.1% generalisation gap. This is within the expected range for a model trained without domain adaptation or multi-site data augmentation.`,
  },
];

export default function ValidationExplainer() {
  return (
    <div>
      <h2 className="text-heading text-black mb-8">
        Understanding the validation methodology
      </h2>
      <div
        className="grid grid-cols-1 md:grid-cols-2 gap-px"
        style={{ background: 'var(--border)' }}
      >
        {EXPLAINERS.map(({ title, body }) => (
          <div
            key={title}
            style={{
              background: '#fff',
              padding: '2rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.75rem',
            }}
          >
            <h3 style={{ fontWeight: 700, fontSize: '0.95rem', color: '#000' }}>{title}</h3>
            <p style={{ fontSize: '0.8125rem', color: '#666', lineHeight: 1.7 }}>{body}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
