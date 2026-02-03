import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { Plus, ArrowRight, Clock, FileText, AlertCircle } from 'lucide-react';

const StatusBadge = ({ status }) => {
  const styles = {
    initiated: 'bg-blue-100 text-blue-800',
    eligibility_checked: 'bg-purple-100 text-purple-800',
    document_generated: 'bg-indigo-100 text-indigo-800',
    submitted_to_airline: 'bg-yellow-100 text-yellow-800',
    awaiting_response: 'bg-yellow-100 text-yellow-800',
    airline_responded: 'bg-orange-100 text-orange-800',
    resolved: 'bg-green-100 text-green-800',
    paid: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
    cancelled: 'bg-gray-100 text-gray-800'
  };

  const className = styles[status] || 'bg-gray-100 text-gray-800';
  const label = status?.replace(/_/g, ' ');

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${className}`}>
      {label}
    </span>
  );
};

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    const fetchClaims = async () => {
      try {
        const response = await api.get(`/users/${user.id}/claims`);
        setClaims(response.data);
      } catch (err) {
        setError('Failed to fetch claims');
      } finally {
        setLoading(false);
      }
    };

    fetchClaims();
  }, [user, navigate]);

  if (!user) return null;

  return (
    <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">My Dashboard</h1>
          <p className="mt-1 text-slate-600">Manage and track your flight compensation claims.</p>
        </div>
        <Link to="/claim/new" className="btn-primary flex items-center gap-2">
          <Plus className="h-5 w-5" />
          New Claim
        </Link>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-aviation-600"></div>
        </div>
      ) : error ? (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <AlertCircle className="h-5 w-5" />
          {error}
        </div>
      ) : claims.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-xl shadow-sm border border-slate-100">
          <div className="mx-auto h-12 w-12 text-slate-400 mb-4">
            <FileText size={48} strokeWidth={1} />
          </div>
          <h3 className="text-lg font-medium text-slate-900">No claims found</h3>
          <p className="mt-1 text-slate-500">You haven't filed any compensation claims yet.</p>
          <div className="mt-6">
            <Link to="/claim/new" className="btn-secondary">
              File your first claim
            </Link>
          </div>
        </div>
      ) : (
        <div className="bg-white shadow-sm rounded-xl border border-slate-100 overflow-hidden">
          <ul className="divide-y divide-slate-100">
            {claims.map((claim) => (
              <li key={claim.id}>
                <Link to={`/track?id=${claim.claim_reference}`} className="block hover:bg-slate-50 transition-colors">
                  <div className="px-6 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="flex-shrink-0 h-10 w-10 rounded-full bg-aviation-50 flex items-center justify-center text-aviation-600">
                        <FileText size={20} />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <p className="text-sm font-medium text-aviation-600">{claim.claim_reference}</p>
                          <span className="text-slate-300">•</span>
                          <p className="text-sm font-medium text-slate-900">{claim.airline_name}</p>
                        </div>
                        <div className="flex items-center gap-4 mt-1">
                           <p className="flex items-center text-sm text-slate-500">
                             <Clock size={14} className="mr-1" />
                             {new Date(claim.flight_date).toLocaleDateString()}
                           </p>
                           <p className="text-sm text-slate-500">
                             Flight: {claim.flight_number}
                           </p>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-4">
                      <div className="text-right hidden sm:block">
                        <p className="text-sm font-medium text-slate-900">₹{claim.compensation_amount.toLocaleString()}</p>
                        <StatusBadge status={claim.status} />
                      </div>
                      <ArrowRight className="h-5 w-5 text-slate-400" />
                    </div>
                  </div>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
