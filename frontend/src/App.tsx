import React, { useState, useEffect } from 'react';
import { ModelSelector } from './components/ModelSelector';
import { ParameterForm } from './components/ParameterForm';
import { Result } from './components/Result';
import { LoadingIndicator } from './components/LoadingIndicator';
import { AssemblyBuilder } from './components/AssemblyBuilder';
import { apiService } from './services/apiService';
import { 
  ModelType, 
  GenerateResponse, 
  ShaftParams, 
  PlateParams, 
  FlangeParams, 
  LbracketParams, 
  UbracketParams,
  HousingParams,
  FlangedShaftParams
} from './types';
import './styles/App.css';

type AllParams = Partial<
  ShaftParams & PlateParams & FlangeParams & LbracketParams & UbracketParams & HousingParams & FlangedShaftParams
>;

const REQUIRED_FIELDS: Record<ModelType, (keyof AllParams)[]> = {
  shaft: ['diameter', 'length'],
  plate: ['length', 'width'],
  flange: ['inner_diameter'],
  lbracket: ['length_1', 'length_2', 'width'],
  ubracket: ['length', 'height', 'width'],
  housing: ['length', 'height', 'width'],
  flanged_shaft: ['left_diameter', 'left_length', 'flange_diameter', 'flange_thickness', 'right_diameter', 'right_length'],
};

export const App: React.FC = () => {
  console.log('App component is rendering!');
  const [mainTab, setMainTab] = useState<'single' | 'assembly'>('single');
  const [selectedModel, setSelectedModel] = useState<ModelType | null>(null);
  const [params, setParams] = useState<AllParams>({});
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<GenerateResponse | null>(null);
  const [theme, setTheme] = useState<'dark' | 'light'>(() => {
    if (typeof window !== 'undefined') {
      return (localStorage.getItem('cad-theme') as 'dark' | 'light') || 'dark';
    }
    return 'dark';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('cad-theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const handleModelSelect = (model: ModelType) => {
    setSelectedModel(model);
    setParams({}); // Reset parameters when model changes
    setResult(null); // Clear previous results
  };

  const handleParamsChange = (newParams: AllParams) => {
    setParams(newParams);
  };

  const isFormValid = (): boolean => {
    if (!selectedModel) return false;
    const requiredFields = REQUIRED_FIELDS[selectedModel];
    return requiredFields.every(field => params[field] !== undefined);
  };

  const validateGeometry = (): string | null => {
    switch (selectedModel) {
      case 'shaft':
        if (params.length! > params.diameter! * 20) {
          return `Geometry Failure: Shaft length (${params.length}mm) cannot exceed 20x diameter (${params.diameter}mm).`;
        }
        break;
      case 'plate':
        if (params.length! > params.width! * 4) {
          return "Geometry Failure: Plate aspect ratio (L/W) must be 4:1 or less.";
        }
        break;
      case 'lbracket':
        if (params.length_1! < params.width! || params.length_2! < params.width!) {
          return "Geometry Failure: Arm lengths must be >= Width (B).";
        }
        break;
      case 'ubracket':
        if (params.length! < params.width! || params.height! < params.width!) {
          return "Geometry Failure: Base length and height must be >= Width (B).";
        }
        break;
      case 'housing':
        const min_side = Math.min(params.length!, params.height!, params.width!);
        const derived_wall = Math.max(6.0, (0.1 * min_side) + 7.5);
        if (derived_wall >= (min_side * 0.4)) {
          return "Geometry Failure: Internal dimensions are too small to accommodate required wall thickness.";
        }
        break;
      case 'flanged_shaft':
        if (params.flange_diameter! <= params.left_diameter! || params.flange_diameter! <= params.right_diameter!) {
          return "Geometry Failure: Flange diameter must be strictly greater than both left and right shaft diameters.";
        }
        break;
    }
    return null;
  };

  const handleGenerate = async () => {
    if (!selectedModel || !isFormValid()) {
      alert('Please fill in all required parameters');
      return;
    }

    const geometryError = validateGeometry();
    if (geometryError) {
      setResult({
        success: false,
        message: 'Validation Failed',
        error: geometryError
      });
      return;
    }

    setIsLoading(true);
    setResult(null);

    const requestParams: any = {};
    const requiredFields = REQUIRED_FIELDS[selectedModel];
    requiredFields.forEach(field => {
      requestParams[field] = params[field];
    });

    const response = await apiService.generateCAD(selectedModel, requestParams);
    setResult(response);
    setIsLoading(false);
  };

  const handleReset = () => {
    setSelectedModel(null);
    setParams({});
    setResult(null);
  };

  // Show result if available
  if (result) {
    return (
      <div className="app">
        <button
          className="theme-toggle"
          onClick={toggleTheme}
          aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
          title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
        >
          {theme === 'dark' ? '☀️' : '🌙'}
        </button>
        <Result result={result} onReset={handleReset} />
      </div>
    );
  }

  return (
    <div className="app">
      <button
        className="theme-toggle"
        onClick={toggleTheme}
        aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
        title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
      >
        {theme === 'dark' ? '☀️' : '🌙'}
      </button>
      <div className="container">
        <header className="app-header">
          <h1>CAD Automation System</h1>
          <p className="app-subtitle">Generate parametric CAD models with ease</p>
        </header>

        <main className="app-main">
          <div className="main-tabs" style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginBottom: '2rem' }}>
            <button 
              className={`btn ${mainTab === 'single' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setMainTab('single')}
            >
              Single Part Generation
            </button>
            <button 
              className={`btn ${mainTab === 'assembly' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setMainTab('assembly')}
            >
              Assembly Builder
            </button>
          </div>

          {mainTab === 'single' ? (
            <>
              <ModelSelector
                selectedModel={selectedModel}
                onSelectModel={handleModelSelect}
                disabled={isLoading}
              />

              <form onSubmit={(e) => { e.preventDefault(); handleGenerate(); }}>
                <ParameterForm
                  modelType={selectedModel}
                  params={params}
                  onParamsChange={handleParamsChange}
                  isLoading={isLoading}
                />

                <div className="action-button-container">
                  <button
                    type="submit"
                    className="btn btn-primary btn-large"
                    disabled={!isFormValid() || isLoading}
                  >
                    {isLoading ? 'Generating...' : 'Generate CAD Model'}
                  </button>
                </div>
              </form>
            </>
          ) : (
            <AssemblyBuilder />
          )}
        </main>

        <footer className="app-footer">
          <p>&copy; 2026 CAD Automation System v1.3. All rights reserved.</p>
        </footer>
      </div>

      <LoadingIndicator isLoading={isLoading} />
    </div>
  );
};
