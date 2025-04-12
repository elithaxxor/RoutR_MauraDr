import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ScanForm from '../components/ScanForm';
import ResultsTable from '../components/ResultsTable';

const Dashboard = ({ token }) => {
  const [results, setResults] = useState({});
  const [taskId, setTaskId] = useState(null);

  const checkTaskStatus = async () => {
    if (!taskId) return;
    try {
      const response = await axios.get(`http://localhost:5000/api/results/${taskId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.data.status === 'completed') {
        setResults(response.data.results);
        setTaskId(null);
      }
    } catch (err) {
      console.error('Error checking task status:', err);
    }
  };

  useEffect(() => {
    if (taskId) {
      const interval = setInterval(checkTaskStatus, 5000);
      return () => clearInterval(interval);
    }
  }, [taskId]);

  return (
    <div className="container">
      <h2>Dashboard</h2>
      <ScanForm token={token} setTaskId={setTaskId} />
      <ResultsTable results={results} />
    </div>
  );
};

export default Dashboard;
