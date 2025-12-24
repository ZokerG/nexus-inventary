import React from 'react';
import Sidebar from '../organisms/Sidebar';

const MainLayout = ({ children }) => {
  return (
    <div className="flex min-h-screen bg-[#0F1419]">
      <Sidebar />
      <div className="ml-64 flex-1 p-8">
        {children}
      </div>
    </div>
  );
};

export default MainLayout;
