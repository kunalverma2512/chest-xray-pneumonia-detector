export default function FaqLayout({ children }) {
  return (
    <section className="section section-white min-h-screen">
      <div style={{ maxWidth: '760px', margin: '0 auto', padding: '0 1.5rem' }}>
        <div style={{ marginBottom: '4rem' }}>
          <span className="label mb-6 inline-flex">FAQ</span>
          <h1 className="text-headline text-black mt-4">
            Frequently asked<br />questions.
          </h1>
          <p className="text-body text-muted mt-4">
            Everything you need to know about PneumoDetectAI and how it works.
          </p>
        </div>
        {children}
      </div>
    </section>
  );
}
