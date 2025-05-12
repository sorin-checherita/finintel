import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from '../services/api';

const AddTicker = () => {
  const [ticker, setTicker] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/tickers', { ticker });
      setTicker('');
      alert('Ticker added successfully!');
    } catch (error) {
      console.error('Error adding ticker:', error);
    }
  };

  return (
    <div className="container mt-4">
      <h1>Add New Ticker</h1>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="ticker">
          <Form.Label>Ticker</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter ticker symbol"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
          />
        </Form.Group>
        <Button variant="primary" type="submit" className="mt-3">
          Add Ticker
        </Button>
      </Form>
    </div>
  );
};

export default AddTicker;