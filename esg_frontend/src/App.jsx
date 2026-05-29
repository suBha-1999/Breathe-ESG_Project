import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchRecords()
  }, [])

  const fetchRecords = async () => {
    try {
      // Fetching the 7 records from your Django API
      const response = await axios.get('https://breathe-esg-assignment-nht7.onrender.com/api/records/')
      setRecords(response.data)
      setLoading(false)
    } catch (error) {
      console.error("Error fetching data:", error)
      setLoading(false)
    }
  }

  const handleApprove = async (id) => {
    try {
      await axios.post(`https://breathe-esg-assignment-nht7.onrender.com/api/records/${id}/approve/`)
      // Update the UI instantly so the analyst doesn't have to refresh
      setRecords(records.map(record => 
        record.id === id ? { ...record, status: 'APPROVED' } : record
      ))
    } catch (error) {
      alert("Failed to approve record.")
    }
  }

  if (loading) return <h2>Loading Analyst Dashboard...</h2>

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Breathe ESG: Data Review Dashboard</h1>
      <p>Review normalized data before locking for final audit.</p>

      <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse', marginTop: '20px' }}>
        <thead>
          <tr style={{ backgroundColor: '#f4f4f4', borderBottom: '2px solid #ddd' }}>
            <th style={{ padding: '12px' }}>Source</th>
            <th style={{ padding: '12px' }}>Scope</th>
            <th style={{ padding: '12px' }}>Normalized Emissions</th>
            <th style={{ padding: '12px' }}>Date / Period</th>
            <th style={{ padding: '12px' }}>Status</th>
            <th style={{ padding: '12px' }}>Action</th>
          </tr>
        </thead>
        <tbody>
          {records.map(record => (
            <tr key={record.id} style={{ borderBottom: '1px solid #ddd' }}>
              <td style={{ padding: '12px' }}>
                <strong>{record.source_name}</strong> <br/>
                <small style={{ color: '#666' }}>{record.source_type}</small>
              </td>
              <td style={{ padding: '12px' }}>{record.scope}</td>
              <td style={{ padding: '12px' }}>
                <strong>{parseFloat(record.normalized_value).toFixed(2)}</strong> <br/>
                <small style={{ color: '#666' }}>MT CO2e (derived from {parseFloat(record.raw_value).toFixed(2)} {record.raw_unit})</small>
              </td>
              <td style={{ padding: '12px' }}>
                {record.start_date === record.end_date 
                  ? record.start_date 
                  : `${record.start_date} to ${record.end_date}`}
              </td>
              <td style={{ padding: '12px' }}>
                {/* UX color coding for the analyst */}
                <span style={{
                  padding: '6px 12px',
                  borderRadius: '12px',
                  fontSize: '0.85rem',
                  fontWeight: 'bold',
                  backgroundColor: record.status === 'APPROVED' ? '#d4edda' : record.status === 'FLAGGED' ? '#f8d7da' : '#fff3cd',
                  color: record.status === 'APPROVED' ? '#155724' : record.status === 'FLAGGED' ? '#721c24' : '#856404'
                }}>
                  {record.status}
                </span>
              </td>
              <td style={{ padding: '12px' }}>
                {record.status === 'PENDING' && (
                  <button 
                    onClick={() => handleApprove(record.id)}
                    style={{ backgroundColor: '#007bff', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}
                  >
                    Approve Row
                  </button>
                )}
                {record.status === 'FLAGGED' && (
                  <button disabled style={{ backgroundColor: '#ccc', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px' }}>
                    Requires Fix
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default App