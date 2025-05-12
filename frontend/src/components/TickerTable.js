import React, { useState } from 'react';
import { Table, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const TickerTable = ({ data, deleteTicker, refreshData }) => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [filter, setFilter] = useState('');
  const navigate = useNavigate();

  const sortedData = [...data].sort((a, b) => {
    if (!sortConfig.key) return 0;
    const aValue = a[sortConfig.key];
    const bValue = b[sortConfig.key];
    if (aValue < bValue) return sortConfig.direction === 'asc' ? -1 : 1;
    if (aValue > bValue) return sortConfig.direction === 'asc' ? 1 : -1;
    return 0;
  });

  const filteredData = sortedData.filter((item) =>
    item.ticker.toLowerCase().includes(filter.toLowerCase())
  );

  const handleSort = (key) => {
    setSortConfig((prev) => ({
      key,
      direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc',
    }));
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Filter by ticker"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        className="mb-3 form-control"
      />
      <Table striped bordered hover>
        <thead>
          <tr>
            <th onClick={() => handleSort('ticker')}>Ticker</th>
            <th onClick={() => handleSort('name')}>Name</th>
            <th onClick={() => handleSort('price')}>Price</th>
            <th onClick={() => handleSort('pe_ratio')}>P/E Ratio</th>
            <th onClick={() => handleSort('revenue')}>Revenue</th>
            <th onClick={() => handleSort('ebitda')}>EBITDA</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredData.map((item) => (
            <tr key={item.ticker}>
              <td
                style={{ cursor: 'pointer', color: 'blue' }}
                onClick={() => navigate(`/ticker/${item.ticker}`)}
              >
                {item.ticker}
              </td>
              <td>{item.name}</td>
              <td>{item.price}</td>
              <td>{item.pe_ratio}</td>
              <td>{item.revenue}</td>
              <td>{item.ebitda}</td>
              <td>
                <Button
                  variant="danger"
                  onClick={() => deleteTicker(item.ticker)}
                >
                  Delete
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default TickerTable;