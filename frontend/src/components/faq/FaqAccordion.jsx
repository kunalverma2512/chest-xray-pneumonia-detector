import FaqItem from './FaqItem.jsx';

const FAQ_DATA = [
  {
    q: 'Is this tool approved for clinical use?',
    a: 'No. PneumoDetectAI is a research-grade screening assistant. It has not received FDA, CE, or equivalent regulatory clearance. All results must be reviewed by a qualified clinician before any clinical decision.',
  },
  {
    q: 'What image formats are accepted?',
    a: 'JPEG, PNG, and WebP up to 10 MB. The image is resized to 224 × 224 pixels server-side. Original resolution is not required, but better quality inputs generally yield higher confidence scores.',
  },
  {
    q: 'Are my images stored or logged?',
    a: 'No. Images are processed entirely in-memory by the FastAPI backend and are never persisted to disk or a database. The server holds the image only for the duration of the inference request.',
  },
  {
    q: 'What does "confidence level" mean?',
    a: 'Confidence level maps the raw sigmoid score to a human-readable tier: High (≥80%), Moderate (60–80%), or Low (<60%). A High-confidence PNEUMONIA result means the model assigns a >80% probability to the positive class.',
  },
  {
    q: 'What is cross-operator validation?',
    a: 'Cross-operator validation evaluates the model on 485 images collected by a different clinical operator than those who produced the training data. This tests real-world generalisation, simulating deployment to a new hospital or imaging system.',
  },
  {
    q: 'Why is sensitivity (97.6%) prioritised over specificity (66.7%)?',
    a: 'For pneumonia screening, false negatives (missed cases) are more dangerous than false positives (unnecessary follow-ups). A high sensitivity ensures the AI rarely misses a true pneumonia case, accepting a higher false-positive rate which clinicians review.',
  },
  {
    q: 'Can I run this locally?',
    a: 'Yes. The backend is a standard FastAPI service; clone the repository, install requirements.txt inside backend/, and run `uvicorn app.main:app --reload`. The frontend runs with `npm run dev` inside frontend/.',
  },
  {
    q: 'What model architecture is used?',
    a: 'MobileNetV2 pre-trained on ImageNet, with a custom classification head: GlobalAveragePooling2D → Dropout(0.3) → Dense(128, relu) → Dropout(0.2) → Dense(1, sigmoid). The base model is frozen during the initial training phase.',
  },
];

export default function FaqAccordion() {
  return (
    <div style={{ borderTop: '1px solid var(--border)' }}>
      {FAQ_DATA.map(({ q, a }) => (
        <FaqItem key={q} question={q} answer={a} />
      ))}
    </div>
  );
}
