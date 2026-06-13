import MainLayout from '../layouts/MainLayout.jsx';
import ContactLayout from '../components/contact/ContactLayout.jsx';
import ContactForm from '../components/contact/ContactForm.jsx';
import ContactInfo from '../components/contact/ContactInfo.jsx';

export default function ContactPage() {
 return (
 <MainLayout>
 <ContactLayout>
 <ContactForm />
 <ContactInfo />
 </ContactLayout>
 </MainLayout>
 );
}
