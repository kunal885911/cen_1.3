import React from 'react';
import '../styles/LoadingIndicator.css';

interface LoadingIndicatorProps {
  isLoading: boolean;
  message?: string;
  subtext?: string;
}

export const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({
  isLoading,
  message = 'Processing CAD model...',
  subtext = 'Generating geometry',
}) => {
  if (!isLoading) {
    return null;
  }

  return (
    <div className="loading-overlay">
      <div className="loading-container">
        <div className="spinner-wrapper"></div>
        <p className="loading-message">{message}</p>
        <p className="loading-subtext">{subtext}</p>
      </div>
    </div>
  );
};
