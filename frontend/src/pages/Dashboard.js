import React, { useState, useEffect } from 'react';
import { Button } from 'react-bootstrap';
import axios from '../services/api';
import TickerTable from '../components/TickerTable';
import AddTickerModal from '../components/AddTickerForm';

const Dashboard = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false); // State to control modal visibility

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/financial-data');
      setData(response.data.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const deleteTicker = async (ticker) => {
    try {
      await axios.delete(`/tickers/${ticker}`);
      fetchData();
    } catch (error) {
      console.error('Error deleting ticker:', error);
    }
  };

  const refreshData = async () => {
    try {
      await axios.post('/refresh-data');
      fetchData();
    } catch (error) {
      console.error('Error refreshing data:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="container mt-4">
      <h1>Dashboard</h1>
      <Button variant="primary" onClick={refreshData} className="mb-3">
        Refresh Data
      </Button>
      <TickerTable
        data={data}
        deleteTicker={deleteTicker}
        refreshData={refreshData}
      />
      {/* Floating Add Ticker Button */}
      <Button
        variant="success"
        className="floating-add-button"
        onClick={() => setShowModal(true)}
      >
        +
      </Button>
      {/* Add Ticker Modal */}
      <AddTickerModal
        show={showModal}
        handleClose={() => setShowModal(false)}
        refreshData={fetchData}
      />
    </div>
  );
};

export default Dashboard;