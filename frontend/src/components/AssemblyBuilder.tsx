import React, { useState, useRef } from 'react';
import { ModelType, PartConfig, ConnectionPair, AssemblyRequest, GenerateResponse, ModelParams } from '../types';
import { apiService } from '../services/apiService';
import { Result } from './Result';
import { LoadingIndicator } from './LoadingIndicator';
import { ParameterForm } from './ParameterForm';
import '../styles/App.css'; // Reuse existing styles

const CONNECTOR_MAP: Partial<Record<ModelType, string[]>> = {
  shaft: ['left_end', 'right_end'],
  flange: ['back_center', 'front_center', 'bolt_holes'],
  plate: ['top_face', 'bottom_face'],
  lbracket: ['face_1', 'face_2'],
  ubracket: ['base_face', 'left_wall', 'right_wall'],
  housing: ['top_face', 'bottom_face', 'front_face']
};

const CONNECTOR_TYPES: Partial<Record<ModelType, Record<string, string>>> = {
  shaft: { left_end: 'cylindrical', right_end: 'cylindrical' },
  flange: { back_center: 'cylindrical', front_center: 'cylindrical', bolt_holes: 'hole' },
  plate: { top_face: 'face', bottom_face: 'face' },
  lbracket: { face_1: 'face', face_2: 'face' },
  ubracket: { base_face: 'face', left_wall: 'face', right_wall: 'face' },
  housing: { top_face: 'face', bottom_face: 'face', front_face: 'face' }
};

const MATING_RULES: Record<string, string[]> = {
  cylindrical: ['cylindrical', 'hole', 'face'],
  hole: ['cylindrical', 'face'],
  face: ['face', 'hole', 'cylindrical']
};

interface AssemblyBuilderProps {
  onBack?: () => void;
}

export const AssemblyBuilder: React.FC<AssemblyBuilderProps> = () => {
  const [mode, setMode] = useState<'manual' | 'config'>('manual');
  
  // Manual Builder State
  const [assemblyName, setAssemblyName] = useState('MyAssembly');
  const [parts, setParts] = useState<PartConfig[]>([]);
  const [connections, setConnections] = useState<ConnectionPair[]>([]);
  
  // Current part being added
  const [currentPartId, setCurrentPartId] = useState('');
  const [currentPartType, setCurrentPartType] = useState<ModelType>('shaft');
  const [currentPartParams, setCurrentPartParams] = useState<Partial<ModelParams>>({});
  
  const [conn1PartId, setConn1PartId] = useState('');
  const [conn1Connector, setConn1Connector] = useState('');
  const [conn2PartId, setConn2PartId] = useState('');
  const [conn2Connector, setConn2Connector] = useState('');

  // Execution state
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<GenerateResponse | null>(null);

  // Config Upload State
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleAddPart = () => {
    if (!currentPartId) {
      alert('Please provide a unique part ID.');
      return;
    }
    if (parts.some(p => p.id === currentPartId)) {
      alert('Part ID already exists.');
      return;
    }

    const REQUIRED_FIELDS: Partial<Record<ModelType, string[]>> = {
      shaft: ['diameter', 'length'],
      plate: ['length', 'width'],
      flange: ['inner_diameter'],
      lbracket: ['length_1', 'length_2', 'width'],
      ubracket: ['length', 'height', 'width'],
      housing: ['length', 'height', 'width']
    };

    const requiredFields = REQUIRED_FIELDS[currentPartType] || [];
    const isFormValid = requiredFields.every(field => (currentPartParams as any)[field] !== undefined);
    if (!isFormValid) {
      alert('Please fill in all required parameters for this part.');
      return;
    }

    let geometryError: string | null = null;
    const params = currentPartParams as any;
    switch (currentPartType) {
      case 'shaft':
        if (params.length > params.diameter * 20) {
          geometryError = `Geometry Failure: Shaft length (${params.length}mm) cannot exceed 20x diameter (${params.diameter}mm).`;
        }
        break;
      case 'plate':
        if (params.length > params.width * 4) {
          geometryError = "Geometry Failure: Plate aspect ratio (L/W) must be 4:1 or less.";
        }
        break;
      case 'lbracket':
        if (params.length_1 < params.width || params.length_2 < params.width) {
          geometryError = "Geometry Failure: Arm lengths must be >= Width (B).";
        }
        break;
      case 'ubracket':
        if (params.length < params.width || params.height < params.width) {
          geometryError = "Geometry Failure: Base length and height must be >= Width (B).";
        }
        break;
      case 'housing':
        const min_side = Math.min(params.length, params.height, params.width);
        const derived_wall = Math.max(6.0, (0.1 * min_side) + 7.5);
        if (derived_wall >= (min_side * 0.4)) {
          geometryError = "Geometry Failure: Internal dimensions are too small to accommodate required wall thickness.";
        }
        break;
    }

    if (geometryError) {
      alert(geometryError);
      return;
    }
    if (parts.some(p => p.id === currentPartId)) {
      alert('Part ID already exists.');
      return;
    }
    setParts([...parts, { id: currentPartId, type: currentPartType, parameters: currentPartParams }]);
    setCurrentPartId('');
    setCurrentPartParams({});
  };

  const handleRemovePart = (id: string) => {
    setParts(parts.filter(p => p.id !== id));
  };

  const getValidConnectors = (p2Type: ModelType) => {
    const allConns = CONNECTOR_MAP[p2Type] || [];
    if (!conn1PartId || !conn1Connector) return allConns;
    
    const p1 = parts.find(p => p.id === conn1PartId);
    if (!p1 || !CONNECTOR_TYPES[p1.type]) return allConns;
    
    const conn1Type = CONNECTOR_TYPES[p1.type]![conn1Connector];
    if (!conn1Type) return allConns;

    const allowedMates = MATING_RULES[conn1Type] || [];
    
    return allConns.filter(c => {
      const typeMap = CONNECTOR_TYPES[p2Type];
      if (!typeMap) return false;
      const cType = typeMap[c];
      return allowedMates.includes(cType);
    });
  };

  const handleAddConnection = () => {
    if (!conn1PartId || !conn1Connector || !conn2PartId || !conn2Connector) {
      alert('Please specify both parts and their connectors.');
      return;
    }
    const c1 = `${conn1PartId}.${conn1Connector}`;
    const c2 = `${conn2PartId}.${conn2Connector}`;
    
    if (c1 === c2) {
      alert('Cannot connect a part to itself on the same connector.');
      return;
    }

    setConnections([...connections, [c1, c2]]);
    setConn1PartId('');
    setConn1Connector('');
    setConn2PartId('');
    setConn2Connector('');
  };

  const handleRemoveConnection = (index: number) => {
    setConnections(connections.filter((_, i) => i !== index));
  };

  const handleGenerateManual = async () => {
    if (parts.length === 0) {
      alert('Please add at least one part.');
      return;
    }
    setIsLoading(true);
    setResult(null);
    const request: AssemblyRequest = {
      assembly_name: assemblyName,
      parts,
      connections,
      export_modes: ['assembly', 'multibody']
    };
    const response = await apiService.generateAssembly(request);
    setResult(response);
    setIsLoading(false);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleGenerateConfig = async () => {
    if (!selectedFile) {
      alert('Please select a configuration file.');
      return;
    }
    setIsLoading(true);
    setResult(null);
    const response = await apiService.generateAssemblyFromConfig(selectedFile);
    setResult(response);
    setIsLoading(false);
  };

  if (result) {
    const COMPONENT_COLORS: Record<string, { r: number, g: number, b: number, name: string }> = {
      shaft:          { r: 0.65, g: 0.65, b: 0.70, name: "Steel Gray" },
      flange:         { r: 0.80, g: 0.50, b: 0.20, name: "Brass Orange" },
      plate:          { r: 0.20, g: 0.55, b: 0.80, name: "Steel Blue" },
      cylinder:       { r: 0.30, g: 0.70, b: 0.40, name: "Anodized Green" },
      pipe:           { r: 0.70, g: 0.20, b: 0.20, name: "Oxide Red" },
      lbracket:       { r: 0.85, g: 0.75, b: 0.10, name: "Zinc Yellow" },
      ubracket:       { r: 0.50, g: 0.20, b: 0.70, name: "Anodized Purple" },
      housing:        { r: 0.20, g: 0.40, b: 0.30, name: "Gunmetal Green" }
    };

    return (
      <div className="app-main">
        <Result result={result} onReset={() => setResult(null)} />
        
        {parts.length > 0 && (
          <div className="color-legend" style={{ marginTop: '2rem', padding: '1rem', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-secondary)' }}>
            <h3 style={{ marginBottom: '1rem' }}>Assembly Color Legend</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {parts.map(p => {
                const color = COMPONENT_COLORS[p.type] || { r: 0.5, g: 0.5, b: 0.5, name: "Default Gray" };
                const rgbString = `rgb(${Math.round(color.r * 255)}, ${Math.round(color.g * 255)}, ${Math.round(color.b * 255)})`;
                return (
                  <li key={p.id} style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
                    <div style={{ width: '16px', height: '16px', backgroundColor: rgbString, border: '1px solid #000' }}></div>
                    <span style={{ fontWeight: 'bold', width: '100px' }}>{p.id}</span>
                    <span style={{ width: '150px' }}>— {color.name}</span>
                    <a href={result.fileUrl} style={{ color: 'var(--primary-color)' }}>individual/{p.id}.step</a>
                  </li>
                );
              })}
            </ul>
            <p style={{ marginTop: '1rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
              Open <strong>assembly_colored.step</strong> to see all parts together.<br/>
              Each part appears in its unique color shown above.<br/>
              Open individual .step files to inspect each part separately.
            </p>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="assembly-builder">
      <div className="tabs" style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
        <button 
          className={`btn ${mode === 'manual' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setMode('manual')}
        >
          Manual Builder
        </button>
        <button 
          className={`btn ${mode === 'config' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setMode('config')}
        >
          Config Upload
        </button>
      </div>

      {mode === 'manual' && (
        <div className="manual-builder">
          <div className="form-group">
            <label>Assembly Name</label>
            <input 
              type="text" 
              value={assemblyName} 
              onChange={e => setAssemblyName(e.target.value)} 
              className="param-input"
            />
          </div>

          <div className="builder-section" style={{ border: '1px solid var(--border-color)', padding: '1rem', borderRadius: '8px', marginBottom: '1rem' }}>
            <h3>Parts List ({parts.length})</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {parts.map(p => (
                <li key={p.id} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', background: 'var(--bg-tertiary)', padding: '0.5rem', borderRadius: '4px' }}>
                  <span><strong>{p.id}</strong> ({p.type})</span>
                  <button onClick={() => handleRemovePart(p.id)} className="btn btn-secondary" style={{ padding: '2px 8px' }}>Remove</button>
                </li>
              ))}
            </ul>

            <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px dashed var(--border-color)' }}>
              <h4>Add New Part</h4>
              <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
                <input 
                  type="text" 
                  placeholder="Part ID (e.g., shaft1)" 
                  value={currentPartId} 
                  onChange={e => setCurrentPartId(e.target.value)}
                  className="param-input"
                />
                <select 
                  value={currentPartType} 
                  onChange={e => {
                    setCurrentPartType(e.target.value as ModelType);
                    setCurrentPartParams({});
                  }}
                  className="param-input"
                >
                  <option value="shaft">Shaft</option>
                  <option value="flange">Flange</option>
                  <option value="plate">Plate</option>
                  <option value="lbracket">L-Bracket</option>
                  <option value="ubracket">U-Bracket</option>
                  <option value="housing">Housing</option>
                </select>
              </div>
              <ParameterForm 
                modelType={currentPartType} 
                params={currentPartParams as any} 
                onParamsChange={p => setCurrentPartParams(p)} 
              />
              <button onClick={handleAddPart} className="btn btn-secondary" style={{ marginTop: '1rem' }}>Add Part</button>
            </div>
          </div>

          <div className="builder-section" style={{ border: '1px solid var(--border-color)', padding: '1rem', borderRadius: '8px', marginBottom: '1rem' }}>
            <h3>Connections List ({connections.length})</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {connections.map((c, i) => (
                <li key={i} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', background: 'var(--bg-tertiary)', padding: '0.5rem', borderRadius: '4px' }}>
                  <span>{c[0]} &lt;--&gt; {c[1]}</span>
                  <button onClick={() => handleRemoveConnection(i)} className="btn btn-secondary" style={{ padding: '2px 8px' }}>Remove</button>
                </li>
              ))}
            </ul>

            <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px dashed var(--border-color)' }}>
              <h4>Add New Connection</h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                  <span style={{ width: '40px', fontWeight: 'bold' }}>From:</span>
                  <select 
                    value={conn1PartId} 
                    onChange={e => { setConn1PartId(e.target.value); setConn1Connector(''); }}
                    className="param-input"
                    style={{ flex: 1 }}
                  >
                    <option value="">Select Part...</option>
                    {parts.map(p => (
                      <option key={`c1-${p.id}`} value={p.id}>{p.id} ({p.type})</option>
                    ))}
                  </select>
                  <select 
                    value={conn1Connector} 
                    onChange={e => setConn1Connector(e.target.value)}
                    className="param-input"
                    style={{ flex: 1 }}
                    disabled={!conn1PartId}
                  >
                    <option value="">Select Connector...</option>
                    {conn1PartId && parts.find(p => p.id === conn1PartId) && 
                      CONNECTOR_MAP[parts.find(p => p.id === conn1PartId)!.type]?.map(c => (
                        <option key={c} value={c}>{c}</option>
                      ))
                    }
                  </select>
                </div>

                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                  <span style={{ width: '40px', fontWeight: 'bold' }}>To:</span>
                  <select 
                    value={conn2PartId} 
                    onChange={e => { setConn2PartId(e.target.value); setConn2Connector(''); }}
                    className="param-input"
                    style={{ flex: 1 }}
                  >
                    <option value="">Select Part...</option>
                    {parts.map(p => (
                      <option key={`c2-${p.id}`} value={p.id}>{p.id} ({p.type})</option>
                    ))}
                  </select>
                  <select 
                    value={conn2Connector} 
                    onChange={e => setConn2Connector(e.target.value)}
                    className="param-input"
                    style={{ flex: 1 }}
                    disabled={!conn2PartId}
                  >
                    <option value="">Select Connector...</option>
                    {conn2PartId && parts.find(p => p.id === conn2PartId) && 
                      getValidConnectors(parts.find(p => p.id === conn2PartId)!.type).map(c => (
                        <option key={c} value={c}>{c}</option>
                      ))
                    }
                  </select>
                </div>

                <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '0.5rem' }}>
                  <button onClick={handleAddConnection} className="btn btn-secondary">Add Connection</button>
                </div>
              </div>
            </div>
          </div>

          <button onClick={handleGenerateManual} className="btn btn-primary btn-large" disabled={isLoading || parts.length === 0}>
            Generate Assembly
          </button>
        </div>
      )}

      {mode === 'config' && (
        <div className="config-upload" style={{ textAlign: 'center', padding: '3rem', border: '2px dashed var(--border-color)', borderRadius: '8px' }}>
          <h3>Upload JSON/YAML Configuration</h3>
          <p>Provide a valid assembly configuration file to automatically run the CAD pipeline.</p>
          <div style={{ margin: '2rem 0' }}>
            <input 
              type="file" 
              accept=".json,.yaml,.yml" 
              ref={fileInputRef} 
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
            <button 
              className="btn btn-secondary" 
              onClick={() => fileInputRef.current?.click()}
            >
              Select File
            </button>
            {selectedFile && <p style={{ marginTop: '1rem' }}>Selected: <strong>{selectedFile.name}</strong></p>}
          </div>
          <button 
            onClick={handleGenerateConfig} 
            className="btn btn-primary btn-large" 
            disabled={isLoading || !selectedFile}
          >
            Run Pipeline
          </button>
        </div>
      )}

      <LoadingIndicator isLoading={isLoading} />
    </div>
  );
};
