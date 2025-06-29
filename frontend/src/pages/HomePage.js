import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Brain, 
  Sparkles, 
  Users, 
  Zap, 
  Shield, 
  Download,
  ArrowRight,
  Star
} from 'lucide-react';

const HomePage = () => {
  const features = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: "AI-Powered Face Detection",
      description: "Advanced facial recognition technology that accurately identifies and maps facial features for seamless swapping."
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Professional Templates",
      description: "Pre-rendered templates for various professions including Doctor, Professor, Engineer, Lawyer, and more."
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Real-time Processing",
      description: "Lightning-fast face swapping with real-time preview and instant results."
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: "Privacy First",
      description: "Your images are processed securely and never stored permanently on our servers."
    }
  ];

  const professions = [
    { name: "Doctor", color: "from-blue-500 to-cyan-500" },
    { name: "Professor", color: "from-purple-500 to-pink-500" },
    { name: "Engineer", color: "from-green-500 to-emerald-500" },
    { name: "Lawyer", color: "from-red-500 to-orange-500" },
    { name: "Business Executive", color: "from-indigo-500 to-blue-500" },
    { name: "Artist", color: "from-yellow-500 to-orange-500" }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <div className="flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl animate-float">
                <Brain className="w-10 h-10 text-white" />
              </div>
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              Transform Your Look with
              <span className="gradient-text block"> AI-Powered Face Swapping</span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Upload your photo and see yourself in different professional roles. 
              Our advanced AI technology preserves your face while seamlessly integrating 
              it into various professional templates.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/upload"
                className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-lg font-semibold rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
              >
                <Sparkles className="w-6 h-6 mr-2" />
                Start Swapping Now
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
              
              <button className="inline-flex items-center px-8 py-4 border-2 border-gray-300 text-gray-700 text-lg font-semibold rounded-xl hover:border-blue-400 hover:text-blue-600 transition-all duration-200">
                <Download className="w-5 h-5 mr-2" />
                Learn More
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose AI-Swap?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Experience the future of professional image transformation with our cutting-edge technology.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="p-6 bg-gray-50 rounded-xl hover:bg-white hover:shadow-lg transition-all duration-200 border border-gray-100"
              >
                <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl mb-4 text-white">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Professions Section */}
      <section className="py-20 bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Professional Templates Available
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Choose from a variety of professional roles and see yourself in different careers.
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {professions.map((profession, index) => (
              <div
                key={index}
                className="group cursor-pointer"
              >
                <div className={`w-full h-32 bg-gradient-to-br ${profession.color} rounded-xl flex items-center justify-center text-white font-semibold text-lg group-hover:scale-105 transition-transform duration-200 shadow-lg`}>
                  {profession.name}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Ready to Transform Your Professional Image?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join thousands of users who have already discovered their professional potential with AI-Swap.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/upload"
              className="inline-flex items-center px-8 py-4 bg-white text-blue-600 text-lg font-semibold rounded-xl hover:bg-gray-100 transition-all duration-200 shadow-lg"
            >
              <Sparkles className="w-6 h-6 mr-2" />
              Start Your Transformation
            </Link>
          </div>
          
          <div className="mt-8 flex items-center justify-center space-x-1 text-blue-100">
            {[...Array(5)].map((_, i) => (
              <Star key={i} className="w-5 h-5 fill-current" />
            ))}
            <span className="ml-2 text-sm">Trusted by 10,000+ users</span>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage; 