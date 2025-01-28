import React, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, TextField, Button, ThemeProvider, createTheme } from '@mui/material';

const darkTheme = createTheme({
  palette: {
    mode: 'dark', // This sets the theme to dark mode
  },
});

const AIAssistanceDialog = ({ isOpen, nodeId, onClose, onLLMResponse }) => {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (nodeId) {
      setInput(`Node ID: ${nodeId}`);
    }
  }, [nodeId]);

  const handleInputChange = (event) => setInput(event.target.value);

  const handleSubmit = async () => {
    setLoading(true);
    const requestBody = {
      message: {
        question: input || 'garage door opener',
        questionType: {
          type: 'list',
          subType: 'products',
        },
      },
    };

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();
      const node_data = JSON.parse(data.answer.content)
      onLLMResponse(node_data); // Pass the response to the parent
    } catch (error) {
      console.error('Error:', error);
      onLLMResponse({ error: 'Something went wrong. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={darkTheme}>
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
            InputLabelProps={{ style: { color: '#fff' } }}
            InputProps={{ style: { color: '#fff' } }}
          />
          <Button
            onClick={handleSubmit}
            variant="contained"
            color="primary"
            style={{ marginTop: '10px' }}
            disabled={loading}
          >
            {loading ? 'Submitting...' : 'Submit'}
          </Button>
        </DialogContent>
      </Dialog>
    </ThemeProvider>
  );
};

export default AIAssistanceDialog;
