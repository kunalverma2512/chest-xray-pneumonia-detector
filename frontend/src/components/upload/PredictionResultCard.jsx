import { Activity, AlertCircle } from 'lucide-react';
import Skeleton from '../ui/Skeleton.jsx';
import MetricChips from './MetricChips.jsx';
import PredictionDetails from './PredictionDetails.jsx';

export default function PredictionResultCard({ data, loading, error }) {
  return (
    <div style={{ border: '1px solid var(--border)', padding: '2rem', background: '#fff', minHeight: '420px', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <h2 style={{ fontWeight: 700, fontSize: '1rem', display: 'flex', alignItems: 'center', gap: '8px', color: '#000' }}>
        <Activity size={18} />
        Analysis Report
      </h2>

      {/* Loading */}
      {loading && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', flex: 1 }}>
          <Skeleton className="h-10 w-full" />
          <Skeleton className="h-20 w-full" />
          <Skeleton className="h-24 w-full" />
          <p style={{ fontSize: '0.75rem', color: '#999', textAlign: 'center' }}>Running AI inference…</p>
        </div>
      )}

      {/* Error */}
      {!loading && error && (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', flex: 1, gap: '1rem', textAlign: 'center' }}>
          <AlertCircle size={40} style={{ color: 'var(--red)' }} />
          <div>
            <p style={{ fontWeight: 600, color: '#000' }}>Analysis failed</p>
            <p style={{ fontSize: '0.8rem', color: '#999', marginTop: '4px' }}>{error}</p>
            <p style={{ margin: '0.25rem 0 0', fontSize: '0.8125rem', color: '#999' }}>
              Ensure the backend API is running and reachable.
            </p>
          </div>
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && !data && (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', flex: 1, gap: '1rem', textAlign: 'center', padding: '2rem 0' }}>
          <div style={{ width: '64px', height: '64px', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Activity size={28} style={{ color: '#ccc' }} />
          </div>
          <div>
            <p style={{ fontWeight: 600, color: '#000' }}>No analysis yet</p>
            <p style={{ fontSize: '0.8rem', color: '#999', marginTop: '4px' }}>
              Upload a chest X-ray and click <strong>Run AI Analysis</strong> to see results.
            </p>
          </div>
        </div>
      )}

      {/* Result */}
      {!loading && !error && data && (
        <div className="animate-fade-up" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {/* Diagnosis banner */}
          <div
            style={{
              padding: '1.5rem',
              textAlign: 'center',
              border: '1px solid',
              borderColor: data.diagnosis === 'PNEUMONIA' ? '#fecdd3' : '#e5e5e5',
              background: data.diagnosis === 'PNEUMONIA' ? '#fff1f2' : '#fafafa',
            }}
          >
            <p style={{ fontSize: '0.7rem', color: '#999', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '6px' }}>AI Diagnosis</p>
            <p
              style={{
                fontSize: '2rem',
                fontWeight: 900,
                letterSpacing: '-0.03em',
                color: data.diagnosis === 'PNEUMONIA' ? 'var(--red)' : '#000',
              }}
            >
              {data.diagnosis}
            </p>
          </div>

          <MetricChips data={data} />
          <PredictionDetails data={data} />
        </div>
      )}
    </div>
  );
}
