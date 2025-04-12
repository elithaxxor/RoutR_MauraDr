import React from 'react';

const ResultsTable = ({ results }) => {
  if (!Object.keys(results).length) return <p>No results available.</p>;

  return (
    <table className="table mt-4">
      <thead>
        <tr>
          <th>Host</th>
          <th>Score</th>
          <th>Category</th>
          <th>Remediation</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(results).map(([host, data]) => (
          <tr key={host}>
            <td>{host}</td>
            <td>{data.score}</td>
            <td>{data.category}</td>
            <td>{data.remediation.join(', ')}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ResultsTable;
