import React from "react";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

function Sidebar({ history, error }) {
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
            <Typography variant="body1">
              <strong>{item.title}</strong>
            </Typography>
            {typeof item.description === "object" ? (
              Object.entries(item.description).map(([key, value]) => (
                <Typography variant="body2" key={key}>
                  <strong>{key}:</strong> {JSON.stringify(value)}
                </Typography>
              ))
            ) : (
              <Typography variant="body2">{item.description}</Typography>
            )}
          </div>
        ));
      } catch (err) {
        console.error("Error parsing items JSON:", err);
        return <Typography variant="body2">Invalid data format</Typography>;
      }
    } else {
      return <Typography variant="body2">{itemsString}</Typography>;
    }
  };

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h6" component="div" sx={{ flexGrow: 0 }}>
        Chat History
      </Typography>
      <div style={{ overflowY: 'auto', flexGrow: 1, padding: '10px' }}>
        {error ? (
          <p>{error}</p>
        ) : (
          history.map((entry, index) => {
          const { question: label, answer: itemsString, timestamp } = entry;


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
    </div>
  );
}

export default Sidebar;
