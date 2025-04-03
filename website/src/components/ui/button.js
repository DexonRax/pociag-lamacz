import React from 'react';

export const Button = ({ children, className, onClick }) => (
    <button
        onClick={onClick}
        className={`px-4 py-2 rounded-lg text-white bg-blue-600 hover:bg-blue-700 ${className}`}
    >
        {children}
    </button>
);
