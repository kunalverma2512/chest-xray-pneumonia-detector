const SPECS = [
  { label: 'Architecture',  value: 'MobileNetV2 + custom classification head' },
  { label: 'Input Size',    value: '224 × 224 RGB — rescaled to [0,1]' },
  { label: 'Training Data', value: 'Balanced 1:1 dataset (Normal : Pneumonia)' },
  { label: 'Loss Function', value: 'Binary cross-entropy' },
  { label: 'Optimiser',     value: 'Adam — lr=0.001, cosine decay' },
  { label: 'Callbacks',     value: 'EarlyStopping (patience=7), ReduceLROnPlateau' },
  { label: 'Output',        value: 'Sigmoid scalar — threshold 0.5' },
  { label: 'Framework',     value: 'TensorFlow / Keras 2.x · macOS-compatible' },
];

export default function AboutModel() {
  return (
    <section className="section section-black">
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1.5rem' }}>
        <div style={{ marginBottom: '3rem' }}>
          <span className="label label-inverted mb-6 inline-flex">Architecture</span>
          <h2 className="text-headline mt-4" style={{ color: '#fff' }}>
            Model technical<br />specification.
          </h2>
        </div>

        <div
          className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-px"
          style={{ background: '#222' }}
        >
          {SPECS.map(({ label, value }) => (
            <div key={label} style={{ background: '#111', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <p style={{ fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: '#555' }}>{label}</p>
              <p style={{ fontSize: '0.875rem', fontWeight: 600, color: '#ccc', lineHeight: 1.5 }}>{value}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
