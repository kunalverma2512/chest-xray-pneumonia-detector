import { useState } from 'react';
import { CheckCircle } from 'lucide-react';

export default function ContactForm() {
  const [form, setForm] = useState({ name: '', email: '', subject: '', message: '' });
  const [errors, setErrors] = useState({});
  const [submitted, setSub] = useState(false);

  const validate = () => {
    const e = {};
    if (!form.name.trim())        e.name    = 'Name is required.';
    if (!form.email.includes('@')) e.email   = 'Enter a valid email address.';
    if (!form.message.trim())      e.message = 'Message cannot be empty.';
    return e;
  };

  const handleChange = (field) => (e) => {
    setForm(f => ({ ...f, [field]: e.target.value }));
    setErrors(er => ({ ...er, [field]: '' }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const e2 = validate();
    if (Object.keys(e2).length) { setErrors(e2); return; }
    setSub(true);
  };

  if (submitted) {
    return (
      <div
        className="lg:col-span-3"
        style={{
          border: '1px solid var(--border)',
          padding: '4rem 2.5rem',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '1.5rem',
          textAlign: 'center',
          minHeight: '360px',
        }}
      >
        <CheckCircle size={48} style={{ color: '#000' }} strokeWidth={1.5} />
        <div>
          <h2 style={{ fontWeight: 700, color: '#000', fontSize: '1.25rem' }}>Message sent!</h2>
          <p style={{ fontSize: '0.875rem', color: '#666', marginTop: '8px' }}>
            Thanks for reaching out. We'll respond to <strong>{form.email}</strong> within 48 hours.
          </p>
        </div>
        <button
          onClick={() => { setSub(false); setForm({ name: '', email: '', subject: '', message: '' }); }}
          style={{ fontSize: '0.8125rem', color: '#999', background: 'none', border: 'none', cursor: 'pointer', textDecoration: 'underline' }}
        >
          Send another message
        </button>
      </div>
    );
  }

  const fieldStyle = (err) => ({
    width: '100%',
    padding: '0.875rem 1rem',
    border: `1px solid ${err ? 'var(--red)' : 'var(--border)'}`,
    background: '#fff',
    color: '#000',
    fontSize: '0.9375rem',
    fontFamily: 'var(--font)',
    outline: 'none',
    transition: 'border-color 0.2s',
  });

  const labelStyle = {
    display: 'block',
    fontSize: '0.7rem',
    fontWeight: 700,
    letterSpacing: '0.08em',
    textTransform: 'uppercase',
    color: '#666',
    marginBottom: '6px',
  };

  return (
    <form
      onSubmit={handleSubmit}
      noValidate
      className="lg:col-span-3"
      style={{ border: '1px solid var(--border)', padding: '2.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}
    >
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label style={labelStyle}>Full name</label>
          <input
            style={fieldStyle(errors.name)}
            placeholder="Dr. Jane Smith"
            value={form.name}
            onChange={handleChange('name')}
            onFocus={e => e.target.style.borderColor = '#000'}
            onBlur={e => e.target.style.borderColor = errors.name ? 'var(--red)' : 'var(--border)'}
          />
          {errors.name && <p style={{ fontSize: '0.75rem', color: 'var(--red)', marginTop: '4px' }}>{errors.name}</p>}
        </div>
        <div>
          <label style={labelStyle}>Email address</label>
          <input
            type="email"
            style={fieldStyle(errors.email)}
            placeholder="jane@hospital.org"
            value={form.email}
            onChange={handleChange('email')}
            onFocus={e => e.target.style.borderColor = '#000'}
            onBlur={e => e.target.style.borderColor = errors.email ? 'var(--red)' : 'var(--border)'}
          />
          {errors.email && <p style={{ fontSize: '0.75rem', color: 'var(--red)', marginTop: '4px' }}>{errors.email}</p>}
        </div>
      </div>

      <div>
        <label style={labelStyle}>Subject</label>
        <input
          style={fieldStyle(false)}
          placeholder="Integration inquiry / clinical question / other"
          value={form.subject}
          onChange={handleChange('subject')}
          onFocus={e => e.target.style.borderColor = '#000'}
          onBlur={e => e.target.style.borderColor = 'var(--border)'}
        />
      </div>

      <div>
        <label style={labelStyle}>Message</label>
        <textarea
          rows={6}
          style={{ ...fieldStyle(errors.message), resize: 'vertical' }}
          placeholder="Describe your question or use case…"
          value={form.message}
          onChange={handleChange('message')}
          onFocus={e => e.target.style.borderColor = '#000'}
          onBlur={e => e.target.style.borderColor = errors.message ? 'var(--red)' : 'var(--border)'}
        />
        {errors.message && <p style={{ fontSize: '0.75rem', color: 'var(--red)', marginTop: '4px' }}>{errors.message}</p>}
      </div>

      <button type="submit" className="btn-primary self-start px-10">
        Send Message
      </button>
    </form>
  );
}
