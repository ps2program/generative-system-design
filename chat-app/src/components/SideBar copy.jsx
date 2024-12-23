import React, { useState, useEffect } from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

function Sidebar() {
    const [history, setHistory] = useState([]);
    const [error, setError] = useState(null);
    const userId = "default_user"; // Replace with dynamic user ID if applicable

    const fetchHistory = async () => {
        try {
            const response = await fetch(`http://localhost:5000/get_history?user_id=${userId}`);
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
        fetchHistory(); // Call fetchHistory when the component mounts or userId changes
    }, [userId]); // Dependency array includes userId

    const isJsonString = (str) => {
        try {
            JSON.parse(str);
            return true;
        } catch (e) {
            return false;
        }
    };

    const renderItems = (itemsString) => {
        if (!itemsString) {
            return <Typography variant="body2">No items available</Typography>;
        }

        if (isJsonString(itemsString)) {
            try {
                const items = JSON.parse(itemsString);
                return items.map((item, index) => (
                    <div key={index}>
                        <Typography variant="body1"><strong>{item.title}</strong></Typography>
                        <Typography variant="body2">{item.description}</Typography>
                    </div>
                ));
            } catch (err) {
                console.error('Error parsing items JSON:', err);
                return <Typography variant="body2">Invalid data format</Typography>;
            }
        } else {
            // If it's not valid JSON, return the string directly
            return <Typography variant="body2">{itemsString}</Typography>;
        }
    };

    return (
        <div>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                Chat History
            </Typography>
            {error ? (
                <p>{error}</p>
            ) : (
                history.map((entry, index) => {
                    const [label, itemsString, timestamp] = entry;

                    return (
                        <Accordion key={index}>
                            <AccordionSummary
                                expandIcon={<ExpandMoreIcon />}
                                aria-controls={`panel${index}-content`}
                                id={`panel${index}-header`}
                            >
                                <Typography>{label}</Typography>
                            </AccordionSummary>
                            <AccordionDetails>
                                <Typography variant="caption">{timestamp}</Typography>
                                {renderItems(itemsString)}
                            </AccordionDetails>
                        </Accordion>
                    );
                })
            )}
        </div>
    );
}

export default Sidebar;
