export default function Button({ children, variant = 'primary', className = '', ...props }) {
  const cls = variant === 'primary'
    ? 'btn-primary'
    : variant === 'danger'
    ? 'btn-danger'
    : 'btn-ghost';

  return (
    <button className={`${cls} ${className}`} {...props}>
      {children}
    </button>
  );
}
