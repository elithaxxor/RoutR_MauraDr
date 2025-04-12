import React, { useState } from 'react';
import axios from 'axios';

const ScanForm = ({ token, setTaskId }) => {
  const [networkCidr, setNetworkCidr] = useState('');
  const [intensity, setIntensity] = useState('low');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        'http://localhost:5000/api/scan',
        { network_cidr: networkCidr, intensity },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setTaskId(response.data.task_id);
      setError('');
    } catch (err) {
      setError('Failed to start scan');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label>Network CIDR</label>
        <input
          type="text"
          className="form-control"
          value={networkCidr}
          onChange={(e) => setNetworkCidr(e.target.value)}
          placeholder="e.g., 192.168.1.0/24"
        />
      </div>
      <div className="mb-3">
        <label>Intensity</label>
        <select className="form-control" value={intensity} onChange={(e) => setIntensity(e.target.value)}>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>
      {error && <p className="text-danger">{error}</p>}
      <button type="submit" className="btn btn-primary">Start Scan</button>
    </form>
  );
};

export default ScanForm;
