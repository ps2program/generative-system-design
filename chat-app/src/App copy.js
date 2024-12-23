import React from 'react';
import './App.css';
import ChatApp from './components/ChatApp';
import SideBar from './components/SideBar'; // Import the sidebar component
import { Grid } from '@mui/material'; // Import Grid from Material UI

function App() {
  return (
    <div className="App">
      <Grid container style={{ height: '100vh' }}>
        {/* Sidebar (1/4 of the screen) */}
        <Grid item xs={3}>
          <SideBar />
        </Grid>

        {/* ChatApp (3/4 of the screen) */}
        <Grid item xs={9}>
          <ChatApp />
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
