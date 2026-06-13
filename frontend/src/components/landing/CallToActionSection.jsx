import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

export default function CallToActionSection() {
  return (
    <section style={{
      minHeight: '60vh',
      width: '100%',
      background: '#000',
      display: 'flex',
      alignItems: 'center',
      boxSizing: 'border-box',
      padding: '7rem 0',
    }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 1.5rem', width: '100%' }}>

        <div style={{ maxWidth: '640px' }}>
          <h2 style={{
            fontSize: 'clamp(2rem, 5vw, 3.5rem)',
            fontWeight: 800,
            letterSpacing: '-0.03em',
            color: '#fff',
            margin: '0 0 1.5rem 0',
            lineHeight: 1.1,
          }}>
            Start screening<br />in seconds.
          </h2>
          <p style={{ fontSize: '1.1rem', color: '#888', lineHeight: 1.7, margin: '0 0 2.5rem 0' }}>
            No account required. Upload a chest X-ray and receive a clinical AI report
            with diagnosis, confidence, and full validation provenance — free, open, and instant.
          </p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
            <Link
              to="/upload"
              className="btn-primary"
              style={{ background: '#fff', color: '#000', borderColor: '#fff' }}
            >
              Analyse an X-Ray <ArrowRight size={18} />
            </Link>
            <Link
              to="/about"
              className="btn-ghost"
              style={{ color: '#999', borderColor: '#333' }}
            >
              Learn More
            </Link>
          </div>
        </div>

      </div>
    </section>
  );
}
