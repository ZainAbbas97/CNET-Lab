import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface UploadResponse {
  success: boolean
  session_id: string
  dataset: {
    rows: number
    columns: string[]
    shape: [number, number]
  }
}

export interface ExecuteResponse {
  success: boolean
  command: string
  result: any
}

export const uploadDataset = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await apiClient.post<UploadResponse>('/api/v1/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  
  return response.data
}

export const executeCommand = async (
  command: string,
  params: Record<string, any>,
  sessionId: string
): Promise<ExecuteResponse> => {
  const response = await apiClient.post<ExecuteResponse>('/api/v1/execute', {
    command,
    params,
    session_id: sessionId,
  })
  
  return response.data
}





