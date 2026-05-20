/**
 * ML Service Client
 * Connects Next.js backend to FastAPI ML service
 */

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000'
const ML_API_KEY = process.env.ML_API_KEY || ''

export interface MLAnalysisRequest {
  analysis_id?: string
  document_id: string
  document_text: string
  analysis_type?: 'comprehensive' | 'ner' | 'classification' | 'risk' | 'summary'
}

export interface MLAnalysisResponse {
  analysis_id: string
  status: string
  results?: any
  error?: string
}

class MLServiceClient {
  private baseUrl: string
  private apiKey: string

  constructor() {
    this.baseUrl = ML_SERVICE_URL
    this.apiKey = ML_API_KEY
  }

  private getHeaders() {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`
    }
    return headers
  }

  async analyzeDocument(request: MLAnalysisRequest): Promise<MLAnalysisResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/document/analyze`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(request),
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`ML service error: ${response.statusText} - ${errorText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to analyze document:', error)
      throw error
    }
  }

  async getAnalysisStatus(analysisId: string): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/analysis/${analysisId}/status`, {
        headers: this.getHeaders(),
      })

      if (!response.ok) {
        throw new Error(`Failed to get status: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to get analysis status:', error)
      throw error
    }
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`, {
        headers: this.getHeaders(),
      })
      return response.ok
    } catch (error) {
      console.error('ML service health check failed:', error)
      return false
    }
  }
}

export const mlService = new MLServiceClient()
