"use client";
import { useState } from 'react';
import ReactMarkdown from 'react-markdown';

export default function TableView({ data, insights }) {
  const [isExpanded, setIsExpanded] = useState(true);

  if (!data || data.length === 0) return null;

  // Determine the type of data being displayed
  const getTableTitle = () => {
    const firstRow = data[0];
    if ('Place' in firstRow && 'Description' in firstRow) return 'Places to Visit';
    if ('Accommodation' in firstRow || 'Type' in firstRow) return 'Accommodations Summary';
    if ('Hospital' in firstRow || 'Medical_Type' in firstRow) return 'Hospitals Summary';
    if ('Restaurant' in firstRow || 'Cuisine' in firstRow) return 'Restaurants Summary';
    if ('Police_Station' in firstRow) return 'Police Stations Summary';
    if ('Weather_Description' in firstRow) return 'Weather Summary'
    return 'Data Summary';
  };

  const tableTitle = getTableTitle();

  return (
    <div className="my-4 bg-white rounded-lg overflow-hidden">
      <div 
        className="bg-gray-50 px-4 py-3 flex justify-between items-center cursor-pointer hover:bg-gray-100"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <h3 className="text-lg font-semibold text-gray-700">
          {tableTitle}
        </h3>
        <button className="text-gray-500 hover:text-gray-700">
          {isExpanded ? '▼' : '▶'}
        </button>
      </div>

      {isExpanded && (
        <div className="p-4">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  {Object.keys(data[0]).map((header) => (
                    <th
                      key={header}
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {header.replace('_', " ")}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {data.map((row, idx) => (
                  <tr key={idx} className="hover:bg-gray-50">
                    {Object.values(row).map((cell, cellIdx) => (
                      <td
                        key={cellIdx}
                        className="px-6 py-4 whitespace-normal text-sm text-gray-500"
                      >
                      {typeof cell === 'string' && cell.startsWith('http') ? (
                        <a 
                          href={cell}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:underline"
                        >
                          {cell}
                        </a>
                      ) : (typeof cell === 'number' && tableTitle === 'Weather Summary') ? (
                        <span>{cell.toFixed(2)}</span>
                      ) : (
                        cell
                      )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {insights && (
            <div className="mt-4 p-4 bg-blue-50 rounded-lg">
              <h4 className="text-md font-semibold text-blue-700 mb-2">
                Key Insights
              </h4>
              <div className="text-sm text-blue-600 prose prose-sm max-w-none prose-strong:text-blue-600 prose-em:text-blue-600 prose-headings:text-blue-600">
                <ReactMarkdown>{insights}</ReactMarkdown>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
