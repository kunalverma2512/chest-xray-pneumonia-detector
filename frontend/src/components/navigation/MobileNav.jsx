import { NavLink } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

export default function MobileNav({ links, open, onClose }) {
  return (
    <>
      {/* Backdrop */}
      <div
        onClick={onClose}
        style={{
          position: 'fixed',
          inset: 0,
          zIndex: 999,
          background: 'rgba(0,0,0,0.25)',
          opacity: open ? 1 : 0,
          pointerEvents: open ? 'auto' : 'none',
          transition: 'opacity 0.25s ease',
        }}
      />

      {/* Slide-down panel */}
      <div
        style={{
          position: 'fixed',
          top: '64px',
          left: 0,
          right: 0,
          zIndex: 1000,
          background: '#fff',
          borderBottom: '1px solid #e5e5e5',
          boxShadow: '0 8px 24px rgba(0,0,0,0.08)',
          opacity: open ? 1 : 0,
          transform: open ? 'translateY(0)' : 'translateY(-12px)',
          pointerEvents: open ? 'auto' : 'none',
          transition: 'opacity 0.25s ease, transform 0.25s ease',
        }}
      >
        {/* Nav links */}
        <nav style={{ padding: '0.75rem 1.5rem' }}>
          {links.map(({ to, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              onClick={onClose}
              style={({ isActive }) => ({
                display: 'flex',
                alignItems: 'center',
                padding: '0.875rem 0',
                borderBottom: '1px solid #f0f0f0',
                fontSize: '0.9375rem',
                fontWeight: isActive ? 700 : 500,
                color: isActive ? '#000' : '#555',
                textDecoration: 'none',
                fontFamily: 'var(--font)',
                transition: 'color 0.2s',
              })}
            >
              <span
                style={{
                  width: '6px',
                  height: '6px',
                  background: '#000',
                  display: 'inline-block',
                  marginRight: '14px',
                  flexShrink: 0,
                  opacity: 0,
                }}
              />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* CTA */}
        <div style={{ padding: '1rem 1.5rem', borderTop: '1px solid #e5e5e5' }}>
          <NavLink
            to="/upload"
            onClick={onClose}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              width: '100%',
              padding: '0.875rem',
              background: '#000',
              color: '#fff',
              fontWeight: 700,
              fontSize: '0.9375rem',
              textDecoration: 'none',
              border: '2px solid #000',
              fontFamily: 'var(--font)',
            }}
          >
            Run Analysis <ArrowRight size={16} />
          </NavLink>
        </div>
      </div>
    </>
  );
}
