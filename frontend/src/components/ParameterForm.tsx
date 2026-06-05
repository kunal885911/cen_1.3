import React from 'react';
import { 
  ModelType, 
  ShaftParams, 
  PlateParams, 
  FlangeParams, 
  LbracketParams, 
  UbracketParams,
  HousingParams,
  FlangedShaftParams
} from '../types';
import '../styles/ParameterForm.css';

type AllParams = Partial<
  ShaftParams & PlateParams & FlangeParams & LbracketParams & UbracketParams & HousingParams & FlangedShaftParams
>;

interface ParameterFormProps {
  modelType: ModelType | null;
  params: AllParams;
  onParamsChange: (params: AllParams) => void;
  isLoading?: boolean;
}

interface InputFieldProps {
  id: string;
  label: string;
  unit: string;
  value: number | undefined;
  onChange: (field: string, value: string) => void;
  disabled: boolean;
  min: number;
  max: number;
  placeholder?: string;
}

const InputField: React.FC<InputFieldProps> = ({ id, label, unit, value, onChange, disabled, min, max, placeholder = "0.0" }) => (
  <div className="form-field">
    <label htmlFor={id}>
      <span>{label}</span>
      <span className="field-unit">{unit}</span>
    </label>
    <div className="input-wrapper">
      <input
        id={id}
        type="number"
        min={min}
        max={max}
        step="0.1"
        value={value === undefined ? '' : value}
        onChange={(e) => onChange(id, e.target.value)}
        disabled={disabled}
        placeholder={placeholder}
        required
      />
      <span className="input-focus-indicator"></span>
    </div>
  </div>
);

export const ParameterForm: React.FC<ParameterFormProps> = ({
  modelType,
  params,
  onParamsChange,
  isLoading = false,
}) => {
  if (!modelType) {
    return (
      <div className="parameter-form">
        <div className="placeholder-text">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" />
            <path d="M9 3v18" />
            <path d="M15 3v18" />
            <path d="M3 9h18" />
            <path d="M3 15h18" />
          </svg>
          <p>Awaiting model selection to configure parameters.</p>
        </div>
      </div>
    );
  }

  const handleInputChange = (field: string, value: string) => {
    const numValue = parseFloat(value);
    if (!isNaN(numValue)) {
      onParamsChange({
        ...params,
        [field]: numValue,
      });
    } else if (value === '') {
      const newParams = { ...params };
      delete newParams[field as keyof typeof newParams];
      onParamsChange(newParams);
    }
  };

  const getIcon = () => {
    switch (modelType) {
      case 'shaft':
        return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/></svg>;
      case 'plate':
        return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>;
      case 'flange':
        return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/></svg>;
      case 'lbracket':
        return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M8 4v12h8"/><path d="M4 4v16h12"/></svg>;
      case 'ubracket':
        return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 4v12h16V4"/><path d="M8 4v8h8V4"/></svg>;
      case 'housing':
        return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="2" y="4" width="20" height="16" rx="2"/><rect x="4" y="6" width="16" height="12" rx="1"/></svg>;
      case 'flanged_shaft':
        return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="2" y="10" width="6" height="4" rx="1"/><rect x="16" y="10" width="6" height="4" rx="1"/><rect x="8" y="6" width="8" height="12" rx="2"/></svg>;
      default:
        return null;
    }
  };

  const renderShaftForm = () => (
    <div className="form-group">
      <InputField id="diameter" label="Diameter" unit="mm" min={6} max={500} value={params.diameter} onChange={handleInputChange} disabled={isLoading} />
      <InputField id="length" label="Length" unit="mm" min={10} max={2000} value={params.length} onChange={handleInputChange} disabled={isLoading} />
    </div>
  );

  const renderPlateForm = () => (
    <div className="form-group">
      <InputField id="length" label="Length" unit="mm" min={10} max={2000} value={params.length} onChange={handleInputChange} disabled={isLoading} />
      <InputField id="width" label="Width" unit="mm" min={10} max={2000} value={params.width} onChange={handleInputChange} disabled={isLoading} />
    </div>
  );

  const renderFlangeForm = () => (
    <div className="form-group">
      <InputField id="inner_diameter" label="Inner Diameter" unit="mm" min={36} max={620} value={params.inner_diameter} onChange={handleInputChange} disabled={isLoading} />
    </div>
  );

  const renderLbracketForm = () => (
    <div className="form-group">
      <InputField id="length_1" label="Length 1 (L1)" unit="mm" min={10} max={1000} value={params.length_1} onChange={handleInputChange} disabled={isLoading} />
      <InputField id="length_2" label="Length 2 (L2)" unit="mm" min={10} max={1000} value={params.length_2} onChange={handleInputChange} disabled={isLoading} />
      <InputField id="width" label="Width (W)" unit="mm" min={10} max={500} value={params.width} onChange={handleInputChange} disabled={isLoading} />
    </div>
  );

  const renderUbracketForm = () => (
    <div className="form-group">
      <InputField id="length" label="Length (L)" unit="mm" min={10} max={1000} value={params.length} onChange={handleInputChange} disabled={isLoading} />
      <InputField id="height" label="Height (H)" unit="mm" min={10} max={1000} value={params.height} onChange={handleInputChange} disabled={isLoading} />
      <InputField id="width" label="Width (W)" unit="mm" min={10} max={500} value={params.width} onChange={handleInputChange} disabled={isLoading} />
    </div>
  );

  const renderHousingForm = () => (
    <div className="form-group">
      <InputField id="length" label="Length" unit="mm" min={20} max={2000} value={params.length} onChange={handleInputChange} disabled={isLoading} />
      <InputField id="height" label="Height" unit="mm" min={20} max={2000} value={params.height} onChange={handleInputChange} disabled={isLoading} />
      <InputField id="width" label="Width" unit="mm" min={20} max={2000} value={params.width} onChange={handleInputChange} disabled={isLoading} />
    </div>
  );

  const renderFlangedShaftForm = () => (
    <div className="form-group">
      <InputField id="left_diameter" label="Left Diameter" unit="mm" min={6} max={500} value={params.left_diameter} onChange={handleInputChange} disabled={isLoading} />
      <InputField id="left_length" label="Left Length" unit="mm" min={10} max={2000} value={params.left_length} onChange={handleInputChange} disabled={isLoading} />
      <InputField id="flange_diameter" label="Flange Diameter" unit="mm" min={36} max={620} value={params.flange_diameter} onChange={handleInputChange} disabled={isLoading} />
      <InputField id="flange_thickness" label="Flange Thickness" unit="mm" min={5} max={500} value={params.flange_thickness} onChange={handleInputChange} disabled={isLoading} />
      <InputField id="right_diameter" label="Right Diameter" unit="mm" min={6} max={500} value={params.right_diameter} onChange={handleInputChange} disabled={isLoading} />
      <InputField id="right_length" label="Right Length" unit="mm" min={10} max={2000} value={params.right_length} onChange={handleInputChange} disabled={isLoading} />
    </div>
  );

  const renderFormContent = () => {
    switch (modelType) {
      case 'shaft': return renderShaftForm();
      case 'plate': return renderPlateForm();
      case 'flange': return renderFlangeForm();
      case 'lbracket': return renderLbracketForm();
      case 'ubracket': return renderUbracketForm();
      case 'housing': return renderHousingForm();
      case 'flanged_shaft': return renderFlangedShaftForm();
      default: return null;
    }
  };

  return (
    <div className="parameter-form">
      <div className="parameter-form-header">
        <div className="parameter-form-header-icon">
          {getIcon()}
        </div>
        <h2>{modelType.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ').replace('bracket', '-Bracket')} Parameters</h2>
      </div>
      
      {renderFormContent()}
    </div>
  );
};
