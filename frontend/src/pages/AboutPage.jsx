import MainLayout from '../layouts/MainLayout.jsx';
import AboutIntro from '../components/about/AboutIntro.jsx';
import AboutModel from '../components/about/AboutModel.jsx';
import AboutYou from '../components/about/AboutYou.jsx';

export default function AboutPage() {
 return (
 <MainLayout>
 <AboutIntro />
 <AboutModel />
 <AboutYou />
 </MainLayout>
 );
}
