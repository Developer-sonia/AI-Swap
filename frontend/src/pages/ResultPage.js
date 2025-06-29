import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  Download, 
  Share2, 
  ArrowLeft, 
  Sparkles, 
  CheckCircle,
  RefreshCw
} from 'lucide-react';
import toast from 'react-hot-toast';

const ResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [originalImage, setOriginalImage] = useState(null);
  const [profession, setProfession] = useState(null);
  const [isDownloading, setIsDownloading] = useState(false);

  useEffect(() => {
    if (location.state) {
      setResult(location.state.result);
      setOriginalImage(location.state.originalImage);
      setProfession(location.state.profession);
    } else {
      // If no state, redirect to upload page
      navigate('/upload');
    }
  }, [location.state, navigate]);

  const handleDownload = async () => {
    if (!result?.result_url) {
      toast.error('No result image available for download');
      return;
    }

    setIsDownloading(true);
    
    try {
      const response = await fetch(result.result_url);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ai-swap-${profession?.name || 'result'}.jpg`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      toast.success('Image downloaded successfully!');
    } catch (error) {
      toast.error('Failed to download image');
      console.error('Download error:', error);
    } finally {
      setIsDownloading(false);
    }
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'AI-Swap Result',
          text: `Check out my ${profession?.name} transformation with AI-Swap!`,
          url: window.location.href,
        });
      } catch (error) {
        console.log('Share cancelled');
      }
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      toast.success('Link copied to clipboard!');
    }
  };

  const handleNewSwap = () => {
    navigate('/upload');
  };

  if (!result || !originalImage || !profession) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4 text-gray-400" />
          <p className="text-gray-600">Loading result...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <CheckCircle className="w-8 h-8 text-green-500 mr-2" />
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900">
              Transformation Complete!
            </h1>
          </div>
          <p className="text-xl text-gray-600">
            Your {profession.name} transformation is ready
          </p>
        </div>

        {/* Results Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Original Image */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 text-center">
              Original Image
            </h2>
            <div className="relative rounded-lg overflow-hidden border border-gray-200">
              <img
                src={originalImage}
                alt="Original"
                className="w-full h-80 object-cover"
              />
            </div>
            <div className="mt-4 text-center">
              <p className="text-sm text-gray-600">Your original photo</p>
            </div>
          </div>

          {/* Transformed Image */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 text-center">
              {profession.name} Transformation
            </h2>
            <div className="relative rounded-lg overflow-hidden border border-gray-200">
              <img
                src={result.result_url}
                alt={`${profession.name} transformation`}
                className="w-full h-80 object-cover"
              />
              <div className="absolute top-2 right-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                <Sparkles className="w-4 h-4 inline mr-1" />
                AI Generated
              </div>
            </div>
            <div className="mt-4 text-center">
              <p className="text-sm text-gray-600">
                Your face in {profession.name} style
              </p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
          <button
            onClick={handleDownload}
            disabled={isDownloading}
            className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-lg hover:from-green-700 hover:to-emerald-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isDownloading ? (
              <>
                <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
                Downloading...
              </>
            ) : (
              <>
                <Download className="w-5 h-5 mr-2" />
                Download Result
              </>
            )}
          </button>

          <button
            onClick={handleShare}
            className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
          >
            <Share2 className="w-5 h-5 mr-2" />
            Share Result
          </button>

          <button
            onClick={handleNewSwap}
            className="inline-flex items-center px-6 py-3 border-2 border-gray-300 text-gray-700 font-semibold rounded-lg hover:border-blue-400 hover:text-blue-600 transition-all duration-200"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Try Another
          </button>
        </div>

        {/* Result Details */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Transformation Details
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">Profession</p>
              <p className="font-semibold text-gray-900">{profession.name}</p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">Angle</p>
              <p className="font-semibold text-gray-900 capitalize">
                {result.angle?.replace('_', ' ') || 'Front'}
              </p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">Status</p>
              <p className="font-semibold text-green-600">Success</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultPage; 