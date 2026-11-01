import React from 'react';

const Loading = ({ message = 'Loading...' }) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[300px] w-full p-6">
      <div className="w-10 h-10 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-3"></div>
      <p className="text-gray-600 text-sm font-medium">{message}</p>
    </div>
  );
};

export default Loading;
