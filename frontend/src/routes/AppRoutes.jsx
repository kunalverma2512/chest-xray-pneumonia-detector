import { Routes, Route } from 'react-router-dom';
import LandingPage from '../pages/LandingPage.jsx';
import UploadPage from '../pages/UploadPage.jsx';
import AboutPage from '../pages/AboutPage.jsx';
import FaqPage from '../pages/FaqPage.jsx';
import ContactPage from '../pages/ContactPage.jsx';
import ModelInsightsPage from '../pages/ModelInsightsPage.jsx';

export default function AppRoutes() {
 return (
 <Routes>
 <Route path="/"element={<LandingPage />} />
 <Route path="/upload"element={<UploadPage />} />
 <Route path="/about"element={<AboutPage />} />
 <Route path="/faq"element={<FaqPage />} />
 <Route path="/contact"element={<ContactPage />} />
 <Route path="/model-insights"element={<ModelInsightsPage />} />
 </Routes>
 );
}
