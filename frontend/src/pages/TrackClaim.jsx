import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import api from '../services/api';
import { Search, Loader2, CheckCircle, XCircle, Clock, FileText } from 'lucide-react';
import { motion } from 'framer-motion';

const StatusStep = ({ title, status, isLast }) => {
  // status: 'completed', 'current', 'upcoming', 'error'

  let icon = <div className="w-3 h-3 bg-slate-300 rounded-full" />;
  let colorClass = "text-slate-400";
  let borderClass = "border-slate-300";

  if (status === 'completed') {
    icon = <CheckCircle className="w-6 h-6 text-green-500" />;
    colorClass = "text-slate-800 font-medium";
    borderClass = "border-green-500";
  } else if (status === 'current') {
    icon = <Loader2 className="w-6 h-6 text-aviation-500 animate-spin" />;
    colorClass = "text-aviation-600 font-bold";
    borderClass = "border-aviation-500";
  } else if (status === 'error') {
    icon = <XCircle className="w-6 h-6 text-red-500" />;
    colorClass = "text-red-600 font-medium";
    borderClass = "border-red-500";
  }

  return (
    <div className="flex flex-col items-center relative flex-1">
      {!isLast && (
        <div className={`absolute top-3 left-1/2 w-full h-0.5 -z-10 ${status === 'completed' ? 'bg-green-500' : 'bg-slate-200'}`} />
      )}
      <div className="bg-white p-1 z-10">
        {icon}
      </div>
      <span className={`mt-2 text-sm ${colorClass}`}>{title}</span>
    </div>
  );
};

const TrackClaim = () => {
  const [searchParams] = useSearchParams();
  const [claimRef, setClaimRef] = useState(searchParams.get('id') || '');
  const [claim, setClaim] = useState(null);
  const [loading, setLoading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState('');

  const fetchClaim = async (ref) => {
    if (!ref) return;
    setLoading(true);
    setError('');
    setClaim(null);

    try {
      const response = await api.get(`/claims/${ref}`);
      setClaim(response.data);
    } catch (err) {
      setError('Claim not found. Please check the reference number.');
    } finally {
      setLoading(false);
    }
  };

  const handleSimulateResponse = async () => {
    if (!claim) return;
    setProcessing(true);
    try {
        const response = await api.post(`/claims/${claim.claim_reference}/process`);
        setClaim(response.data.claim);
    } catch (err) {
        setError('Simulation failed: ' + (err.response?.data?.error || err.message));
    } finally {
        setProcessing(false);
    }
  };

  useEffect(() => {
    const id = searchParams.get('id');
    if (id) {
      setClaimRef(id);
      fetchClaim(id);
    }
  }, [searchParams]);

  const handleSubmit = (e) => {
    e.preventDefault();
    fetchClaim(claimRef);
  };

  // Determine steps status
  const getSteps = (status) => {
    // Default state
    let steps = [
      { title: 'Submitted', status: 'upcoming' },
      { title: 'In Review', status: 'upcoming' },
      { title: 'Decision', status: 'upcoming' },
    ];

    if (!status) return steps;

    // Map backend status to steps
    // Statuses: initiated, eligibility_checked, document_generated, submitted_to_airline, awaiting_response, airline_responded, resolved, rejected, paid, cancelled

    // Step 1: Submitted
    steps[0].status = 'completed';

    // Step 2: In Review
    const inReviewStatuses = ['submitted_to_airline', 'awaiting_response', 'airline_responded', 'escalated_airsewa', 'escalated_dgca'];
    const doneStatuses = ['resolved', 'rejected', 'paid', 'cancelled'];

    if (inReviewStatuses.includes(status)) {
        steps[1].status = 'current';
    } else if (doneStatuses.includes(status)) {
        steps[1].status = 'completed';
    } else {
        // Still in early stages (initiated, etc)
        steps[1].status = 'current';
    }

    // Step 3: Decision
    if (status === 'resolved' || status === 'paid') {
        steps[2].status = 'completed';
        steps[2].title = 'Approved';
    } else if (status === 'rejected' || status === 'cancelled') {
        steps[2].status = 'error';
        steps[2].title = 'Rejected';
    } else if (steps[1].status === 'completed') {
        steps[2].status = 'current'; // Waiting for final decision logic if passed review but not final state?
        // Actually, if 'airline_responded', it might be waiting user action or auto decision.
        // For simplicity, let's say 'airline_responded' is still 'In Review' until 'resolved'/'rejected'.
    }

    return steps;
  };

  const steps = claim ? getSteps(claim.status) : [];

  return (
    <div className="max-w-3xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Track Your Claim</h1>
        <p className="mt-2 text-slate-600">Enter your claim reference number to check the current status.</p>
      </div>

      <form onSubmit={handleSubmit} className="mb-10">
        <div className="flex gap-4 max-w-md mx-auto">
          <div className="relative flex-grow">
            <Search className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
            <input
              type="text"
              placeholder="e.g. FC-20251028-6E234-0001"
              className="input-field pl-10"
              value={claimRef}
              onChange={(e) => setClaimRef(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? <Loader2 className="animate-spin h-5 w-5" /> : 'Track'}
          </button>
        </div>
      </form>

      {error && (
        <div className="text-center p-4 bg-red-50 text-red-600 rounded-lg border border-red-100 max-w-md mx-auto">
          {error}
        </div>
      )}

      {claim && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden"
        >
          <div className="px-6 py-4 bg-aviation-50 border-b border-aviation-100 flex justify-between items-center">
            <div>
              <span className="text-xs font-semibold text-aviation-600 uppercase tracking-wider">Claim Reference</span>
              <h3 className="text-lg font-bold text-slate-900">{claim.claim_reference}</h3>
            </div>
            <div className="text-right">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Amount</span>
              <h3 className="text-lg font-bold text-slate-900">₹{claim.compensation_amount.toLocaleString()}</h3>
            </div>
          </div>

          <div className="p-8">
            <div className="flex justify-between mb-12">
              {steps.map((step, index) => (
                <StatusStep
                  key={index}
                  title={step.title}
                  status={step.status}
                  isLast={index === steps.length - 1}
                />
              ))}
            </div>

            <div className="bg-slate-50 rounded-lg p-6 space-y-4">
              <h4 className="font-semibold text-slate-900 flex items-center gap-2">
                <FileText className="h-5 w-5 text-aviation-500" />
                Claim Details
              </h4>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="block text-slate-500">Airline</span>
                  <span className="font-medium text-slate-900">{claim.airline_name}</span>
                </div>
                <div>
                  <span className="block text-slate-500">Flight Number</span>
                  <span className="font-medium text-slate-900">{claim.flight_number}</span>
                </div>
                <div>
                  <span className="block text-slate-500">Date</span>
                  <span className="font-medium text-slate-900">{new Date(claim.flight_date).toLocaleDateString()}</span>
                </div>
                <div>
                  <span className="block text-slate-500">Status</span>
                  <span className="font-medium text-slate-900 capitalize">{claim.status?.replace(/_/g, ' ')}</span>
                </div>
              </div>

              {claim.resolution_notes && (
                <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded text-sm text-green-800">
                    <strong>Resolution:</strong> {claim.resolution_notes}
                </div>
              )}

              {/* Eligibility Assessment Section */}
              {claim.eligibility_details && (
                <div className="mt-6 border-t border-slate-200 pt-6">
                    <h4 className="font-semibold text-slate-900 mb-3 flex items-center gap-2">
                         <span className={claim.is_eligible ? "text-green-500" : "text-red-500"}>
                            {claim.is_eligible ? "✅" : "❌"}
                         </span>
                         Eligibility Assessment
                    </h4>
                    <div className="bg-slate-50 p-4 rounded-lg text-sm space-y-3">
                        <div>
                            <span className="block text-slate-500 text-xs uppercase tracking-wide">Compensation</span>
                            <span className="font-bold text-slate-900 text-lg">
                                {claim.eligibility_details.currency} {claim.eligibility_details.compensation_amount}
                            </span>
                        </div>
                        <div>
                            <span className="block text-slate-500 text-xs uppercase tracking-wide">Reasoning</span>
                            <p className="text-slate-700 mt-1">{claim.eligibility_details.reason}</p>
                        </div>

                        {claim.eligibility_details.airline_obligations && Object.keys(claim.eligibility_details.airline_obligations).length > 0 && (
                            <div>
                                <span className="block text-slate-500 text-xs uppercase tracking-wide mb-1">Additional Entitlements</span>
                                <ul className="list-disc pl-5 space-y-1 text-slate-700">
                                    {claim.eligibility_details.airline_obligations.meals_and_refreshments && (
                                        <li>Meals and Refreshments</li>
                                    )}
                                    {claim.eligibility_details.airline_obligations.hotel_accommodation && (
                                        <li>Hotel Accommodation (for overnight delays)</li>
                                    )}
                                    {claim.eligibility_details.airline_obligations.communication && (
                                        <li>Two phone calls or emails</li>
                                    )}
                                    {claim.eligibility_details.airline_obligations.refund_option && (
                                        <li>Option for Full Refund</li>
                                    )}
                                </ul>
                            </div>
                        )}

                         <div className="text-xs text-slate-400 mt-2">
                            Legal Basis: {claim.eligibility_details.legal_basis || 'DGCA CAR Section 3'}
                        </div>
                    </div>
                </div>
              )}

              {claim.status === 'submitted_to_airline' && (
                <div className="pt-4 border-t border-slate-200">
                    <button
                        onClick={handleSimulateResponse}
                        disabled={processing}
                        className="w-full btn-primary bg-indigo-600 hover:bg-indigo-700 text-white py-2 rounded-lg flex justify-center items-center gap-2"
                    >
                        {processing ? <Loader2 className="animate-spin h-5 w-5" /> : 'Simulate Airline Response (Demo)'}
                    </button>
                    <p className="text-xs text-center text-slate-500 mt-2">
                        *In a real scenario, this happens automatically when the airline replies (up to 30 days).
                    </p>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default TrackClaim;
