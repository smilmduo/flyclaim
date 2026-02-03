import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Layout from './components/Layout';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import SubmitClaim from './pages/SubmitClaim';
import TrackClaim from './pages/TrackClaim';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/claim/new" element={<SubmitClaim />} />
            <Route path="/track" element={<TrackClaim />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </Layout>
      </AuthProvider>
    </Router>
  );
}

export default App;
