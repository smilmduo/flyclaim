import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { Loader2, Plane, Calendar, AlertTriangle, User, MapPin, FileText } from 'lucide-react';
import TicketScanner from '../components/TicketScanner';

const SubmitClaim = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    flight_number: '',
    flight_date: '',
    airline_name: '',
    reason: 'delay',
    pnr: '',
    passenger_name: '',
    route_from: '',
    route_to: ''
  });

  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleScanComplete = (data) => {
    setFormData(prev => ({
      ...prev,
      flight_number: data.flight_number || prev.flight_number,
      flight_date: data.flight_date || prev.flight_date,
      airline_name: data.airline_name || prev.airline_name,
      reason: data.disruption_type || 'delay',
      pnr: data.pnr || prev.pnr,
      passenger_name: data.passenger_name || prev.passenger_name,
      route_from: data.route_from || prev.route_from,
      route_to: data.route_to || prev.route_to
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const payload = {
        ...formData,
        user_id: user.id
      };

      const response = await api.post('/claims', payload);
      navigate(`/track?id=${response.data.claim.claim_reference}`);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to submit claim');
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  return (
    <div className="max-w-3xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
        <div className="bg-aviation-50 px-8 py-6 border-b border-aviation-100">
          <h2 className="text-2xl font-bold text-aviation-900">File a New Claim</h2>
          <p className="text-aviation-700 mt-1">Provide your flight details to get started.</p>
        </div>

        <div className="p-8 pb-0">
          <TicketScanner onScanComplete={handleScanComplete} />
        </div>

        <form onSubmit={handleSubmit} className="p-8 pt-4 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            {/* Passenger Info */}
            <div className="md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Passenger Name
                </label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
                  <input
                    type="text"
                    name="passenger_name"
                    required
                    placeholder="e.g. John Doe"
                    className="input-field pl-10"
                    value={formData.passenger_name}
                    onChange={handleChange}
                  />
                </div>
              </div>
               <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  PNR / Booking Ref
                </label>
                <div className="relative">
                  <FileText className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
                  <input
                    type="text"
                    name="pnr"
                    placeholder="e.g. S9MUFD"
                    className="input-field pl-10"
                    value={formData.pnr}
                    onChange={handleChange}
                  />
                </div>
              </div>
            </div>

            {/* Flight Info */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Flight Number
              </label>
              <div className="relative">
                <Plane className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
                <input
                  type="text"
                  name="flight_number"
                  required
                  placeholder="e.g. 6E-234"
                  className="input-field pl-10"
                  value={formData.flight_number}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Date of Travel
              </label>
              <div className="relative">
                <Calendar className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
                <input
                  type="date"
                  name="flight_date"
                  required
                  className="input-field pl-10"
                  value={formData.flight_date}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Airline Name
              </label>
              <input
                type="text"
                name="airline_name"
                required
                placeholder="e.g. IndiGo"
                className="input-field"
                value={formData.airline_name}
                onChange={handleChange}
              />
            </div>

            {/* Route */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Departure Airport
              </label>
              <div className="relative">
                <MapPin className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
                <input
                  type="text"
                  name="route_from"
                  placeholder="e.g. Delhi (DEL)"
                  className="input-field pl-10"
                  value={formData.route_from}
                  onChange={handleChange}
                />
              </div>
            </div>
             <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Arrival Airport
              </label>
              <div className="relative">
                <MapPin className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
                <input
                  type="text"
                  name="route_to"
                  placeholder="e.g. Mumbai (BOM)"
                  className="input-field pl-10"
                  value={formData.route_to}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Reason for Claim
              </label>
              <div className="relative">
                <AlertTriangle className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
                <select
                  name="reason"
                  className="input-field pl-10"
                  value={formData.reason}
                  onChange={handleChange}
                >
                  <option value="delay">Flight Delayed</option>
                  <option value="cancellation">Flight Cancelled</option>
                  <option value="denied">Denied Boarding</option>
                </select>
              </div>
            </div>
          </div>

          {error && (
            <div className="text-red-500 text-sm bg-red-50 p-3 rounded-lg border border-red-100">
              {error}
            </div>
          )}

          <div className="pt-4">
            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary flex justify-center items-center gap-2 text-lg"
            >
              {loading ? <Loader2 className="animate-spin h-5 w-5" /> : 'Submit Claim'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SubmitClaim;
