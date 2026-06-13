export default function ContactLayout({ children }) {
  return (
    <section className="section section-white min-h-screen">
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1.5rem' }}>
        <div style={{ marginBottom: '4rem' }}>
          <span className="label mb-6 inline-flex">Contact</span>
          <h1 className="text-headline text-black mt-4">
            Get in touch.
          </h1>
          <p className="text-body text-muted mt-4 max-w-lg">
            Have a clinical question, integration inquiry, or want to collaborate?
            We respond within 48 hours.
          </p>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8 items-start">
          {children}
        </div>
      </div>
    </section>
  );
}
