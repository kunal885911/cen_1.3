import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './App';
import './styles/index.css';

const rootElement = document.getElementById('root');

if (!rootElement) {
  console.error('❌ Root element not found!');
  throw new Error('Root element not found');
}

try {
  console.log('✅ Root element found, mounting React...');
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
  console.log('✅ React app mounted successfully');
} catch (error) {
  console.error('❌ Error mounting React:', error);
  rootElement.innerHTML = `<div style="color: red; padding: 20px; font-family: monospace; white-space: pre-wrap;"><h2>Error Mounting App</h2>${error}</div>`;
}
