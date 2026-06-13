import MainLayout from '../layouts/MainLayout.jsx';
import HeroSection from '../components/landing/HeroSection.jsx';
import HighlightsSection from '../components/landing/HighlightsSection.jsx';
import HowItWorksSection from '../components/landing/HowItWorksSection.jsx';
import MetricsSection from '../components/landing/MetricsSection.jsx';
import TrustSignalsSection from '../components/landing/TrustSignalsSection.jsx';
import CallToActionSection from '../components/landing/CallToActionSection.jsx';

export default function LandingPage() {
 return (
 <MainLayout>
 <HeroSection />
 <HighlightsSection />
 <HowItWorksSection />
 <MetricsSection />
 <TrustSignalsSection />
 <CallToActionSection />
 </MainLayout>
 );
}
