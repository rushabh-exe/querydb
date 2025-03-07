import React, { useState } from 'react';
import Table from './components/Table.jsx';
import Graph from './components/Graph.jsx';
import PieieChart from './components/PieChart.jsx';
import HumanReadableResponse from './components/HumanReadableResponse.jsx';
const App = () => {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSendPrompt = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      if (!res.ok) throw new Error('Network response was not ok');
      
      const data = await res.json();
      
      if (!data.success) {
        throw new Error(data.message || 'Query execution failed');
      }
      console.log(data);
      setResponse(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8 bg-gray-100">
      <div className="max-w-4xl mx-auto space-y-6">
        <h1 className="text-2xl font-bold text-gray-800">SQL Visualization Chat</h1>

        <div className="space-y-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Enter your query..."
              className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleSendPrompt}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              Send
            </button>
          </div>

          {error && (
            <div className="p-4 bg-red-100 text-red-700 rounded-lg">
              Error: {error}
            </div>
          )}

          {isLoading ? (
            <div className="p-4 bg-blue-100 text-blue-700 rounded-lg">
              Loading...
            </div>
          ) : (
            response && (
              <>
                <div className="bg-white p-6 rounded-lg shadow">
                  {response.visualization_type === 'table' && (
                    <Table 
                      columns={response.data.columns} 
                      rows={response.data.rows} 
                    />
                  )}
                  {response.visualization_type === 'graph' && (
                    <Graph
                      data={response.data.data} 
                      config={response.data.config}  
                     />
                  )}
                  {response.visualization_type === 'pie' && (
                    <PieieChart data={response.data.data} />
                  )}
                </div>
                
                <div className="mt-6">
                  <h2>Human Like Response</h2>
                  {response.human_readable && (
                    <HumanReadableResponse rawResponse={response.human_readable} />
                  )}  
                  {/* <h2 className="text-lg font-semibold mb-4">Raw Data</h2>
                  <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm max-h-48">
                    {JSON.stringify(response.raw, null, 2)}
                  </pre> */}
                </div>
              </>
            )
          )}
        </div>
      </div>
    </div>
  );
};

export default App;