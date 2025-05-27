import formatFileSize from '../utils/formatFileSize';
import useDragAndDropUpload from '../hooks/useDragAndDropUpload';

export default function DragAndDropUpload() {
  const { file, isUploading, error, handleDrop, handleDragOver } =
    useDragAndDropUpload();

  return (
    <div
      className="flex flex-col items-center justify-center border-2 border-dashed border-gray-400 rounded-md p-6 text-center"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      {isUploading ? (
        <div className="flex items-center justify-center">
          <div className="h-6 w-6 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
          <span className="ml-2">Uploading...</span>
        </div>
      ) : file ? (
        <div>
          <p className="font-medium">{file.name}</p>
          <p className="text-sm text-gray-500">{formatFileSize(file.size)}</p>
        </div>
      ) : (
        <p>Drag and drop a PDF file here</p>
      )}
      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
    </div>
  );
}
