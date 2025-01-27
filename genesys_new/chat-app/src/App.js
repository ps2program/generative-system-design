import React, { useState, useEffect } from 'react';
import './App.css';
import ChatApp from './components/ChatApp';
import SideBar from './components/SideBar'; // Import the sidebar component
import { Grid } from '@mui/material'; // Import Grid from Material UI

function App() {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);
  const userId = "default_user"; // Replace with dynamic user ID if applicable

  const apiUrl = process.env.REACT_APP_API_URL || "http://127.0.0.1:5055";

  const fetchHistory = async () => {
    try {
      const response = await fetch(`${apiUrl}/get_history?user_id=${userId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setHistory(data.history);
      setError(null); // Reset error state on successful fetch
    } catch (err) {
      console.error('Error fetching history:', err);
      setError('Failed to fetch history. Please try again later.');
    }
  };

  useEffect(() => {
    fetchHistory(); // Fetch history when the component mounts
  }, [userId]); // Dependency array includes userId

  return (
    <div className="App">
      <Grid container style={{ height: '100vh' }}>
        {/* Sidebar (1/4 of the screen) */}
        <Grid item xs={3}>
          <SideBar history={history} error={error} /> {/* Pass history and error to Sidebar */}
        </Grid>

        {/* ChatApp (3/4 of the screen) */}
        <Grid item xs={9}>
          <ChatApp onMessageSent={fetchHistory} /> {/* Pass the fetchHistory function to ChatApp */}
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
