import JobStatusList from '../../src/components/JobStatusList';

export default function DashboardPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center space-y-4">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <JobStatusList userId="demo-user" />
    </main>
  );
}
