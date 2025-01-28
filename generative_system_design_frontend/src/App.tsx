// import React, { useCallback, useRef, useState } from 'react';
import { useCallback, useRef, useState } from 'react';
import ELK from 'elkjs/lib/elk.bundled.js';
import AIAssistanceDialog from './Components/AIAssistanceDialog';

import ChatIcon from '@mui/icons-material/Chat';
import { IconButton } from '@mui/material'; // Import IconButton
import { Button } from '@mui/material';
import '@xyflow/react/dist/style.css';
// import jsonData from './data.js';
// Define types for Node and Edge

import axios from 'axios';

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

const elk: any = new ELK();

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
  const [dialogNodeId, setDialogNodeId] = useState('node-1');
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

  // Fetch data from the API endpoint
  const loadJsonData = useCallback(async () => {
    try {
      const response = await axios.post("http://localhost:5050/predict", {
        user_id: "default_user", // Replace with appropriate user_id if needed
        message: { question: "Electric Bike" }, 
      });

      const jsonData = JSON.parse(response.data.answer.content); // Assuming the data is in the "answer" field
      const newNodes = jsonData.map((item, index) => ({
        id: `node-${index + 1}`,
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
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }, [setNodes, setEdges]);


  // Callback to handle LLM response
  // Callback to handle LLM response
  const handleLLMResponse = (response: any) => {
    if (response) {
      // Create the "System" node as the root node only if there are no existing nodes
      const systemNode = {
        id: 'node-0', // Root node id
        data: { label: 'System', description: 'The root node for all other nodes' },
        position: { x: 150, y: 150 }, // Position it at the center or any desired position
      };

      // Check if there are already existing nodes
      const isExistingNodes = nodes.length > 0;

      // Create new nodes from the LLM response
      const newNodes = response.map((item, index) => ({
        id: `node-${isExistingNodes ? nodes.length + index + 1 : index + 1}`, // Node IDs starting from 1, adjust based on existing nodes
        data: { label: item.title || `Node ${index + 1}`, description: item.description || '' },
        position: { x: Math.random() * 300, y: Math.random() * 300 },
      }));

      // Create edges based on whether there are existing nodes or not
      const newEdges = newNodes.map((node) => ({
        id: `edge-${node.id}`,
        source: isExistingNodes ? dialogNodeId : systemNode.id, // Use dialogNodeId if nodes exist, otherwise use systemNode
        target: node.id,
        animated: true,
      }));

      // Set the nodes and edges state
      setNodes((nds) => [
        ...(!isExistingNodes ? [systemNode] : []), // Add systemNode only if no nodes exist
        ...nds,
        ...newNodes,
      ]);
      setEdges((eds) => [...eds, ...newEdges]); // Add the edges connecting dialogNodeId or systemNode to new nodes
    }

    // Close the dialog after processing the LLM response
    setIsDialogOpen(false);
  };



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
            Electric Bike
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
            Vertical
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
            Horizontal
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
            Radial
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
            Force
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

        <AIAssistanceDialog
          isOpen={isDialogOpen}
          nodeId={nodeId} // Passing nodeId as a prop
          onClose={() => setIsDialogOpen(false)} // Close the dialog when the user clicks outside or closes it
          onLLMResponse={handleLLMResponse} // Passing handleLLMResponse as the onLLMResponse prop
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
