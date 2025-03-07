import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Graph = ({ data, config }) => {
  if (!data || !config) return <p>No data available</p>;

  const { xAxis, yAxis, graphType } = config;

  return (
    <div className="w-full h-96">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey={xAxis} 
            label={{ value: xAxis, position: 'bottom' }}
          />
          <YAxis 
            label={{ value: yAxis, angle: -90, position: 'left' }}
          />
          <Tooltip 
            formatter={(value, name) => [`$${value.toFixed(2)}`, name]}
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #ccc',
              borderRadius: '4px',
              padding: '10px'
            }}
          />
          <Line 
            type="monotone" 
            dataKey={yAxis} 
            stroke="#8884d8" 
            strokeWidth={2}
            dot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Graph;
