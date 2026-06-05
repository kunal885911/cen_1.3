import React from 'react';
import { ModelType } from '../types';
import '../styles/ModelSelector.css';

interface ModelSelectorProps {
  selectedModel: ModelType | null;
  onSelectModel: (model: ModelType) => void;
  disabled?: boolean;
}

const MODEL_OPTIONS: Array<{
  id: ModelType;
  name: string;
  description: string;
  icon: React.ReactNode;
  tags: string[];
}> = [
  {
    id: 'shaft',
    name: 'Cylindrical Shaft',
    description: 'Precision rotating machine element for power transmission and bearing support.',
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="6" width="20" height="12" rx="2" />
        <path d="M6 6v12" />
        <path d="M18 6v12" />
        <path d="M10 6v12" />
        <path d="M14 6v12" />
      </svg>
    ),
    tags: ['Length', 'Diameter']
  },
  {
    id: 'plate',
    name: 'Structural Plate',
    description: 'Load-bearing flat component utilized for mounting, separation, and foundational bases.',
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M3 20h18L21 4H3z" />
        <path d="M3 12h18" />
        <path d="M9 4v16" />
        <path d="M15 4v16" />
      </svg>
    ),
    tags: ['Length', 'Width', 'Thickness']
  },
  {
    id: 'flange',
    name: 'Mechanical Flange',
    description: 'Connection component for piping and shafts, providing a rim for attachment.',
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="9" />
        <circle cx="12" cy="12" r="3" />
        <circle cx="12" cy="6" r="1.5" />
        <circle cx="12" cy="18" r="1.5" />
        <circle cx="6" cy="12" r="1.5" />
        <circle cx="18" cy="12" r="1.5" />
      </svg>
    ),
    tags: ['Diameter', 'Thickness']
  },
  {
    id: 'lbracket',
    name: 'L-Type Bracket',
    description: 'Angle-shaped structural support for 90-degree joints and mounting.',
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M8 4v12h8" />
        <path d="M4 4v16h12" />
        <path d="M4 4h4" />
        <path d="M16 16h4" />
        <path d="M20 16L16 20" />
      </svg>
    ),
    tags: ['L1', 'L2', 'Thickness']
  },
  {
    id: 'ubracket',
    name: 'U-Type Bracket',
    description: 'Three-sided support component for clamping and securing elements.',
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M4 4v12h16V4" />
        <path d="M8 4v8h8V4" />
        <path d="M4 4h4" />
        <path d="M16 4h4" />
      </svg>
    ),
    tags: ['L', 'H', 'W', 'Thickness']
  },
  {
    id: 'housing',
    name: 'Housing Component',
    description: 'Enclosed structural housing for protecting and containing mechanical elements.',
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="4" width="20" height="16" rx="2" />
        <rect x="4" y="6" width="16" height="12" rx="1" />
        <path d="M6 8h12" />
        <path d="M6 12h12" />
        <path d="M6 16h12" />
      </svg>
    ),
    tags: ['Length', 'Height', 'Width', 'Wall Thickness']
  },
  {
    id: 'flanged_shaft',
    name: 'Flanged Shaft',
    description: 'Coaxial shaft assembly featuring a central flange for coupling or mounting.',
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="10" width="6" height="4" rx="1" />
        <rect x="16" y="10" width="6" height="4" rx="1" />
        <rect x="8" y="6" width="8" height="12" rx="2" />
      </svg>
    ),
    tags: ['Left', 'Right', 'Flange']
  },
];

export const ModelSelector: React.FC<ModelSelectorProps> = ({
  selectedModel,
  onSelectModel,
  disabled = false,
}) => {
  return (
    <div className="model-selector">
      <div className="form-label">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <span>Model Configuration Base</span>
      </div>
      
      <div className="model-cards">
        {MODEL_OPTIONS.map((model) => (
          <button
            key={model.id}
            className={`model-card ${selectedModel === model.id ? 'selected' : ''}`}
            onClick={() => onSelectModel(model.id)}
            disabled={disabled}
            type="button"
          >
            <div className="model-card-check">✓</div>
            
            <div className="model-card-icon">
              {model.icon}
            </div>
            
            <div className="model-card-header">
              <h3>{model.name}</h3>
            </div>
            
            <p className="model-card-description">{model.description}</p>
            
            <div className="model-card-tags">
              {model.tags.map(tag => (
                <span key={tag} className="model-card-tag">{tag}</span>
              ))}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};
