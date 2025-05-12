import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard'; // Import the Dashboard page
import Header from './components/Header'; // Import the Header component
import './styles/App.css';

function App() {
  return (
    <Router>
      <Header /> {/* Add a navigation header */}
      <div className="App">
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          {/* Add more routes here as needed */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
