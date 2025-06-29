import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Image as ImageIcon, X, CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';

const ImageUpload = ({ onImageUpload, onImageRemove, uploadedImage }) => {
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
      toast.error('Please upload an image file (JPEG, PNG, WebP)');
      return;
    }

    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('File size must be less than 10MB');
      return;
    }

    setIsUploading(true);
    
    try {
      await onImageUpload(file);
      toast.success('Image uploaded successfully!');
    } catch (error) {
      toast.error('Failed to upload image. Please try again.');
      console.error('Upload error:', error);
    } finally {
      setIsUploading(false);
    }
  }, [onImageUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp']
    },
    multiple: false,
    disabled: isUploading
  });

  const handleRemoveImage = () => {
    onImageRemove();
    toast.success('Image removed');
  };

  return (
    <div className="w-full">
      {!uploadedImage ? (
        <div
          {...getRootProps()}
          className={`relative border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all duration-200 ${
            isDragActive
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
          } ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <input {...getInputProps()} />
          
          {isUploading ? (
            <div className="flex flex-col items-center space-y-4">
              <div className="spinner"></div>
              <p className="text-gray-600">Uploading image...</p>
            </div>
          ) : (
            <div className="flex flex-col items-center space-y-4">
              <div className="flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full">
                {isDragActive ? (
                  <Upload className="w-8 h-8 text-blue-600" />
                ) : (
                  <ImageIcon className="w-8 h-8 text-gray-400" />
                )}
              </div>
              
              <div>
                <p className="text-lg font-medium text-gray-900">
                  {isDragActive ? 'Drop your image here' : 'Upload your image'}
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  Drag and drop an image, or click to select
                </p>
                <p className="text-xs text-gray-400 mt-2">
                  Supports JPEG, PNG, WebP • Max 10MB
                </p>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="relative">
          <div className="relative rounded-lg overflow-hidden border border-gray-200">
            <img
              src={uploadedImage.preview || uploadedImage.url}
              alt="Uploaded"
              className="w-full h-64 object-cover"
            />
            <div className="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 transition-all duration-200 flex items-center justify-center">
              <button
                onClick={handleRemoveImage}
                className="opacity-0 hover:opacity-100 bg-red-500 text-white p-2 rounded-full transition-all duration-200 hover:bg-red-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>
          
          <div className="mt-3 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <span className="text-sm text-gray-600">Image uploaded successfully</span>
            </div>
            <button
              onClick={handleRemoveImage}
              className="text-sm text-red-600 hover:text-red-700 font-medium"
            >
              Remove
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUpload; 