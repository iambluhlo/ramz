import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Homepage from './pages/Homepage';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Trading from './pages/Trading';
import Wallet from './pages/Wallet';
import AdminPanel from './pages/AdminPanel';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-dark-900 text-gray-100">
        <Navbar />
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/trading" element={<Trading />} />
          <Route path="/wallet" element={<Wallet />} />
          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;