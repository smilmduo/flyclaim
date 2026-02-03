import { useState, useRef, useEffect } from 'react';
import { Upload, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import api from '../services/api';

const TicketScanner = ({ onScanComplete }) => {
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState('');
  const [preview, setPreview] = useState(null);
  const fileInputRef = useRef(null);

  // Cleanup object URL
  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview);
    };
  }, [preview]);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please upload an image file (JPG, PNG)');
      return;
    }

    setScanning(true);
    setError('');

    // Create preview
    const objectUrl = URL.createObjectURL(file);
    setPreview(objectUrl);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/extract/ocr', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      onScanComplete(response.data);
    } catch (err) {
      console.error('Scan failed:', err);
      setError('Failed to scan ticket. Please enter details manually.');
    } finally {
      setScanning(false);
      // We don't reset input here so user can see the file name/preview if we wanted,
      // but to allow re-uploading same file we might want to, but standard is keep it or reset if needed.
      // With preview shown, we don't need to reset immediately unless "Change Image" is clicked.
    }
  };

  const handleReset = (e) => {
    e.stopPropagation();
    setPreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="mb-8">
      <div
        className={`bg-aviation-50 border-2 border-dashed border-aviation-200 rounded-xl p-6 text-center transition-colors ${!preview ? 'hover:bg-aviation-100 cursor-pointer' : ''}`}
        onClick={() => !preview && fileInputRef.current?.click()}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept="image/*"
          className="hidden"
        />

        {preview ? (
          <div className="flex flex-col items-center">
            <img
              src={preview}
              alt="Ticket Preview"
              className="h-48 object-contain mb-4 rounded-lg border border-slate-200 bg-white"
            />
            {scanning ? (
              <div className="flex items-center gap-2 text-aviation-700">
                <Loader2 className="h-5 w-5 animate-spin" />
                <span className="font-medium">Extracting details...</span>
              </div>
            ) : (
              <div className="text-center w-full">
                 <div className="flex items-center justify-center gap-2 text-green-600 mb-3">
                   <CheckCircle className="h-5 w-5" />
                   <span className="font-medium">Details Extracted</span>
                 </div>
                 <button
                   type="button"
                   onClick={handleReset}
                   className="text-sm text-aviation-600 hover:text-aviation-800 underline z-10 relative"
                 >
                   Scan a different ticket
                 </button>
              </div>
            )}
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <Upload className="h-10 w-10 text-aviation-500 mb-2" />
            <p className="text-aviation-800 font-medium text-lg">Scan Flight Ticket</p>
            <p className="text-sm text-aviation-500">Upload a photo of your boarding pass or ticket</p>
            <button type="button" className="mt-4 btn-secondary text-sm py-2">
              Select Image
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="mt-2 flex items-center gap-2 text-sm text-red-600">
          <AlertCircle className="h-4 w-4" />
          {error}
        </div>
      )}
    </div>
  );
};

export default TicketScanner;
