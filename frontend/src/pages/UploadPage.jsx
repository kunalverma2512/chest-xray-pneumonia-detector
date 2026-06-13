import MainLayout from '../layouts/MainLayout.jsx';
import UploadLayout from '../components/upload/UploadLayout.jsx';
import XrayUploadPanel from '../components/upload/XrayUploadPanel.jsx';
import PredictionResultCard from '../components/upload/PredictionResultCard.jsx';
import { useUploadXray } from '../hooks/useUploadXray.js';

export default function UploadPage() {
 const { upload, data, loading, error } = useUploadXray();

 return (
 <MainLayout>
 <UploadLayout>
 <XrayUploadPanel onUpload={upload} loading={loading} />
 <PredictionResultCard data={data} loading={loading} error={error} />
 </UploadLayout>
 </MainLayout>
 );
}
