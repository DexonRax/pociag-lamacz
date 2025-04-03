import React from 'react';

export const Card = ({ children, className }) => (
    <div className={`p-4 rounded-2xl shadow-lg bg-gray-800 ${className}`}>
        {children}
    </div>
);

export const CardContent = ({ children }) => (
    <div className="text-white">
        {children}
    </div>
);
