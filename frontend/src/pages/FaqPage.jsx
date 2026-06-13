import MainLayout from '../layouts/MainLayout.jsx';
import FaqLayout from '../components/faq/FaqLayout.jsx';
import FaqAccordion from '../components/faq/FaqAccordion.jsx';

export default function FaqPage() {
 return (
 <MainLayout>
 <FaqLayout>
 <FaqAccordion />
 </FaqLayout>
 </MainLayout>
 );
}
