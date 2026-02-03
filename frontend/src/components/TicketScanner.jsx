import { useState, useRef } from 'react';
import { Upload, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import api from '../services/api';

const TicketScanner = ({ onScanComplete }) => {
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

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
      // Reset input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <div className="mb-8">
      <div className="bg-aviation-50 border-2 border-dashed border-aviation-200 rounded-xl p-6 text-center hover:bg-aviation-100 transition-colors cursor-pointer"
           onClick={() => fileInputRef.current?.click()}>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept="image/*"
          className="hidden"
        />

        {scanning ? (
          <div className="flex flex-col items-center">
            <Loader2 className="h-10 w-10 text-aviation-600 animate-spin mb-2" />
            <p className="text-aviation-700 font-medium">Scanning ticket...</p>
            <p className="text-sm text-aviation-500">Extracting flight details</p>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <Upload className="h-10 w-10 text-aviation-500 mb-2" />
            <p className="text-aviation-800 font-medium text-lg">Scan Flight Ticket</p>
            <p className="text-sm text-aviation-500">Upload a photo of your boarding pass or ticket</p>
            <button className="mt-4 btn-secondary text-sm py-2">
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
