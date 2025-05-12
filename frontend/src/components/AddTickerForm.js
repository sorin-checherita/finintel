import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import axios from '../services/api';

const AddTickerModal = ({ show, handleClose, refreshData }) => {
  const [ticker, setTicker] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/tickers', { ticker });
      setTicker('');
      refreshData(); // Refresh the table after adding a ticker
      handleClose();
    } catch (error) {
      console.error('Error adding ticker:', error);
    }
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Add New Ticker</Modal.Title>
      </Modal.Header>
      <Modal.Body>
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
      </Modal.Body>
    </Modal>
  );
};

export default AddTickerModal;