import SubscribeButton from '../../src/components/SubscribeButton';
import JobStatusList from '../../src/components/JobStatusList';

export default function DashboardPage() {
  const currentPlan = 'Free';

  return (
    <main className="flex min-h-screen flex-col items-center space-y-4 p-4">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <p>Current plan: {currentPlan}</p>
      <SubscribeButton />
      <JobStatusList userId="demo-user" />
    </main>
  );
}
