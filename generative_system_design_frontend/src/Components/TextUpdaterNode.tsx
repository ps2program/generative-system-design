import React, { useCallback } from 'react';
import { Handle, Position } from '@xyflow/react';

const handleStyle = { left: 10 };

type TextUpdaterNodeProps = {
  data: {
    label: string;
    onLabelChange: (label: string) => void;
  };
};

const TextUpdaterNode: React.FC<TextUpdaterNodeProps> = ({ data }) => {
  const onChange = useCallback((evt: React.ChangeEvent<HTMLInputElement>) => {
    data.onLabelChange(evt.target.value);
  }, [data]);

  return (
    <>
      <Handle type="target" position={Position.Top} />
      <div style={{ padding: '10px', border: '1px solid #ccc', borderRadius: '5px' }}>
        <label htmlFor="text">Node Label:</label>
        <input
          id="text"
          name="text"
          value={data.label}
          onChange={onChange}
          className="nodrag"
          style={{ marginLeft: '10px', padding: '5px' }}
        />
      </div>
      <Handle type="source" position={Position.Bottom} id="a" />
      <Handle type="source" position={Position.Bottom} id="b" style={handleStyle} />
    </>
  );
};

export default TextUpdaterNode;
