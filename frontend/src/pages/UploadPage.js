import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Upload, 
  Sparkles, 
  User, 
  Briefcase, 
  Camera,
  ArrowRight,
  Loader
} from 'lucide-react';
import toast from 'react-hot-toast';
import ImageUpload from '../components/ImageUpload';
import { uploadImage, getProfessions, swapFace } from '../services/api';

const UploadPage = () => {
  const navigate = useNavigate();
  const [uploadedImage, setUploadedImage] = useState(null);
  const [professions, setProfessions] = useState([]);
  const [selectedProfession, setSelectedProfession] = useState(null);
  const [selectedAngle, setSelectedAngle] = useState('front');
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);

  const angles = [
    { id: 'front', name: 'Front View', icon: '👤' },
    { id: 'side', name: 'Side View', icon: '👥' },
    { id: 'three_quarter', name: 'Three Quarter', icon: '👤' },
    { id: 'back', name: 'Back View', icon: '👤' }
  ];

  useEffect(() => {
    loadProfessions();
  }, []);

  const loadProfessions = async () => {
    try {
      const data = await getProfessions();
      setProfessions(data.professions || []);
    } catch (error) {
      toast.error('Failed to load professions');
      console.error('Error loading professions:', error);
    }
  };

  const handleImageUpload = async (file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await uploadImage(formData);
      
      if (response.success) {
        setUploadedImage({
          file,
          preview: URL.createObjectURL(file),
          imageId: response.image_id,
          faceDetected: response.face_detected,
          landmarks: response.landmarks
        });
        setCurrentStep(2);
      } else {
        throw new Error(response.message || 'Upload failed');
      }
    } catch (error) {
      toast.error(error.message || 'Failed to upload image');
      throw error;
    }
  };

  const handleImageRemove = () => {
    if (uploadedImage?.preview) {
      URL.revokeObjectURL(uploadedImage.preview);
    }
    setUploadedImage(null);
    setSelectedProfession(null);
    setCurrentStep(1);
  };

  const handleProfessionSelect = (profession) => {
    setSelectedProfession(profession);
    setCurrentStep(3);
  };

  const handleSwapFace = async () => {
    if (!uploadedImage || !selectedProfession) {
      toast.error('Please select an image and profession');
      return;
    }

    setIsProcessing(true);
    
    try {
      const response = await swapFace({
        image_id: uploadedImage.imageId,
        profession: selectedProfession.id,
        angle: selectedAngle
      });

      if (response.success) {
        // Navigate to result page with the result data
        navigate('/result', { 
          state: { 
            result: response,
            originalImage: uploadedImage.preview,
            profession: selectedProfession
          }
        });
      } else {
        throw new Error(response.message || 'Face swap failed');
      }
    } catch (error) {
      toast.error(error.message || 'Failed to process face swap');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Upload & Transform
          </h1>
          <p className="text-xl text-gray-600">
            Upload your photo and choose a professional template to see yourself in a new role.
          </p>
        </div>

        {/* Progress Steps */}
        <div className="flex justify-center mb-8">
          <div className="flex items-center space-x-4">
            {[1, 2, 3].map((step) => (
              <div key={step} className="flex items-center">
                <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 ${
                  currentStep >= step 
                    ? 'bg-blue-600 border-blue-600 text-white' 
                    : 'bg-white border-gray-300 text-gray-400'
                }`}>
                  {step === 1 && <Upload className="w-5 h-5" />}
                  {step === 2 && <Briefcase className="w-5 h-5" />}
                  {step === 3 && <Sparkles className="w-5 h-5" />}
                </div>
                {step < 3 && (
                  <div className={`w-16 h-0.5 mx-2 ${
                    currentStep > step ? 'bg-blue-600' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Step 1: Image Upload */}
        {currentStep === 1 && (
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="text-center mb-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                Upload Your Photo
              </h2>
              <p className="text-gray-600">
                Choose a clear, front-facing photo for best results
              </p>
            </div>
            
            <ImageUpload
              onImageUpload={handleImageUpload}
              onImageRemove={handleImageRemove}
              uploadedImage={uploadedImage}
            />
          </div>
        )}

        {/* Step 2: Profession Selection */}
        {currentStep >= 2 && uploadedImage && (
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="text-center mb-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                Choose Your Profession
              </h2>
              <p className="text-gray-600">
                Select a professional template to transform your image
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {professions.map((profession) => (
                <div
                  key={profession.id}
                  onClick={() => handleProfessionSelect(profession)}
                  className={`p-6 rounded-xl border-2 cursor-pointer transition-all duration-200 hover:shadow-lg ${
                    selectedProfession?.id === profession.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-blue-300'
                  }`}
                >
                  <div className="flex items-center space-x-3 mb-3">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                      <User className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">
                        {profession.name}
                      </h3>
                      <p className="text-sm text-gray-500">
                        {profession.description}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">
                      {profession.angles?.length || 4} angles available
                    </span>
                    <ArrowRight className="w-5 h-5 text-gray-400" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Step 3: Angle Selection and Processing */}
        {currentStep >= 3 && selectedProfession && (
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="text-center mb-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                Choose View Angle
              </h2>
              <p className="text-gray-600">
                Select the angle for your {selectedProfession.name} transformation
              </p>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              {angles.map((angle) => (
                <div
                  key={angle.id}
                  onClick={() => setSelectedAngle(angle.id)}
                  className={`p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 text-center ${
                    selectedAngle === angle.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-blue-300'
                  }`}
                >
                  <div className="text-2xl mb-2">{angle.icon}</div>
                  <div className="text-sm font-medium text-gray-900">
                    {angle.name}
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-center">
              <button
                onClick={handleSwapFace}
                disabled={isProcessing}
                className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-lg font-semibold rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                {isProcessing ? (
                  <>
                    <Loader className="w-6 h-6 mr-2 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-6 h-6 mr-2" />
                    Transform My Image
                  </>
                )}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadPage; 