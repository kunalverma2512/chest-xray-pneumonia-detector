import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

const WORDS = ['AI-powered', 'Clinical-grade', 'Validated', 'Precise'];

export default function HeroSection() {
  const [wordIdx, setWordIdx] = useState(0);
  const [displayed, setDisplayed] = useState('');
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const target = WORDS[wordIdx];
    let timeout;
    if (!deleting && displayed.length < target.length) {
      timeout = setTimeout(() => setDisplayed(target.slice(0, displayed.length + 1)), 70);
    } else if (!deleting && displayed.length === target.length) {
      timeout = setTimeout(() => setDeleting(true), 2000);
    } else if (deleting && displayed.length > 0) {
      timeout = setTimeout(() => setDisplayed(displayed.slice(0, -1)), 40);
    } else {
      setDeleting(false);
      setWordIdx(i => (i + 1) % WORDS.length);
    }
    return () => clearTimeout(timeout);
  }, [displayed, deleting, wordIdx]);

  return (
    <section style={{
      minHeight: '100vh',
      width: '100%',
      background: '#fff',
      display: 'flex',
      alignItems: 'center',
      boxSizing: 'border-box',
      padding: '7rem 0 5rem',
    }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 1.5rem', width: '100%' }}>

        {/* Label */}
        <div className="animate-fade-up" style={{ marginBottom: '2rem' }}>
          <span className="label">Clinical AI · Pediatric Pneumonia Detection</span>
        </div>

        {/* Headline */}
        <h1
          className="animate-fade-up"
          style={{
            fontSize: 'clamp(2.75rem, 9vw, 7rem)',
            fontWeight: 900,
            letterSpacing: '-0.04em',
            lineHeight: 1.0,
            color: '#000',
            margin: 0,
            animationDelay: '0.1s',
          }}
        >
          <span style={{ color: '#aaa' }}>
            {displayed}
            <span className="cursor-blink">|</span>
          </span>
          <br />
          pneumonia
          <br />
          screening.
        </h1>

        {/* Subtext */}
        <p
          className="animate-fade-up"
          style={{
            fontSize: 'clamp(1rem, 2vw, 1.2rem)',
            fontWeight: 400,
            color: '#666',
            marginTop: '2rem',
            maxWidth: '520px',
            lineHeight: 1.7,
            animationDelay: '0.2s',
          }}
        >
          Upload a pediatric chest X-ray. Our deep learning model returns a
          diagnosis in seconds — validated on 485 independent samples with 97.6% sensitivity.
        </p>

        {/* CTAs */}
        <div
          className="animate-fade-up"
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '1rem',
            marginTop: '2.5rem',
            animationDelay: '0.3s',
          }}
        >
          <Link to="/upload" className="btn-primary">
            Analyse an X-Ray <ArrowRight size={18} />
          </Link>
          <Link to="/model-insights" className="btn-ghost">
            View Validation Metrics
          </Link>
        </div>

        {/* Metric strip */}
        <div
          className="animate-fade-up metric-strip"
          style={{
            marginTop: '5rem',
            paddingTop: '2.5rem',
            borderTop: '1px solid #e5e5e5',
            animationDelay: '0.4s',
          }}
        >
          {[
            { value: '82.7%', label: 'Cross-Operator Accuracy' },
            { value: '97.6%', label: 'Sensitivity (TPR)' },
            { value: '0.961', label: 'ROC-AUC' },
            { value: '485',   label: 'Validation Samples' },
          ].map(({ value, label }) => (
            <div key={label} style={{ minWidth: '100px' }}>
              <div style={{ fontSize: 'clamp(1.5rem, 4vw, 2.5rem)', fontWeight: 900, letterSpacing: '-0.03em', color: '#000' }}>
                {value}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '4px' }}>{label}</div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}
