import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Clock, Shield, Search, ArrowRight, Plane, CheckCircle } from 'lucide-react';

const FeatureCard = ({ icon: Icon, title, description, delay }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, delay }}
    className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow"
  >
    <div className="w-12 h-12 bg-aviation-50 rounded-lg flex items-center justify-center mb-4 text-aviation-600">
      <Icon size={24} />
    </div>
    <h3 className="text-xl font-semibold text-slate-800 mb-2">{title}</h3>
    <p className="text-slate-600">{description}</p>
  </motion.div>
);

const StepCard = ({ number, title, description }) => (
  <div className="flex flex-col items-center text-center p-4">
    <div className="w-10 h-10 rounded-full bg-aviation-600 text-white flex items-center justify-center font-bold mb-4 shadow-lg shadow-aviation-200">
      {number}
    </div>
    <h4 className="text-lg font-semibold text-slate-800 mb-2">{title}</h4>
    <p className="text-sm text-slate-500 max-w-xs">{description}</p>
  </div>
);

const Home = () => {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-white pt-16 pb-24 lg:pt-32 lg:pb-40">
        <div className="absolute inset-0 bg-gradient-to-br from-aviation-50 via-white to-aviation-50 opacity-70" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center max-w-3xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-900 tracking-tight mb-6">
                Claim Your Flight <br className="hidden sm:block" />
                <span className="text-aviation-600">Compensation Easily</span>
              </h1>
              <p className="text-xl text-slate-600 mb-10 max-w-2xl mx-auto">
                Delayed or cancelled flight? Get up to <span className="font-semibold text-slate-900">₹20,000</span> in compensation.
                We handle the paperwork, you get paid.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="flex flex-col sm:flex-row justify-center gap-4"
            >
              <Link to="/claim/new" className="btn-primary flex items-center justify-center gap-2 group text-lg px-8 py-3">
                File a Claim
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link to="/track" className="btn-secondary text-lg px-8 py-3">
                Track Claim
              </Link>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1, delay: 0.5 }}
              className="mt-12 flex items-center justify-center gap-6 text-sm text-slate-500"
            >
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span>No Win, No Fee</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span>DGCA Compliant</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span>Quick Processing</span>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">Why Choose FlyClaim?</h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              We combine AI technology with legal expertise to get your compensation faster.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              icon={Clock}
              title="Fast & Automated"
              description="Our AI agents process your claim instantly, cutting down waiting times by weeks."
              delay={0.1}
            />
            <FeatureCard
              icon={Shield}
              title="Secure & Private"
              description="Your data is encrypted and handled with bank-grade security protocols."
              delay={0.2}
            />
            <FeatureCard
              icon={Search}
              title="Transparent Tracking"
              description="Track every step of your claim in real-time through our dashboard."
              delay={0.3}
            />
          </div>
        </div>
      </section>

      {/* How it Works Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">How It Works</h2>
          </div>

          <div className="relative">
            {/* Connecting line for desktop */}
            <div className="hidden md:block absolute top-10 left-0 w-full h-0.5 bg-slate-100 -z-10" />

            <div className="grid md:grid-cols-4 gap-8">
              <StepCard
                number="1"
                title="Submit Details"
                description="Enter your flight information and reason for delay."
              />
              <StepCard
                number="2"
                title="AI Verification"
                description="We verify eligibility against DGCA rules instantly."
              />
              <StepCard
                number="3"
                title="Airline Submission"
                description="We generate legal documents and send to the airline."
              />
              <StepCard
                number="4"
                title="Get Paid"
                description="Receive compensation directly in your bank account."
              />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
