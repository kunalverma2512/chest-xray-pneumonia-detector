import MainLayout from '../layouts/MainLayout.jsx';
import InsightsLayout from '../components/modelInsights/InsightsLayout.jsx';
import MetricsOverview from '../components/modelInsights/MetricsOverview.jsx';
import ValidationExplainer from '../components/modelInsights/ValidationExplainer.jsx';
import MetricSummaryCard from '../components/modelInsights/MetricSummaryCard.jsx';

export default function ModelInsightsPage() {
  return (
    <MainLayout>
      <InsightsLayout>
        <MetricsOverview />
        <ValidationExplainer />

        {/* Comparison section */}
        <div>
          <h2 className="text-heading text-black mb-8">
            Internal vs. Cross-Operator Summary
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-px" style={{ background: 'var(--border)' }}>
            <MetricSummaryCard
              label="Internal Accuracy"
              value="94.8%"
              delta="Test split · same training distribution"
            />
            <MetricSummaryCard
              label="Cross-Operator Accuracy"
              value="82.7%"
              delta="485 samples · independent operator cohort"
              important
            />
            <MetricSummaryCard
              label="Generalisation Gap"
              value="−12.1%"
              delta="Acceptable for single-site model"
            />
          </div>
        </div>
      </InsightsLayout>
    </MainLayout>
  );
}
