import { useState, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import MobileNav from './MobileNav.jsx';

const NAV_LINKS = [
  { to: '/',               label: 'Home' },
  { to: '/upload',         label: 'Analyse X-Ray' },
  { to: '/model-insights', label: 'Model Insights' },
  { to: '/about',          label: 'About' },
  { to: '/faq',            label: 'FAQ' },
  { to: '/contact',        label: 'Contact' },
];

export default function Navbar() {
  const [scrolled, setScrolled]     = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isMobile, setIsMobile]     = useState(window.innerWidth < 768);
  const { pathname } = useLocation();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    const onResize = () => setIsMobile(window.innerWidth < 768);
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onResize, { passive: true });
    return () => {
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onResize);
    };
  }, []);

  useEffect(() => setMobileOpen(false), [pathname]);

  return (
    <>
      <header
        style={{
          position: 'fixed',
          top: 0, left: 0, right: 0,
          zIndex: 1000,
          background: 'rgba(255,255,255,0.97)',
          backdropFilter: 'blur(12px)',
          WebkitBackdropFilter: 'blur(12px)',
          borderBottom: scrolled ? '1px solid #e5e5e5' : '1px solid transparent',
          transition: 'border-color 0.3s ease',
        }}
      >
        <div
          style={{
            maxWidth: '1280px',
            margin: '0 auto',
            padding: '0 1.5rem',
            height: '64px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '1rem',
          }}
        >
          {/* ── Brand ── */}
          <NavLink
            to="/"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              textDecoration: 'none',
              flexShrink: 0,
            }}
          >
            <span
              style={{
                width: '30px',
                height: '30px',
                background: '#000',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0,
              }}
            >
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M1 7h2.5l2-4 3 8 2-4H13" stroke="white" strokeWidth="1.5" strokeLinecap="square"/>
              </svg>
            </span>
            <span
              style={{
                fontWeight: 800,
                fontSize: '0.9375rem',
                color: '#000',
                letterSpacing: '-0.02em',
                whiteSpace: 'nowrap',
                fontFamily: 'var(--font)',
              }}
            >
              PneumoDetect<span style={{ color: '#e11d48' }}>AI</span>
            </span>
          </NavLink>

          {/* ── Desktop Nav Links ── */}
          {!isMobile && (
            <nav
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '2px',
                flex: 1,
                justifyContent: 'center',
              }}
            >
              {NAV_LINKS.map(({ to, label }) => (
                <NavLink
                  key={to}
                  to={to}
                  end={to === '/'}
                  style={({ isActive }) => ({
                    display: 'inline-block',
                    padding: '6px 14px',
                    fontSize: '0.875rem',
                    fontWeight: 500,
                    textDecoration: 'none',
                    color: isActive ? '#000' : '#555',
                    background: isActive ? '#f2f2f2' : 'transparent',
                    transition: 'background 0.2s, color 0.2s',
                    whiteSpace: 'nowrap',
                    fontFamily: 'var(--font)',
                  })}
                  onMouseEnter={e => {
                    if (e.currentTarget.getAttribute('aria-current') !== 'page') {
                      e.currentTarget.style.background = '#000';
                      e.currentTarget.style.color = '#fff';
                    }
                  }}
                  onMouseLeave={e => {
                    const active = e.currentTarget.getAttribute('aria-current') === 'page';
                    e.currentTarget.style.background = active ? '#f2f2f2' : 'transparent';
                    e.currentTarget.style.color = active ? '#000' : '#555';
                  }}
                >
                  {label}
                </NavLink>
              ))}
            </nav>
          )}

          {/* ── Right Side ── */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexShrink: 0 }}>
            {/* Desktop CTA */}
            {!isMobile && (
              <NavLink
                to="/upload"
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  padding: '8px 20px',
                  background: '#000',
                  color: '#fff',
                  fontWeight: 700,
                  fontSize: '0.875rem',
                  textDecoration: 'none',
                  border: '2px solid #000',
                  transition: 'background 0.2s, color 0.2s',
                  whiteSpace: 'nowrap',
                  fontFamily: 'var(--font)',
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.background = '#fff';
                  e.currentTarget.style.color = '#000';
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.background = '#000';
                  e.currentTarget.style.color = '#fff';
                }}
              >
                Run Analysis
              </NavLink>
            )}

            {/* Mobile hamburger */}
            {isMobile && (
              <button
                onClick={() => setMobileOpen(v => !v)}
                aria-label="Toggle menu"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: '40px',
                  height: '40px',
                  background: 'none',
                  border: '1px solid #e5e5e5',
                  cursor: 'pointer',
                  color: '#000',
                }}
              >
                {mobileOpen ? <X size={20} /> : <Menu size={20} />}
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Mobile slide-down menu */}
      <MobileNav links={NAV_LINKS} open={mobileOpen && isMobile} onClose={() => setMobileOpen(false)} />
    </>
  );
}
