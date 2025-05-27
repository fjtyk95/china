import { useState, DragEvent } from 'react';

async function uploadFile(file: File): Promise<void> {
  const formData = new FormData();
  formData.append('file', file);
  await fetch('/api/upload', { method: 'POST', body: formData });
}

export default function useDragAndDropUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDrop = async (e: DragEvent<HTMLDivElement>): Promise<void> => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (!droppedFile) return;
    if (droppedFile.type !== 'application/pdf') {
      setError('Only PDF files are allowed');
      return;
    }
    setFile(droppedFile);
    setError(null);
    setIsUploading(true);
    try {
      await uploadFile(droppedFile);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>): void => {
    e.preventDefault();
  };

  return {
    file,
    isUploading,
    error,
    handleDrop,
    handleDragOver,
  };
}
