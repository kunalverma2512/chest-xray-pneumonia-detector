export default function Input({ label, error, className = '', ...props }) {
 return (
 <div className="flex flex-col gap-1.5">
 {label && (
 <label className="text-caption text-muted font-medium uppercase tracking-wider">
 {label}
 </label>
 )}
 <input
 className={`w-full bg-[var(--clr-surface-2)] border border-[var(--clr-border)] px-4 py-2.5
 text-[var(--clr-text)] placeholder:text-[var(--clr-muted)] text-sm
 focus:border-[var(--clr-teal)] focus:outline-none transition-colors
 ${error ? 'border-rose-500' : ''} ${className}`}
 {...props}
 />
 {error && <p className="text-caption text-rose-400">{error}</p>}
 </div>
 );
}
