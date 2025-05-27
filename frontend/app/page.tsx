import DragAndDropUpload from '../components/DragAndDropUpload';

export default function Page() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-8">
      <h1 className="text-2xl font-bold">Hello Next.js 14!</h1>
      <DragAndDropUpload />
    </main>
  );
}
