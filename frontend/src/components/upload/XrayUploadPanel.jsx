import { useRef, useState, useCallback } from 'react';
import { Upload, ImageIcon, X, FileSearch } from 'lucide-react';
import Button from '../ui/Button.jsx';
import { formatFileSize } from '../../utils/formatters.js';

const ACCEPTED = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
const MAX_BYTES = 10 * 1024 * 1024;

export default function XrayUploadPanel({ onUpload, loading }) {
  const inputRef = useRef(null);
  const [file, setFile]     = useState(null);
  const [preview, setPrev]  = useState(null);
  const [dragOver, setDrag] = useState(false);
  const [fileErr, setErr]   = useState('');

  const handleFile = useCallback((f) => {
    setErr('');
    if (!f) return;
    if (!ACCEPTED.includes(f.type)) { setErr('Please upload a JPEG, PNG, or WebP image.'); return; }
    if (f.size > MAX_BYTES)         { setErr('File exceeds 10 MB limit.'); return; }
    setFile(f);
    setPrev(URL.createObjectURL(f));
  }, []);

  const onDrop      = useCallback((e) => { e.preventDefault(); setDrag(false); handleFile(e.dataTransfer.files?.[0]); }, [handleFile]);
  const onDragOver  = (e) => { e.preventDefault(); setDrag(true); };
  const onDragLeave = () => setDrag(false);

  const clear = () => {
    setFile(null); setPrev(null); setErr('');
    if (inputRef.current) inputRef.current.value = '';
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file && !loading) onUpload(file);
  };

  return (
    <div style={{ border: '1px solid var(--border)', padding: '2rem', background: '#fff' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
        <h2 style={{ fontWeight: 700, fontSize: '1rem', display: 'flex', alignItems: 'center', gap: '8px', color: '#000' }}>
          <ImageIcon size={18} />
          Upload X-Ray Image
        </h2>
        {file && (
          <button
            onClick={clear}
            style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#999' }}
          >
            <X size={18} />
          </button>
        )}
      </div>

      {/* Drop zone */}
      <div
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onClick={() => !file && inputRef.current?.click()}
        className={`drop-zone ${dragOver ? 'active' : ''}`}
        style={{
          minHeight: '240px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: file ? 'default' : 'pointer',
          marginBottom: '1rem',
        }}
      >
        {preview ? (
          <img src={preview} alt="X-ray preview" style={{ maxHeight: '240px', maxWidth: '100%', objectFit: 'contain' }} />
        ) : (
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <div style={{ width: '56px', height: '56px', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1rem' }}>
              <Upload size={24} style={{ color: '#999' }} />
            </div>
            <p style={{ fontWeight: 500, color: '#000', fontSize: '0.9rem' }}>
              Drop X-ray here or{' '}
              <span style={{ textDecoration: 'underline', textDecorationStyle: 'dashed' }}>browse</span>
            </p>
            <p style={{ fontSize: '0.75rem', color: '#999', marginTop: '4px' }}>JPEG, PNG, WebP — max 10 MB</p>
          </div>
        )}
      </div>

      <input
        ref={inputRef}
        type="file"
        accept={ACCEPTED.join(',')}
        style={{ display: 'none' }}
        onChange={(e) => handleFile(e.target.files?.[0])}
      />

      {file && (
        <div style={{ border: '1px solid var(--border)', padding: '0.75rem', display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '1rem', background: '#fafafa' }}>
          <FileSearch size={15} style={{ color: '#555', flexShrink: 0 }} />
          <div style={{ flex: 1, minWidth: 0 }}>
            <p style={{ fontSize: '0.8rem', fontWeight: 600, color: '#000', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{file.name}</p>
            <p style={{ fontSize: '0.75rem', color: '#999' }}>{formatFileSize(file.size)}</p>
          </div>
        </div>
      )}

      {fileErr && <p style={{ fontSize: '0.8rem', color: 'var(--red)', marginBottom: '0.75rem' }}>{fileErr}</p>}

      <Button onClick={handleSubmit} disabled={!file || loading} className="w-full justify-center">
        {loading ? (
          <>
            <span style={{ width: '16px', height: '16px', border: '2px solid currentColor', borderTopColor: 'transparent', display: 'inline-block', animation: 'spin 0.7s linear infinite' }} />
            Analysing…
          </>
        ) : 'Run AI Analysis'}
      </Button>
    </div>
  );
}
