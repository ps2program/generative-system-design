import React, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, TextField, IconButton, Button, ThemeProvider, createTheme, Typography, Box } from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';

// Create a dark theme using Material-UI's createTheme
const darkTheme = createTheme({
  palette: {
    mode: 'dark', // This sets the theme to dark mode
  },
});

const AIAssistanceDialog = ({ isOpen, nodeId, onClose }) => {
  const [open, setOpen] = useState(isOpen);
  const [input, setInput] = useState('');
  const [response, setResponse] = useState(null); // To store the API response
  const [loading, setLoading] = useState(false); // To track loading state

  // Set the input field when the nodeId changes
  useEffect(() => {
    if (nodeId) {
      setInput(`Node ID: ${nodeId}`);
    }
  }, [nodeId]);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const handleInputChange = (event) => setInput(event.target.value);

  const handleSubmit = async () => {
    setLoading(true);
    const requestBody = {
      message: {
        question: input || "garage door opener", // Use the input or default to "garage door opener"
        questionType: {
          type: "list",
          subType: "products"
        }
      }
    };
  
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/predict`, {  // Use the environment variable
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });
  
      const data = await response.json();
      setResponse(data); // Store the response in the state
    } catch (error) {
      console.error("Error:", error);
      setResponse({ error: "Something went wrong. Please try again." });
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <ThemeProvider theme={darkTheme}>
      <div>
        <Dialog open={isOpen} onClose={onClose}>
          <DialogTitle>AI Assistance</DialogTitle>
          <DialogContent>
            <TextField
              fullWidth
              label="Ask AI"
              value={input}
              onChange={handleInputChange}
              variant="outlined"
              margin="dense"
              InputLabelProps={{
                style: { color: '#fff' },
              }}
              InputProps={{
                style: { color: '#fff' },
              }}
            />
            <Button
              onClick={handleSubmit}
              variant="contained"
              color="primary"
              style={{ marginTop: '10px' }}
              disabled={loading} // Disable button while loading
            >
              {loading ? 'Submitting...' : 'Submit'}
            </Button>
            {response && (
              <Box mt={2}>
                <Typography variant="h6" color="primary">
                  Response:
                </Typography>
                <Typography variant="body1" color="textSecondary">
                  {response.error ? response.error : JSON.stringify(response, null, 2)}
                </Typography>
              </Box>
            )}
          </DialogContent>
        </Dialog>
      </div>
    </ThemeProvider>
  );
};

export default AIAssistanceDialog;
