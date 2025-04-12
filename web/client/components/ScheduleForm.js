import React, { useState } from 'react';
import axios from 'axios';

const ScheduleForm = ({ token }) => {
  const [networkCidr, setNetworkCidr] = useState('');
  const [intensity, setIntensity] = useState('low');
  const [frequency, setFrequency] = useState('immediate');
  const [time, setTime] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = { network_cidr: networkCidr, intensity, frequency };
      if (frequency !== 'immediate') payload.time = time;
      const response = await axios.post(
        'http://localhost:5000/api/schedule',
        payload,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setMessage(`Schedule created: ${response.data.message}`);
    } catch (err) {
      setMessage('Failed to create schedule');
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
      <div className="mb-3">
        <label>Frequency</label>
        <select className="form-control" value={frequency} onChange={(e) => setFrequency(e.target.value)}>
          <option value="immediate">Immediate</option>
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
        </select>
      </div>
      {frequency !== 'immediate' && (
        <div className="mb-3">
          <label>Time (HH:MM)</label>
          <input
            type="text"
            className="form-control"
            value={time}
            onChange={(e) => setTime(e.target.value)}
            placeholder="e.g., 03:00"
          />
        </div>
      )}
      {message && <p className={message.includes('Failed') ? 'text-danger' : 'text-success'}>{message}</p>}
      <button type="submit" className="btn btn-primary">Set Schedule</button>
    </form>
  );
};

export default ScheduleForm;
