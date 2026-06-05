import React from 'react';
import { GenerateResponse } from '../types';
import { apiService } from '../services/apiService';
import '../styles/Result.css';

interface ResultProps {
  result: GenerateResponse | null;
  onReset: () => void;
}

export const Result: React.FC<ResultProps> = ({ result, onReset }) => {
  if (!result) {
    return null;
  }

  const handleDownload = () => {
    if (result.fileUrl) {
      apiService.downloadFile(result.fileUrl, result.downloadName || 'cad-output.zip');
    }
  };

  return (
    <div className={`result-container ${result.success ? 'success' : 'error'}`}>
      <div className="result-content">
        <div className="result-icon">
          {result.success ? (
            <div className="success-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
            </div>
          ) : (
            <div className="error-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </div>
          )}
        </div>

        <h2 className="result-title">
          {result.success ? 'Generation Successful' : 'Generation Failed'}
        </h2>

        <p className="result-message">{result.message}</p>

        {result.success && result.outputFiles && result.outputFiles.length > 0 && (
          <div className="file-chips">
            {result.outputFiles.map(file => (
              <span key={file} className="file-chip">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                {file}
              </span>
            ))}
          </div>
        )}

        {result.error && (
          <div className="result-error">
            <strong>System Error:</strong><br/>
            {result.error}
          </div>
        )}

        <div className="result-actions">
          {result.success && result.fileUrl && (
            <button className="btn btn-primary btn-download" onClick={handleDownload}>
              Download CAD Package
            </button>
          )}

          <button className="btn btn-secondary" onClick={onReset}>
            Start New Configuration
          </button>
        </div>
      </div>
    </div>
  );
};
