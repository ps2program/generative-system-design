import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import hljs from "highlight.js";
import "highlight.js/styles/atom-one-dark.css";
import {
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Box,
  Grid,
  TextField,
  Button,
  Paper,
  CircularProgress,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from "@mui/material";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import LightModeIcon from "@mui/icons-material/LightMode";
import SendIcon from "@mui/icons-material/Send";
import DeleteIcon from "@mui/icons-material/Delete"; // Import Delete Icon
import "./ChatApp.css"; // Custom CSS for additional styling

function ChatApp({ onMessageSent }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [loading, setLoading] = useState(false);
  const [models, setModels] = useState([]); // State to store available models
  const [selectedModel, setSelectedModel] = useState(""); // State for selected model

  const apiUrl = process.env.REACT_APP_API_URL || "http://127.0.0.1:5055";

  useEffect(() => {
    document.querySelectorAll("pre code").forEach((block) => {
      hljs.highlightElement(block);
    });
  }, [messages]);

  const isJsonString = (str) => {
    try {
      JSON.parse(str);
      return true;
    } catch (e) {
      return false;
    }
  };

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const response = await fetch(`${apiUrl}/get_available_models`);
        const result = await response.json();
        const modelData = result.data.map((model) => ({
          id: model.id,
          name: model.id,
        }));
        setModels(modelData);
      } catch (error) {
        console.error("Error fetching available models:", error);
      }
    };

    fetchModels();
  }, [apiUrl]);

  const handleModelChange = async (event) => {
    const selectedModelName = event.target.value;
    setSelectedModel(selectedModelName);

    try {
      const response = await fetch(`${apiUrl}/change_model`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_name: selectedModelName }),
      });
      const result = await response.json();
      if (result.status === "success") {
        console.log(`Model changed to ${selectedModelName}`);
      } else {
        console.error(`Error: ${result.message}`);
      }
    } catch (error) {
      console.error("Error changing model:", error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();

    const userMessage = {
      role: "user",
      content: input,
      model: selectedModel,
    };
    setMessages([...messages, userMessage]);
    setInput("");

    setLoading(true);

    try {
      const response = await fetch(`${apiUrl}/predict_v1`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMessage.content,
          model: selectedModel,
        }),
      });

      const data = await response.json();
      let clientdata;

      if (typeof data.answer === "string" && isJsonString(data.answer)) {
        clientdata = JSON.parse(data.answer);
      } else {
        clientdata = { message: data.answer };
      }

      const aiMessage = {
        role: "ai",
        content: `\`\`\`json\n${JSON.stringify(clientdata, null, 2)}\n\`\`\``,
      };

      setMessages((prevMessages) => [...prevMessages, aiMessage]);
      onMessageSent();
    } catch (error) {
      console.error("Error fetching AI response:", error);
    }

    setLoading(false);
  };

  // Clear history function
  const clearHistory = async () => {
    try {
      const response = await fetch(`${apiUrl}/clear_history`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: "default_user" }), // You can adjust this with user-specific logic
      });

      const result = await response.json();
      if (result.status === "success") {
        console.log("Chat history cleared successfully.");
        onMessageSent();
        setMessages([]); // Clear the chat history in the UI
      } else {
        console.error(`Error: ${result.message}`);
      }
    } catch (error) {
      console.error("Error clearing history:", error);
    }
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <Box
      sx={{
        backgroundColor: isDarkMode ? "#121212" : "#f5f5f5",
        minHeight: "100vh",
        padding: 1,
      }}
    >
      <AppBar position="static" color="primary">
        <Toolbar>
          <Typography variant="h4" component="div" sx={{ flexGrow: 1 }}>
            xSystems AI Engine
          </Typography>

          <FormControl sx={{ minWidth: 200, ml: "auto" }}>
            <InputLabel id="model-select-label" sx={{ color: "inherit" }}>
              Select Model
            </InputLabel>
            <Select
              labelId="model-select-label"
              value={selectedModel}
              onChange={handleModelChange}
              label="Select Model"
              sx={{
                backgroundColor: "080e2c",
                color: "inherit",
                borderColor: "white",
                "& .MuiOutlinedInput-notchedOutline": {
                  borderColor: "white",
                },
                "&:hover .MuiOutlinedInput-notchedOutline": {
                  borderColor: "white",
                },
                "& .MuiSvgIcon-root": {
                  color: "white",
                },
              }}
            >
              {models.map((model) => (
                <MenuItem key={model.id} value={model.name}>
                  {model.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* <IconButton onClick={toggleDarkMode} color="inherit" sx={{ ml: 2 }}>
            {isDarkMode ? <LightModeIcon /> : <DarkModeIcon />}
          </IconButton> */}

          {/* Clear history button */}
          <IconButton onClick={clearHistory} color="inherit" sx={{ ml: 2 }}>
            <DeleteIcon />
          </IconButton>
        </Toolbar>
      </AppBar>

      <Box sx={{ mt: 3, display: "flex", justifyContent: "center" }}>
        <Grid container spacing={2} maxWidth="xl" sx={{ width: "100%" }}>
          <Grid item xs={12} md={8}>
            <Paper
              elevation={3}
              sx={{
                padding: 2,
                backgroundColor: isDarkMode ? "#333" : "#fff",
                width: "100%",
              }}
            >
              <Box
                id="chat-box"
                sx={{ maxHeight: "500px", overflowY: "auto", padding: 2 }}
              >
                {messages.map((msg, index) => (
                  <Box key={index} sx={{ mb: 2 }}>
                    <Paper
                      elevation={1}
                      sx={{
                        padding: 1,
                        backgroundColor:
                          msg.role === "user"
                            ? isDarkMode
                              ? "#fff7f7"
                              : "#e3f2fd"
                            : isDarkMode
                            ? "#666"
                            : "#ffffff",
                        width: "100%",
                      }}
                    >
                      <Typography variant="body1" sx={{ fontWeight: "bold" }}>
                        {msg.role === "user" ? "User" : "AI"}:
                      </Typography>
                      <Typography variant="body2">
                        {msg.role === "ai" ? (
                          <ReactMarkdown remarkPlugins={[remarkGfm]}>
                            {msg.content}
                          </ReactMarkdown>
                        ) : (
                          msg.content
                        )}
                      </Typography>
                    </Paper>
                  </Box>
                ))}

                {loading && (
                  <Box
                    display="flex"
                    justifyContent="center"
                    alignItems="center"
                    sx={{ mt: 2 }}
                  >
                    <CircularProgress />
                    <Typography variant="body1" sx={{ ml: 1 }}>
                      AI is thinking...
                    </Typography>
                  </Box>
                )}
              </Box>

              <Box
                component="form"
                onSubmit={sendMessage}
                sx={{ mt: 2, display: "flex" }}
              >
                <TextField
                  label="Ask your question"
                  variant="outlined"
                  fullWidth
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  disabled={loading}
                />

                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  sx={{ ml: 1 }}
                  disabled={loading || !input}
                  endIcon={<SendIcon />}
                >
                  Send
                </Button>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
}

export default ChatApp;
