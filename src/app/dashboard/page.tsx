"use client"

import { useState, useEffect, useRef } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { Input } from "@/components/ui/input"
import {
  FileText,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Clock,
  Users,
  Shield,
  Zap,
  Eye,
  Download,
  RefreshCw,
  Activity,
  BarChart3,
  FileCheck,
  AlertTriangle,
  Upload,
  X,
  Trash2,
} from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

interface AnalysisResult {
  id: string
  documentId: string
  documentName: string
  status: string
  progress: number
  results?: any
  startedAt: string
  completedAt?: string
}

export default function DashboardPage() {
  const [analyses, setAnalyses] = useState<AnalysisResult[]>([])
  const [selectedAnalysis, setSelectedAnalysis] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState<string | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [showUploadDialog, setShowUploadDialog] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [stats, setStats] = useState({
    total: 0,
    completed: 0,
    processing: 0,
    failed: 0,
  })

  // Fetch analyses on mount
  useEffect(() => {
    fetchAnalyses()
    const interval = setInterval(fetchAnalyses, 3000) // Poll every 3 seconds
    return () => clearInterval(interval)
  }, [])

  // Auto-refresh selected analysis if it's still processing
  useEffect(() => {
    if (selectedAnalysis && selectedAnalysis.status === 'processing') {
      const interval = setInterval(() => {
        fetchAnalyses()
      }, 2000) // Poll every 2 seconds for active analysis
      return () => clearInterval(interval)
    }
  }, [selectedAnalysis])

  const fetchAnalyses = async () => {
    try {
      const response = await fetch('/api/analysis/list')
      if (response.ok) {
        const data = await response.json()
        setAnalyses(data.analyses || [])
        setStats(data.stats || stats)
      }
    } catch (error) {
      console.error('Failed to fetch analyses:', error)
    }
  }

  const viewAnalysis = (analysis: AnalysisResult) => {
    setSelectedAnalysis(analysis)
  }

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      setUploadError(null)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadError("Please select a file to upload")
      return
    }

    setUploading(true)
    setUploadError(null)

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const response = await fetch('/api/documents/upload', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Upload failed')
      }

      const data = await response.json()
      console.log('Upload successful:', data)

      // Close dialog
      setShowUploadDialog(false)
      setSelectedFile(null)
      
      // Refresh analyses list
      await fetchAnalyses()

      // Auto-select the new analysis after a short delay
      setTimeout(() => {
        const newAnalysis = analyses.find(a => a.id === data.analysis_id)
        if (newAnalysis) {
          setSelectedAnalysis(newAnalysis)
        }
      }, 1000)

    } catch (error) {
      console.error('Upload error:', error)
      setUploadError('Failed to upload document. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  const handleDelete = async (documentId: string, analysisId: string, documentName: string, event: React.MouseEvent) => {
    // Stop propagation to prevent card click
    event.stopPropagation()
    
    // Confirm deletion
    if (!confirm(`Are you sure you want to delete "${documentName}"?\n\nThis will permanently remove the document and all its analyses.`)) {
      return
    }

    try {
      const response = await fetch(`/api/documents/${documentId}`, {
        method: 'DELETE',
      })

      if (!response.ok) {
        throw new Error('Delete failed')
      }

      const data = await response.json()
      console.log('🗑️ Delete successful:', data)

      // If the deleted document was selected, clear selection
      if (selectedAnalysis?.id === analysisId) {
        setSelectedAnalysis(null)
      }

      // Refresh analyses list
      await fetchAnalyses()

    } catch (error) {
      console.error('❌ Delete error:', error)
      alert('Failed to delete document. Please try again.')
    }
  }

  const cancelUpload = () => {
    setShowUploadDialog(false)
    setSelectedFile(null)
    setUploadError(null)
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-600" />
      case 'processing':
        return <Activity className="h-5 w-5 text-blue-600 animate-pulse" />
      case 'failed':
        return <AlertTriangle className="h-5 w-5 text-red-600" />
      default:
        return <Clock className="h-5 w-5 text-gray-600" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'processing':
        return 'bg-blue-100 text-blue-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen py-8 px-4" style={{ backgroundColor: "#F2FFF5" }}>
      <div className="container mx-auto max-w-7xl space-y-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900">AI Analysis Dashboard</h1>
              <p className="text-gray-600 mt-2">
                Real-time document analysis powered by 7 AI models
              </p>
            </div>
            <div className="flex items-center space-x-3">
              <Button
                onClick={() => setShowUploadDialog(true)}
                className="bg-[#40684D] hover:bg-[#355a42] flex items-center space-x-2"
              >
                <Upload className="h-4 w-4" />
                <span>Upload Document</span>
              </Button>
              <Button
                onClick={fetchAnalyses}
                variant="outline"
                className="flex items-center space-x-2"
              >
                <RefreshCw className="h-4 w-4" />
                <span>Refresh</span>
              </Button>
            </div>
          </div>
        </motion.div>

        {/* Stats Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          {[
            {
              title: "Total Documents",
              value: stats.total,
              icon: FileText,
              color: "text-blue-600",
              bg: "bg-blue-100",
            },
            {
              title: "Completed",
              value: stats.completed,
              icon: CheckCircle,
              color: "text-green-600",
              bg: "bg-green-100",
            },
            {
              title: "Processing",
              value: stats.processing,
              icon: Activity,
              color: "text-purple-600",
              bg: "bg-purple-100",
            },
            {
              title: "Failed",
              value: stats.failed,
              icon: AlertTriangle,
              color: "text-red-600",
              bg: "bg-red-100",
            },
          ].map((stat, index) => (
            <Card key={index} className="bg-white">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">{stat.title}</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                  </div>
                  <div className={`p-4 rounded-full ${stat.bg}`}>
                    <stat.icon className={`h-6 w-6 ${stat.color}`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </motion.div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Analysis List */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="lg:col-span-1"
          >
            <Card className="bg-white">
              <CardHeader>
                <CardTitle>Recent Analyses</CardTitle>
                <CardDescription>Click to view detailed results</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {analyses.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <FileText className="h-12 w-12 mx-auto mb-3 text-gray-400" />
                    <p>No analyses yet</p>
                    <p className="text-sm">Upload a document to get started</p>
                  </div>
                ) : (
                  <div className="space-y-3 max-h-[600px] overflow-y-auto">
                    {analyses.map((analysis) => (
                      <motion.div
                        key={analysis.id}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`p-4 border rounded-lg cursor-pointer transition-all relative group ${
                          selectedAnalysis?.id === analysis.id
                            ? "border-[#40684D] bg-green-50"
                            : "border-gray-200 hover:border-gray-300"
                        }`}
                        onClick={() => viewAnalysis(analysis)}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1 pr-8">
                            <div className="flex items-center space-x-2 mb-2">
                              {getStatusIcon(analysis.status)}
                              <span className="font-medium text-sm text-gray-900 truncate">
                                {analysis.documentName}
                              </span>
                            </div>
                            <Badge className={getStatusColor(analysis.status)}>
                              {analysis.status}
                            </Badge>
                            {analysis.status === 'processing' && (
                              <Progress value={analysis.progress} className="mt-2" />
                            )}
                          </div>
                          
                          {/* Delete Button */}
                          <Button
                            variant="ghost"
                            size="sm"
                            className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity text-red-600 hover:text-red-700 hover:bg-red-50"
                            onClick={(e) => handleDelete(analysis.documentId, analysis.id, analysis.documentName, e)}
                            title="Delete document"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                        <div className="mt-2 text-xs text-gray-500">
                          {new Date(analysis.startedAt).toLocaleString()}
                        </div>
                      </motion.div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>

          {/* Analysis Details */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="lg:col-span-2"
          >
            {selectedAnalysis ? (
              <Card className="bg-white">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle>{selectedAnalysis.documentName}</CardTitle>
                      <CardDescription>
                        Analysis ID: {selectedAnalysis.id}
                      </CardDescription>
                    </div>
                    <Badge className={getStatusColor(selectedAnalysis.status)}>
                      {selectedAnalysis.status}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  {selectedAnalysis.status === 'processing' ? (
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">Processing...</span>
                        <span className="text-sm text-gray-600">
                          {selectedAnalysis.progress}%
                        </span>
                      </div>
                      <Progress value={selectedAnalysis.progress} />
                      <div className="flex items-center space-x-2 text-sm text-gray-600">
                        <Activity className="h-4 w-4 animate-pulse text-blue-600" />
                        <span>AI models are analyzing your document</span>
                      </div>
                    </div>
                  ) : selectedAnalysis.status === 'completed' && selectedAnalysis.results ? (
                    <Tabs defaultValue="overview" className="w-full">
                      <TabsList className="grid w-full grid-cols-5">
                        <TabsTrigger value="overview">Overview</TabsTrigger>
                        <TabsTrigger value="entities">Entities</TabsTrigger>
                        <TabsTrigger value="classification">Type</TabsTrigger>
                        <TabsTrigger value="risk">Risk</TabsTrigger>
                        <TabsTrigger value="summary">Summary</TabsTrigger>
                      </TabsList>

                      <TabsContent value="overview" className="space-y-4 mt-4">
                        <AnalysisOverview results={selectedAnalysis.results} />
                      </TabsContent>

                      <TabsContent value="entities" className="space-y-4 mt-4">
                        <EntitiesView entities={selectedAnalysis.results?.entities || []} />
                      </TabsContent>

                      <TabsContent value="classification" className="space-y-4 mt-4">
                        <ClassificationView
                          classification={selectedAnalysis.results?.classification || {}}
                        />
                      </TabsContent>

                      <TabsContent value="risk" className="space-y-4 mt-4">
                        <RiskView risk={selectedAnalysis.results?.risk_assessment || {}} />
                      </TabsContent>

                      <TabsContent value="summary" className="space-y-4 mt-4">
                        <SummaryView summary={selectedAnalysis.results?.summary || ""} />
                      </TabsContent>
                    </Tabs>
                  ) : selectedAnalysis.status === 'failed' ? (
                    <div className="text-center py-8">
                      <AlertTriangle className="h-12 w-12 mx-auto mb-3 text-red-600" />
                      <p className="text-red-600 font-medium">Analysis Failed</p>
                      <p className="text-sm text-gray-600 mt-2">
                        Please try uploading the document again
                      </p>
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <Clock className="h-12 w-12 mx-auto mb-3 text-gray-400" />
                      <p className="text-gray-600">Analysis queued</p>
                      <p className="text-sm text-gray-500 mt-2">
                        Processing will start shortly
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>
            ) : (
              <Card className="bg-white h-full flex items-center justify-center">
                <CardContent className="text-center py-12">
                  <Eye className="h-16 w-16 mx-auto mb-4 text-gray-300" />
                  <p className="text-gray-500 text-lg">Select an analysis to view details</p>
                  <p className="text-sm text-gray-400 mt-2">
                    Click on any analysis from the list to see results
                  </p>
                </CardContent>
              </Card>
            )}
          </motion.div>
        </div>

        {/* Upload Dialog Modal */}
        <AnimatePresence>
          {showUploadDialog && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
              onClick={cancelUpload}
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                onClick={(e) => e.stopPropagation()}
                className="bg-white rounded-lg shadow-xl max-w-md w-full"
              >
                <Card className="border-0">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle>Upload Document for Analysis</CardTitle>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={cancelUpload}
                        className="h-8 w-8 p-0"
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                    <CardDescription>
                      Upload a legal document to analyze with 7 AI models
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {/* File Input */}
                    <div className="space-y-2">
                      <Input
                        ref={fileInputRef}
                        type="file"
                        accept=".pdf,.doc,.docx,.txt"
                        onChange={handleFileSelect}
                        className="cursor-pointer"
                      />
                      <p className="text-xs text-gray-500">
                        Supported formats: PDF, DOC, DOCX, TXT (Max 10MB)
                      </p>
                    </div>

                    {/* Selected File Preview */}
                    {selectedFile && (
                      <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                        <div className="flex items-center space-x-2">
                          <FileText className="h-5 w-5 text-[#40684D]" />
                          <div className="flex-1">
                            <p className="font-medium text-sm text-gray-900">
                              {selectedFile.name}
                            </p>
                            <p className="text-xs text-gray-600">
                              {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                            </p>
                          </div>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => setSelectedFile(null)}
                            className="h-8 w-8 p-0"
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    )}

                    {/* Error Message */}
                    {uploadError && (
                      <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                        <div className="flex items-center space-x-2">
                          <AlertCircle className="h-5 w-5 text-red-600" />
                          <p className="text-sm text-red-800">{uploadError}</p>
                        </div>
                      </div>
                    )}

                    {/* Upload Progress */}
                    {uploading && (
                      <div className="space-y-2">
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                          <Activity className="h-4 w-4 animate-pulse text-blue-600" />
                          <span>Uploading and starting analysis...</span>
                        </div>
                        <Progress value={50} className="w-full" />
                      </div>
                    )}

                    {/* Action Buttons */}
                    <div className="flex items-center space-x-3 pt-2">
                      <Button
                        onClick={handleUpload}
                        disabled={!selectedFile || uploading}
                        className="flex-1 bg-[#40684D] hover:bg-[#355a42]"
                      >
                        {uploading ? (
                          <>
                            <Activity className="h-4 w-4 mr-2 animate-pulse" />
                            Uploading...
                          </>
                        ) : (
                          <>
                            <Upload className="h-4 w-4 mr-2" />
                            Upload & Analyze
                          </>
                        )}
                      </Button>
                      <Button
                        onClick={cancelUpload}
                        disabled={uploading}
                        variant="outline"
                        className="flex-1"
                      >
                        Cancel
                      </Button>
                    </div>

                    {/* Info Box */}
                    <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                      <div className="flex items-start space-x-2">
                        <Zap className="h-4 w-4 text-blue-600 mt-0.5" />
                        <div className="text-xs text-blue-800">
                          <p className="font-medium">What happens next:</p>
                          <ul className="mt-1 space-y-1 list-disc list-inside">
                            <li>Document is uploaded and saved</li>
                            <li>7 AI models analyze your document</li>
                            <li>Results appear in real-time on this dashboard</li>
                            <li>Analysis typically takes 30-60 seconds</li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

// Sub-components for different views
function AnalysisOverview({ results }: { results: any }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Document Type</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-2xl font-bold">{results?.classification?.document_type || "N/A"}</p>
          <p className="text-sm text-gray-600 mt-1">
            Confidence: {(results?.classification?.confidence * 100).toFixed(1)}%
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Risk Level</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-2xl font-bold">
            {results?.risk_assessment?.risk_level || "N/A"}
          </p>
          <p className="text-sm text-gray-600 mt-1">
            Score: {(results?.risk_assessment?.risk_score * 100).toFixed(0)}%
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Entities Found</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-2xl font-bold">{results?.entities?.length || 0}</p>
          <p className="text-sm text-gray-600 mt-1">Named entities detected</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Key Clauses</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-2xl font-bold">{results?.qa_results?.length || 0}</p>
          <p className="text-sm text-gray-600 mt-1">Important clauses identified</p>
        </CardContent>
      </Card>
    </div>
  )
}

function EntitiesView({ entities }: { entities: any[] }) {
  // Group entities by type for better organization
  const groupedEntities = entities.reduce((acc: any, entity) => {
    const type = entity.type || "OTHER";
    if (!acc[type]) {
      acc[type] = [];
    }
    acc[type].push(entity);
    return acc;
  }, {});

  // Define colors for different entity types
  const getEntityTypeColor = (type: string) => {
    const colors: { [key: string]: string } = {
      PERSON: "bg-blue-100 text-blue-800 border-blue-300",
      ORG: "bg-purple-100 text-purple-800 border-purple-300",
      ORGANIZATION: "bg-purple-100 text-purple-800 border-purple-300",
      DATE: "bg-green-100 text-green-800 border-green-300",
      MONEY: "bg-yellow-100 text-yellow-800 border-yellow-300",
      LOCATION: "bg-pink-100 text-pink-800 border-pink-300",
      GPE: "bg-pink-100 text-pink-800 border-pink-300",
      LAW: "bg-red-100 text-red-800 border-red-300",
      PERCENT: "bg-orange-100 text-orange-800 border-orange-300",
      TIME: "bg-teal-100 text-teal-800 border-teal-300",
    };
    return colors[type] || "bg-gray-100 text-gray-800 border-gray-300";
  };

  const getEntityIcon = (type: string) => {
    switch (type) {
      case "PERSON":
        return "👤";
      case "ORG":
      case "ORGANIZATION":
        return "🏢";
      case "DATE":
      case "TIME":
        return "📅";
      case "MONEY":
      case "PERCENT":
        return "💰";
      case "LOCATION":
      case "GPE":
        return "📍";
      case "LAW":
        return "⚖️";
      default:
        return "📌";
    }
  };

  return (
    <div className="space-y-6">
      {entities.length === 0 ? (
        <Card>
          <CardContent className="py-12">
            <div className="text-center">
              <div className="text-5xl mb-4">🔍</div>
              <p className="text-gray-500 text-lg">No entities found in this document</p>
              <p className="text-gray-400 text-sm mt-2">
                Entities include people, organizations, dates, locations, and legal terms
              </p>
            </div>
          </CardContent>
        </Card>
      ) : (
        <>
          {/* Summary Stats */}
          <Card className="bg-gradient-to-r from-blue-50 to-purple-50">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-gray-800">Total Entities Found</h3>
                  <p className="text-3xl font-bold text-blue-600 mt-1">{entities.length}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-600">Entity Types</p>
                  <p className="text-2xl font-bold text-purple-600">{Object.keys(groupedEntities).length}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Grouped Entities */}
          {Object.entries(groupedEntities).map(([type, typeEntities]: [string, any]) => (
            <Card key={type}>
              <CardHeader className={`${getEntityTypeColor(type)} border-b-2`}>
                <CardTitle className="flex items-center space-x-2">
                  <span className="text-2xl">{getEntityIcon(type)}</span>
                  <span>{type}</span>
                  <Badge variant="secondary" className="ml-2">
                    {typeEntities.length} found
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {typeEntities.map((entity: any, index: number) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className={`p-4 rounded-lg border-2 ${getEntityTypeColor(type)} hover:shadow-md transition-shadow`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="font-semibold text-lg">{entity.text}</p>
                          {entity.context && (
                            <p className="text-sm text-gray-600 mt-2 italic line-clamp-2">
                              "{entity.context}"
                            </p>
                          )}
                        </div>
                      </div>
                      <div className="mt-3 flex items-center space-x-4">
                        <div className="flex items-center space-x-1">
                          <span className="text-xs text-gray-500">Confidence:</span>
                          <div className="flex items-center space-x-1">
                            <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                              <div
                                className="h-full bg-gradient-to-r from-green-400 to-green-600"
                                style={{ width: `${entity.score * 100}%` }}
                              />
                            </div>
                            <span className="text-xs font-semibold">{(entity.score * 100).toFixed(0)}%</span>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </>
      )}
    </div>
  );
}

function ClassificationView({ classification }: { classification: any }) {
  const clauses = classification?.clauses || [];
  
  // Get color for clause type
  const getClauseColor = (label: string) => {
    const colors: { [key: string]: string } = {
      "Termination": "bg-red-100 text-red-800 border-red-300",
      "Indemnification": "bg-orange-100 text-orange-800 border-orange-300",
      "Confidentiality": "bg-purple-100 text-purple-800 border-purple-300",
      "Limitation of Liability": "bg-yellow-100 text-yellow-800 border-yellow-300",
      "Governing Law": "bg-blue-100 text-blue-800 border-blue-300",
      "Force Majeure": "bg-pink-100 text-pink-800 border-pink-300",
      "Payment Terms": "bg-green-100 text-green-800 border-green-300",
      "Intellectual Property": "bg-indigo-100 text-indigo-800 border-indigo-300",
      "Non-Compete": "bg-red-100 text-red-800 border-red-300",
      "Dispute Resolution": "bg-teal-100 text-teal-800 border-teal-300",
      "Warranties": "bg-cyan-100 text-cyan-800 border-cyan-300",
      "Assignment": "bg-amber-100 text-amber-800 border-amber-300",
    };
    return colors[label] || "bg-gray-100 text-gray-800 border-gray-300";
  };
  
  const getClauseIcon = (label: string) => {
    const icons: { [key: string]: string } = {
      "Termination": "🚫",
      "Indemnification": "🛡️",
      "Confidentiality": "🔒",
      "Limitation of Liability": "⚖️",
      "Governing Law": "📜",
      "Force Majeure": "⚡",
      "Payment Terms": "💵",
      "Intellectual Property": "💡",
      "Non-Compete": "🚷",
      "Dispute Resolution": "⚖️",
      "Warranties": "✓",
      "Assignment": "📋",
    };
    return icons[label] || "📄";
  };
  
  return (
    <div className="space-y-6">
      {/* Document Type Card */}
      <Card className="bg-gradient-to-br from-indigo-50 via-blue-50 to-purple-50 border-2 shadow-lg">
        <CardHeader>
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-indigo-100 rounded-lg">
              <FileText className="h-6 w-6 text-indigo-600" />
            </div>
            <div>
              <CardTitle className="text-xl">Document Classification</CardTitle>
              <p className="text-sm text-gray-600 mt-1">AI-powered document type identification</p>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="text-center p-4 bg-white rounded-lg shadow-sm">
              <p className="text-sm font-medium text-gray-600 mb-2">Document Type</p>
              <p className="text-3xl font-bold text-indigo-600">
                {classification.document_type || "Unknown"}
              </p>
            </div>
            <div className="text-center p-4 bg-white rounded-lg shadow-sm">
              <p className="text-sm font-medium text-gray-600 mb-2">Confidence Score</p>
              <p className="text-3xl font-bold text-blue-600">
                {(classification.confidence * 100).toFixed(1)}%
              </p>
              <div className="mt-2 w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-400 to-indigo-600 transition-all duration-500"
                  style={{ width: `${classification.confidence * 100}%` }}
                />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Identified Clauses */}
      {clauses.length > 0 && (
        <Card>
          <CardHeader className="bg-gray-50 border-b">
            <CardTitle className="flex items-center space-x-2">
              <span className="text-xl">📑</span>
              <span>Identified Clauses</span>
              <Badge variant="secondary" className="ml-2">
                {clauses.length} found
              </Badge>
            </CardTitle>
            <p className="text-sm text-gray-600 mt-2">
              Key legal clauses and provisions identified in the document
            </p>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="space-y-4">
              {clauses.map((clause: any, index: number) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <Card className={`${getClauseColor(clause.label)} border-l-4 hover:shadow-lg transition-shadow`}>
                    <CardContent className="pt-4">
                      <div className="space-y-3">
                        {/* Header */}
                        <div className="flex items-start justify-between">
                          <div className="flex items-center space-x-3">
                            <span className="text-2xl">{getClauseIcon(clause.label)}</span>
                            <div>
                              <Badge className={`${getClauseColor(clause.label)} border`}>
                                {clause.label}
                              </Badge>
                              <p className="text-sm text-gray-600 mt-1">
                                Clause #{index + 1}
                              </p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="text-lg font-bold text-gray-800">
                              {(clause.score * 100).toFixed(0)}%
                            </p>
                            <p className="text-xs text-gray-500">Confidence</p>
                          </div>
                        </div>

                        {/* Clause Text */}
                        <div className="bg-white rounded-lg p-4 shadow-sm">
                          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                            Clause Content
                          </p>
                          <div className="bg-gray-50 rounded p-3 border-l-4 border-gray-300">
                            <p className="text-sm text-gray-800 leading-relaxed">
                              {clause.paragraph || clause.full_text || "No text available"}
                            </p>
                          </div>
                        </div>

                        {/* Confidence Bar */}
                        <div className="bg-white rounded-lg p-3 shadow-sm">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                              Classification Confidence
                            </span>
                          </div>
                          <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-gradient-to-r from-green-400 to-green-600 transition-all duration-500"
                              style={{ width: `${clause.score * 100}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* No Clauses Found */}
      {(!clauses || clauses.length === 0) && (
        <Card>
          <CardContent className="py-12">
            <div className="text-center">
              <div className="text-5xl mb-4">📑</div>
              <p className="text-gray-500 text-lg">No specific clauses identified</p>
              <p className="text-gray-400 text-sm mt-2">
                The document may be too short or lack standard legal clause structures
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function RiskView({ risk }: { risk: any }) {
  // Risk level configuration
  const getRiskConfig = (level: string) => {
    const configs: { [key: string]: { color: string; bg: string; icon: string; description: string } } = {
      Critical: {
        color: "text-red-700",
        bg: "bg-red-100 border-red-300",
        icon: "🚨",
        description: "Immediate action required - High legal exposure"
      },
      High: {
        color: "text-orange-700",
        bg: "bg-orange-100 border-orange-300",
        icon: "⚠️",
        description: "Significant risks identified - Review recommended"
      },
      Moderate: {
        color: "text-yellow-700",
        bg: "bg-yellow-100 border-yellow-300",
        icon: "⚡",
        description: "Moderate concerns present - Proceed with caution"
      },
      Low: {
        color: "text-blue-700",
        bg: "bg-blue-100 border-blue-300",
        icon: "ℹ️",
        description: "Minor risks detected - Generally acceptable"
      },
      Minimal: {
        color: "text-green-700",
        bg: "bg-green-100 border-green-300",
        icon: "✅",
        description: "Very low risk - Safe to proceed"
      }
    };
    return configs[level] || configs["Moderate"];
  };

  const riskConfig = getRiskConfig(risk.risk_level);
  const riskPercentage = ((risk.risk_score / 5) * 100).toFixed(0);

  return (
    <div className="space-y-6">
      {/* Overall Risk Assessment Card */}
      <Card className={`${riskConfig.bg} border-2 shadow-lg`}>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="text-4xl">{riskConfig.icon}</div>
              <div>
                <CardTitle className="text-2xl">Risk Assessment</CardTitle>
                <p className="text-sm text-gray-600 mt-1">{riskConfig.description}</p>
              </div>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Risk Level */}
            <div className="text-center p-4 bg-white rounded-lg shadow-sm">
              <p className="text-sm font-medium text-gray-600 mb-2">Risk Level</p>
              <p className={`text-3xl font-bold ${riskConfig.color}`}>
                {risk.risk_level || "Unknown"}
              </p>
            </div>

            {/* Risk Score */}
            <div className="text-center p-4 bg-white rounded-lg shadow-sm">
              <p className="text-sm font-medium text-gray-600 mb-2">Risk Score</p>
              <div className="flex items-center justify-center space-x-2">
                <p className="text-3xl font-bold text-gray-800">{risk.risk_score}</p>
                <p className="text-lg text-gray-500">/5</p>
              </div>
            </div>

            {/* Risk Percentage */}
            <div className="text-center p-4 bg-white rounded-lg shadow-sm">
              <p className="text-sm font-medium text-gray-600 mb-2">Risk Percentage</p>
              <div className="relative">
                <p className="text-3xl font-bold text-gray-800">{riskPercentage}%</p>
                <div className="mt-2 w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className={`h-full transition-all duration-500 ${
                      risk.risk_score >= 4 ? "bg-red-500" :
                      risk.risk_score >= 3 ? "bg-orange-500" :
                      risk.risk_score >= 2 ? "bg-yellow-500" : "bg-green-500"
                    }`}
                    style={{ width: `${riskPercentage}%` }}
                  />
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Risk Factors Section */}
      {risk.risk_factors && risk.risk_factors.length > 0 && (
        <Card>
          <CardHeader className="bg-gray-50 border-b">
            <CardTitle className="flex items-center space-x-2">
              <span className="text-xl">🔍</span>
              <span>Identified Risk Factors</span>
              <Badge variant="secondary" className="ml-2">
                {risk.risk_factors.length} found
              </Badge>
            </CardTitle>
            <p className="text-sm text-gray-600 mt-2">
              Detailed analysis of potential legal and contractual risks
            </p>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="space-y-4">
              {risk.risk_factors.map((factor: any, index: number) => {
                const factorConfig = getRiskConfig(factor.risk_level);
                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <Card className={`${factorConfig.bg} border-l-4 hover:shadow-lg transition-shadow`}>
                      <CardContent className="pt-6">
                        <div className="space-y-4">
                          {/* Header */}
                          <div className="flex items-start justify-between">
                            <div className="flex items-center space-x-3">
                              <span className="text-2xl">{factorConfig.icon}</span>
                              <div>
                                <Badge className={`${factorConfig.bg} ${factorConfig.color} border`}>
                                  {factor.risk_level || "Unknown"}
                                </Badge>
                                <p className="text-sm text-gray-600 mt-1">
                                  Risk Factor #{index + 1}
                                </p>
                              </div>
                            </div>
                            <div className="text-right">
                              <p className="text-2xl font-bold text-gray-800">
                                {factor.risk_score}/5
                              </p>
                              <p className="text-xs text-gray-500">Risk Score</p>
                            </div>
                          </div>

                          {/* Type */}
                          <div className="bg-white rounded-lg p-3 shadow-sm">
                            <div className="flex items-center space-x-2">
                              <span className="text-sm font-semibold text-gray-700">Category:</span>
                              <Badge variant="outline" className="font-medium">
                                {factor.type || "Unspecified"}
                              </Badge>
                            </div>
                          </div>

                          {/* Clause Content */}
                          <div className="bg-white rounded-lg p-4 shadow-sm">
                            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                              Problematic Clause
                            </p>
                            <div className="bg-gray-50 rounded p-3 border-l-4 border-gray-300">
                              <p className="text-sm text-gray-800 italic leading-relaxed">
                                "{factor.clause || "No clause text available"}"
                              </p>
                            </div>
                          </div>

                          {/* Confidence Meter */}
                          <div className="bg-white rounded-lg p-3 shadow-sm">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                                Analysis Confidence
                              </span>
                              <span className="text-sm font-bold text-gray-800">
                                {(factor.confidence * 100).toFixed(1)}%
                              </span>
                            </div>
                            <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                              <div
                                className="h-full bg-gradient-to-r from-blue-400 to-blue-600 transition-all duration-500"
                                style={{ width: `${factor.confidence * 100}%` }}
                              />
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {/* No Risk Factors */}
      {(!risk.risk_factors || risk.risk_factors.length === 0) && (
        <Card>
          <CardContent className="py-12">
            <div className="text-center">
              <div className="text-5xl mb-4">🎯</div>
              <p className="text-gray-500 text-lg">No specific risk factors identified</p>
              <p className="text-gray-400 text-sm mt-2">
                The document appears to have standard clauses with minimal concerns
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

function SummaryView({ summary }: { summary: string }) {
  // Split summary into sentences for better readability
  const sentences = summary ? summary.match(/[^.!?]+[.!?]+/g) || [summary] : [];
  
  return (
    <div className="space-y-4">
      <Card className="bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
        <CardHeader>
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-indigo-100 rounded-lg">
              <FileText className="h-6 w-6 text-indigo-600" />
            </div>
            <div>
              <CardTitle className="text-xl">Document Summary</CardTitle>
              <p className="text-sm text-gray-600 mt-1">AI-generated executive summary</p>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {!summary || summary.trim() === "" ? (
            <div className="text-center py-12">
              <div className="text-5xl mb-4">📄</div>
              <p className="text-gray-500 text-lg">No summary available</p>
              <p className="text-gray-400 text-sm mt-2">
                The document could not be summarized
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Key Points Section */}
              <div className="bg-white rounded-lg p-6 shadow-sm border-l-4 border-indigo-500">
                <h4 className="font-semibold text-gray-800 mb-4 flex items-center space-x-2">
                  <span className="text-xl">📋</span>
                  <span>Key Points</span>
                </h4>
                <div className="space-y-3">
                  {sentences.slice(0, 5).map((sentence, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      <div className="flex-shrink-0 w-6 h-6 bg-indigo-500 text-white rounded-full flex items-center justify-center text-sm font-semibold mt-0.5">
                        {index + 1}
                      </div>
                      <p className="text-gray-700 leading-relaxed flex-1">
                        {sentence.trim()}
                      </p>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Full Summary Section */}
              {sentences.length > 5 && (
                <div className="bg-white rounded-lg p-6 shadow-sm">
                  <h4 className="font-semibold text-gray-800 mb-4 flex items-center space-x-2">
                    <span className="text-xl">📖</span>
                    <span>Complete Summary</span>
                  </h4>
                  <p className="text-gray-700 leading-relaxed text-justify">
                    {summary}
                  </p>
                </div>
              )}

              {/* Summary Stats */}
              <div className="grid grid-cols-3 gap-4">
                <Card className="bg-blue-50 border-blue-200">
                  <CardContent className="pt-4 text-center">
                    <p className="text-2xl font-bold text-blue-600">
                      {summary.split(' ').length}
                    </p>
                    <p className="text-xs text-gray-600 mt-1">Words</p>
                  </CardContent>
                </Card>
                <Card className="bg-purple-50 border-purple-200">
                  <CardContent className="pt-4 text-center">
                    <p className="text-2xl font-bold text-purple-600">
                      {sentences.length}
                    </p>
                    <p className="text-xs text-gray-600 mt-1">Sentences</p>
                  </CardContent>
                </Card>
                <Card className="bg-pink-50 border-pink-200">
                  <CardContent className="pt-4 text-center">
                    <p className="text-2xl font-bold text-pink-600">
                      {Math.ceil(summary.split(' ').length / 200)}
                    </p>
                    <p className="text-xs text-gray-600 mt-1">Min Read</p>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
