import { ShieldCheck, Info, Clock } from 'lucide-react';
import { formatTimestamp } from '../../utils/formatters.js';

export default function PredictionDetails({ data }) {
  if (!data) return null;
  const { recommendation, external_validation_performance: xval, raw_score, filename, image_size, timestamp } = data;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      {/* Recommendation */}
      <div style={{ border: '1px solid var(--border)', padding: '1rem 1.25rem', display: 'flex', gap: '12px', background: '#fafafa' }}>
        <ShieldCheck size={18} style={{ color: '#000', flexShrink: 0, marginTop: '2px' }} />
        <div>
          <p style={{ fontSize: '0.75rem', fontWeight: 700, color: '#000', marginBottom: '4px', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
            Clinical Recommendation
          </p>
          <p style={{ fontSize: '0.8125rem', color: '#555', lineHeight: 1.6 }}>{recommendation}</p>
        </div>
      </div>

      {/* External validation provenance */}
      {xval && (
        <div style={{ border: '1px solid var(--border)', padding: '1rem 1.25rem' }}>
          <p style={{ fontSize: '0.75rem', fontWeight: 700, color: '#000', marginBottom: '1rem', textTransform: 'uppercase', letterSpacing: '0.06em', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Info size={14} />
            Cross-Operator Validation Provenance
          </p>
          <div className="grid grid-cols-2 gap-3">
            {[
              { label: 'Accuracy',     value: xval.accuracy },
              { label: 'Sensitivity',  value: xval.sensitivity },
              { label: 'Specificity',  value: xval.specificity },
              { label: 'Validated On', value: xval.validated_on },
            ].map(({ label, value }) => (
              <div key={label}>
                <p style={{ fontSize: '0.65rem', color: '#999', textTransform: 'uppercase', letterSpacing: '0.06em' }}>{label}</p>
                <p style={{ fontSize: '0.875rem', fontWeight: 700, color: '#000', marginTop: '2px' }}>{value}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Meta */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
        {filename   && <span style={{ fontSize: '0.75rem', color: '#999' }}>📄 {filename}</span>}
        {image_size && <span style={{ fontSize: '0.75rem', color: '#999' }}>📐 {image_size}</span>}
        {raw_score != null && <span style={{ fontSize: '0.75rem', color: '#999' }}>Score: {Number(raw_score).toFixed(4)}</span>}
        {timestamp  && (
          <span style={{ fontSize: '0.75rem', color: '#999', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Clock size={11} /> {formatTimestamp(timestamp)}
          </span>
        )}
      </div>
    </div>
  );
}
