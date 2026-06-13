/**
 * Format a float confidence value to a percent string.
 * Input: 94.32 →"94.3%"
 */
export function formatConfidence(value) {
 if (value == null) return '—';
 return `${Number(value).toFixed(1)}%`;
}

/**
 * Map confidence_level string to a CSS badge variant class.
 */
export function confidenceLevelBadge(level) {
 const map = { High: 'badge-green', Moderate: 'badge-amber', Low: 'badge-rose' };
 return map[level] || 'badge-indigo';
}

/**
 * Map diagnosis to badge variant.
 */
export function diagnosisBadge(diagnosis) {
 return diagnosis === 'PNEUMONIA' ? 'badge-rose' : 'badge-teal';
}

/**
 * Return a short date/time string from an ISO timestamp.
 */
export function formatTimestamp(ts) {
 if (!ts) return '';
 try {
 return new Date(ts).toLocaleString('en-US', {
 month: 'short', day: 'numeric', year: 'numeric',
 hour: '2-digit', minute: '2-digit',
 });
 } catch {
 return ts;
 }
}

/**
 * Human-readable file size.
 */
export function formatFileSize(bytes) {
 if (!bytes) return '';
 if (bytes < 1024) return `${bytes} B`;
 if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
 return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}
