// import React, { useCallback, useRef, useState } from 'react';
import  { useCallback, useRef, useState } from 'react';
import ELK from 'elkjs/lib/elk.bundled.js';
import AIAssistanceDialog from './Components/AIAssistanceDialog';

import ChatIcon from '@mui/icons-material/Chat';
import { IconButton } from '@mui/material'; // Import IconButton
import { Button } from '@mui/material';
import '@xyflow/react/dist/style.css';
// import jsonData from './data.js';
// Define types for Node and Edge



// Define types for Node and Edge
// type Node = {
//   id: string;
//   data: {
//     label: string;
//     description: string;
//   };
//   position: { x: number; y: number };
// };


import {
  ReactFlow,
  ReactFlowProvider,
  Panel,
  useNodesState,
  useEdgesState,
  useReactFlow,
  ProOptions,
  reconnectEdge,
  Background,
  Controls,
  addEdge,
  type OnConnect,
  Connection,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

type Edge = {
  id: string;
  source: string;
  target: string;
  animated: boolean;
};

const elk:any = new ELK();
const jsonData = [
  {
    "index": "1",
    "title": "Safety and Security Features",
    "description": "The garage door opener should have safety features such as sensors to detect obstacles, automatic reversal in case of obstruction, and secure rolling code encryption for remote control signals."
  },
  {
    "index": "2",
    "title": "Power and Energy Efficiency",
    "description": "The garage door opener should be powered by a reliable motor with minimal energy consumption and low operating noise."
  },
  {
    "index": "3",
    "title": "Ease of Installation",
    "description": "The garage door opener should have a simple and straightforward installation process, with clear instructions and minimal additional hardware required."
  },
  {
    "index": "4",
    "title": "Remote Control Functionality",
    "description": "The garage door opener should have a reliable remote control system with multiple frequencies and a range of at least 100 feet."
  },
  {
    "index": "5",
    "title": "Smart Home Integration",
    "description": "The garage door opener should be compatible with popular smart home systems, allowing for voice control and automated scheduling."
  },
  {
    "index": "6",
    "title": "Durable Construction and Materials",
    "description": "The garage door opener should be constructed with high-quality materials and have a durable design to withstand regular use and harsh weather conditions."
  },
  {
    "index": "7",
    "title": "Noise Reduction",
    "description": "The garage door opener should have noise-reducing features, such as soft-start and slow-stop functions, to minimize disturbance during operation."
  },
  {
    "index": "8",
    "title": "Maintenance and Repair",
    "description": "The garage door opener should be designed for easy maintenance and repair, with accessible components and clear troubleshooting instructions."
  }
];




const useLayoutedElements = () => {
  const { getNodes, setNodes, getEdges, fitView } = useReactFlow();
  const defaultOptions = {
    'elk.algorithm': 'layered',
    'elk.layered.spacing.nodeNodeBetweenLayers': 100,
    'elk.spacing.nodeNode': 80,
  };

  const getLayoutedElements = useCallback((options) => {
    const layoutOptions = { ...defaultOptions, ...options };
    const graph = {
      id: 'root',
      layoutOptions: layoutOptions,
      children: getNodes().map((node) => ({
        ...node,
        width: node.measured?.width || 150,
        height: node.measured?.height || 50,
      })),
      edges: getEdges(),
    };

    elk.layout(graph).then(({ children }) => {
      children.forEach((node) => {
        node.position = { x: node.x, y: node.y };
      });

      setNodes(children);
      window.requestAnimationFrame(() => {
        fitView();
      });
    });
  }, [getNodes, getEdges, setNodes, fitView]);

  return { getLayoutedElements };
};

const LayoutFlow = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [dialogNodeId, setDialogNodeId] = useState(null);
  const [nodeId, setNodeId] = useState('None'); // Initial nodeId
  const { getLayoutedElements } = useLayoutedElements();

  const proOptions: ProOptions = { account: 'paid-pro', hideAttribution: true };
  const edgeReconnectSuccessful = useRef(true);

  const onConnect: OnConnect = useCallback(
    (connection) => setEdges((edges) => addEdge(connection, edges)),
    [setEdges]
  );
console.log(dialogNodeId)

  const onReconnect = useCallback(
    (oldEdge: Edge, newConnection: Connection) => {
      edgeReconnectSuccessful.current = true;
      setEdges((els) => reconnectEdge(oldEdge, newConnection, els));
    },
    []
  );

  // Function to handle node click and create new nodes
  const onNodeClick = useCallback(
    (event, node) => {
      // Check if the clicked node is the AIAssistanceDialog node
      if (node.data.label === 'AIAssistanceDialog') {
        debugger
        console.log(event)
        setDialogNodeId(node.id); // Set the node ID to track which node was clicked
        setNodeId(node.id);
        setIsDialogOpen(true); // Open the dialog
      } else {
        // Create three new nodes, one of which is AIAssistanceDialog
        const newNodes = [
          {
            id: `node-${nodes.length + 1}`,
            position: {
              x: node.position.x + 100,
              y: node.position.y + 50,
            },
            data: { label: `Child Node 1` },
            type: 'default',
          },
          {
            id: `node-${nodes.length + 2}`,
            position: {
              x: node.position.x + 200,
              y: node.position.y + 100,
            },
            data: { label: `AIAssistanceDialog` },
            type: 'default',
          },
          {
            id: `node-${nodes.length + 3}`,
            position: {
              x: node.position.x + 300,
              y: node.position.y + 150,
            },
            data: { label: `Child Node 2` },
            type: 'default',
          },
        ];

        // Create edges connecting the new nodes
        const newEdges = [
          {
            id: `edge-${edges.length + 2}`,
            source: newNodes[0].id,
            target: newNodes[1].id,
            animated: true,
          },
          {
            id: `edge-${edges.length + 1}`,
            source: node.id,
            target: newNodes[0].id,
            animated: true,
          },

          {
            id: `edge-${edges.length + 3}`,
            source: newNodes[0].id,
            target: newNodes[2].id,
            animated: true,
          },
        ];

        setNodes((nds) => [...nds, ...newNodes]);
        setEdges((eds) => [...eds, ...newEdges]);
      }
    },
    [nodes, edges, setNodes, setEdges]
  );

  const loadJsonData = useCallback(() => {
    const newNodes = jsonData.map((item) => ({
      id: `node-${item.index}`,
      data: { label: item.title, description: item.description },
      position: { x: 0, y: 0 },
    }));

    const newEdges = jsonData.slice(1).map((item, idx) => ({
      id: `edge-${idx + 1}`,
      source: `node-${jsonData[idx].index}`,
      target: `node-${item.index}`,
    }));

    setNodes(newNodes);
    setEdges(newEdges);
  }, [setNodes, setEdges]);

  return (
    <ReactFlow
      snapToGrid
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      fitView
      colorMode="dark"
      proOptions={proOptions}
      onNodeClick={onNodeClick}
      onConnect={onConnect}
      onReconnect={onReconnect}
    >
      <Background />


      <div style={{ height: '50vh', display: 'flex', justifyContent: 'center' }}>


        <Panel position="top-left">
          <Button
            onClick={loadJsonData}
            sx={{
              backgroundColor: '#333',
              color: 'white',
              border: '2px solid #ccc',
              '&:hover': { backgroundColor: '#555' },
              padding: '8px 16px',
              margin: '5px',
              cursor: 'pointer',
            }}
          >
            Load JSON Data
          </Button>

          <Button
            onClick={() =>
              getLayoutedElements({
                'elk.algorithm': 'layered',
                'elk.direction': 'DOWN',
              })
            }
            sx={{
              backgroundColor: '#333',
              color: 'white',
              border: '2px solid #ccc',
              '&:hover': { backgroundColor: '#555' },
              padding: '8px 16px',
              margin: '5px',
              cursor: 'pointer',
            }}
          >
            Vertical Layout
          </Button>

          <Button
            onClick={() =>
              getLayoutedElements({
                'elk.algorithm': 'layered',
                'elk.direction': 'RIGHT',
              })
            }
            sx={{
              backgroundColor: '#333',
              color: 'white',
              border: '2px solid #ccc',
              '&:hover': { backgroundColor: '#555' },
              padding: '8px 16px',
              margin: '5px',
              cursor: 'pointer',
            }}
          >
            Horizontal Layout
          </Button>

          <Button
            onClick={() =>
              getLayoutedElements({
                'elk.algorithm': 'org.eclipse.elk.radial',
              })
            }
            sx={{
              backgroundColor: '#333',
              color: 'white',
              border: '2px solid #ccc',
              '&:hover': { backgroundColor: '#555' },
              padding: '8px 16px',
              margin: '5px',
              cursor: 'pointer',
            }}
          >
            Radial Layout
          </Button>

          <Button
            onClick={() =>
              getLayoutedElements({
                'elk.algorithm': 'org.eclipse.elk.force',
              })
            }
            sx={{
              backgroundColor: '#333',
              color: 'white',
              border: '2px solid #ccc',
              '&:hover': { backgroundColor: '#555' },
              padding: '8px 16px',
              margin: '5px',
              cursor: 'pointer',
            }}
          >
            Force Layout
          </Button>
        </Panel>
      </div>


      <Panel position="bottom-right">
        {/* Icon button to trigger the dialog */}
        <IconButton
          color="primary"
          onClick={() => setIsDialogOpen(true)} // Open the dialog on click
          style={{ position: 'fixed', bottom: 20, right: 20 }}
        >
          <ChatIcon fontSize="large" />
        </IconButton>

        {/* AI Assistance Dialog */}
        <AIAssistanceDialog
          isOpen={isDialogOpen}
          nodeId={nodeId} // Passing nodeId as a prop
          onClose={() => setIsDialogOpen(false)} // Close the dialog when the user clicks outside or closes it
        />
      </Panel>

      <Controls position="bottom-left" >
      </Controls>
    </ReactFlow>
  );
};

export default function App() {
  return (
    <ReactFlowProvider>
      <LayoutFlow />
    </ReactFlowProvider>
  );
}
