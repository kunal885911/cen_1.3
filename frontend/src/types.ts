export type ModelType = 'shaft' | 'plate' | 'flange' | 'lbracket' | 'ubracket' | 'housing' | 'flanged_shaft';

export interface ShaftParams {
  diameter: number;
  length: number;
}

export interface PlateParams {
  length: number;
  width: number;
}

export interface FlangeParams {
  inner_diameter: number;
}

export interface LbracketParams {
  length_1: number;
  length_2: number;
  width: number;
}

export interface UbracketParams {
  length: number;
  height: number;
  width: number;
}

export interface HousingParams {
  length: number;
  height: number;
  width: number;
}

export interface FlangedShaftParams {
  left_diameter: number;
  left_length: number;
  flange_diameter: number;
  flange_thickness: number;
  right_diameter: number;
  right_length: number;
}

export type ModelParams =
  | ShaftParams
  | PlateParams
  | FlangeParams
  | LbracketParams
  | UbracketParams
  | HousingParams
  | FlangedShaftParams;

export interface GenerateRequest {
  type: ModelType;
  params: ModelParams;
}

export interface GenerateResponse {
  success: boolean;
  message: string;
  fileUrl?: string;
  downloadName?: string;
  outputFiles?: string[];
  error?: string;
}

export interface AppState {
  selectedModel: ModelType | null;
  params: Partial<ShaftParams & PlateParams & FlangeParams & LbracketParams & UbracketParams & HousingParams & FlangedShaftParams>;
  isLoading: boolean;
  result: GenerateResponse | null;
  error: string | null;
}

export interface PartConfig {
  id: string;
  type: ModelType;
  parameters: Partial<ModelParams>;
}

export type ConnectionPair = [string, string];

export interface AssemblyRequest {
  assembly_name: string;
  parts: PartConfig[];
  connections: ConnectionPair[];
  export_modes?: string[];
}
