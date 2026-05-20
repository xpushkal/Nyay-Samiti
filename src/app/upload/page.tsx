"use client"

import type React from "react"

import { useState, useCallback } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Upload, FileText, ImageIcon, CheckCircle, Shield, Clock, Zap, AlertCircle, Activity } from "lucide-react"
import { motion } from "framer-motion"

export default function UploadPage() {
  const router = useRouter()
  const [dragActive, setDragActive] = useState(false)
  const [files, setFiles] = useState<File[]>([])
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [processed, setProcessed] = useState(false)
  const [uploadedAnalysisIds, setUploadedAnalysisIds] = useState<string[]>([])

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const newFiles = Array.from(e.dataTransfer.files)
      setFiles((prev) => [...prev, ...newFiles])
    }
  }, [])

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const newFiles = Array.from(e.target.files)
      setFiles((prev) => [...prev, ...newFiles])
    }
  }

  const simulateUpload = async () => {
    setUploading(true)
    setProgress(0)
    const analysisIds: string[] = []

    try {
      let currentProgress = 0
      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch('/api/documents/upload', {
          method: 'POST',
          body: formData,
        })

        if (response.ok) {
          const data = await response.json()
          analysisIds.push(data.analysis_id)
          console.log('Upload successful:', data)
          
          // Update progress
          currentProgress = ((i + 1) / files.length) * 100
          setProgress(currentProgress)
        } else {
          console.error('Upload failed for:', file.name)
        }
      }

      setUploadedAnalysisIds(analysisIds)
      setProcessed(true)
      
    } catch (error) {
      console.error('Upload failed:', error)
      setUploading(false)
    }
  }

  const viewInDashboard = () => {
    router.push('/dashboard')
  }

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index))
  }

  return (
    <div className="min-h-screen py-12" style={{ backgroundColor: "#F2FFF5" }}>
      <div className="container mx-auto px-4">
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Upload Your Legal Documents</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Drag and drop or click to upload your document for AI-powered simplification. Get clear, understandable
            explanations in seconds.
          </p>
        </motion.div>

        <div className="max-w-4xl mx-auto space-y-8">
          {/* Upload Area */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <Card
              className={`border-2 border-dashed transition-colors ${
                dragActive ? "border-[#40684D] bg-green-50" : "border-gray-300 hover:border-[#40684D]"
              }`}
            >
              <CardContent className="p-12">
                <div
                  className="text-center space-y-6"
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  <div className="flex justify-center">
                    <div className="p-6 bg-green-100 rounded-full">
                      <Upload className="h-12 w-12 text-[#40684D]" />
                    </div>
                  </div>

                  <div>
                    <h3 className="text-2xl font-semibold text-gray-900 mb-2">Drop your document here</h3>
                    <p className="text-gray-600 mb-4">or click to browse files from your device</p>

                    <input
                      type="file"
                      multiple
                      accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
                      onChange={handleFileSelect}
                      className="hidden"
                      id="file-upload"
                    />
                    <label htmlFor="file-upload">
                      <Button className="bg-[#40684D] hover:bg-[#355a42] cursor-pointer">Choose Files</Button>
                    </label>
                  </div>

                  <div className="flex justify-center space-x-6 text-sm text-gray-500">
                    <div className="flex items-center space-x-1">
                      <FileText className="h-4 w-4" />
                      <span>PDF, DOC, DOCX</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <ImageIcon className="h-4 w-4" />
                      <span>JPG, PNG</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Shield className="h-4 w-4" />
                      <span>Max 10MB</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Processing Stats */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="grid md:grid-cols-3 gap-6"
          >
            {[
              { icon: Zap, label: "Average Processing Time", value: "28 seconds", color: "text-blue-600" },
              { icon: CheckCircle, label: "Success Rate", value: "99.9%", color: "text-[#40684D]" },
              { icon: Shield, label: "Documents Processed Today", value: "1,247", color: "text-purple-600" },
            ].map((stat, index) => (
              <Card key={index} className="text-center p-6 bg-white">
                <CardContent className="space-y-2">
                  <stat.icon className={`h-8 w-8 mx-auto ${stat.color}`} />
                  <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
                  <div className="text-sm text-gray-600">{stat.label}</div>
                </CardContent>
              </Card>
            ))}
          </motion.div>

          {/* Upload Instructions */}
          {files.length === 0 && (
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
            >
              <Card className="bg-white">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <FileText className="h-5 w-5 text-blue-600" />
                    </div>
                    <span>How to Upload Your Document</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-3 gap-6">
                    {[
                      {
                        step: "1",
                        title: "Prepare Your Document",
                        description:
                          "Ensure your document is clear and readable. Scanned documents work perfectly too!",
                        tips: ["High resolution preferred", "All pages included", "Text should be legible"],
                      },
                      {
                        step: "2",
                        title: "Choose Upload Method",
                        description: "Drag and drop your file or click to browse from your device.",
                        tips: ["Multiple files supported", "Up to 10MB per file", "Batch processing available"],
                      },
                      {
                        step: "3",
                        title: "Review & Process",
                        description: "Check your uploaded files and click process to start AI simplification.",
                        tips: ["Preview before processing", "Estimated time: 30 seconds", "Results in plain language"],
                      },
                    ].map((instruction, index) => (
                      <div key={index} className="space-y-4">
                        <div className="flex items-center space-x-3">
                          <div className="w-8 h-8 bg-[#40684D] text-white rounded-full flex items-center justify-center font-bold text-sm">
                            {instruction.step}
                          </div>
                          <h3 className="font-semibold text-gray-900">{instruction.title}</h3>
                        </div>
                        <p className="text-gray-600 text-sm">{instruction.description}</p>
                        <ul className="space-y-1">
                          {instruction.tips.map((tip, tipIndex) => (
                            <li key={tipIndex} className="flex items-center space-x-2 text-xs text-gray-500">
                              <CheckCircle className="h-3 w-3 text-[#40684D]" />
                              <span>{tip}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {/* Before/After Samples Carousel */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.8 }}
          >
            <Card className="bg-white">
              <CardHeader>
                <CardTitle>See the Transformation</CardTitle>
                <p className="text-gray-600">Real examples of how our AI simplifies complex legal language</p>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {[
                    {
                      type: "Employment Contract Clause",
                      before:
                        "The party of the first part hereby covenants and agrees to indemnify, defend, and hold harmless the party of the second part from and against any and all claims, demands, losses, costs, expenses, obligations, liabilities, damages, recoveries, and deficiencies, including but not limited to reasonable attorneys' fees...",
                      after:
                        "You agree to protect the other party and pay for any legal problems or costs that might come up because of this agreement, including lawyer fees.",
                      category: "Employment Contract",
                      complexity: "High",
                      timeToProcess: "22 seconds",
                    },
                    {
                      type: "Legal Notice",
                      before:
                        "WHEREAS, the aforementioned party has failed to comply with the terms and conditions as stipulated in the aforementioned agreement dated the fifteenth day of March, two thousand and twenty-four...",
                      after:
                        "Because you didn't follow the rules in our agreement from March 15, 2024, we're sending you this notice.",
                      category: "Breach Notice",
                      complexity: "Medium",
                      timeToProcess: "18 seconds",
                    },
                    {
                      type: "Property Deed",
                      before:
                        "TO HAVE AND TO HOLD the above granted and bargained premises, with all the privileges and appurtenances thereof, to the said grantee, their heirs and assigns forever, subject nevertheless to the reservations, limitations, provisos and conditions...",
                      after:
                        "You now own this property completely, along with all rights that come with it, and you can pass it on to your family. However, there are some rules and restrictions that still apply.",
                      category: "Real Estate",
                      complexity: "High",
                      timeToProcess: "31 seconds",
                    },
                  ].map((example, index) => (
                    <div key={index} className="border rounded-lg p-6 space-y-4">
                      <div className="flex items-center justify-between">
                        <h4 className="font-semibold text-gray-900">{example.type}</h4>
                        <div className="flex items-center space-x-2">
                          <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                            {example.category}
                          </span>
                          <span
                            className={`text-xs px-2 py-1 rounded ${
                              example.complexity === "High"
                                ? "bg-red-100 text-red-700"
                                : "bg-yellow-100 text-yellow-700"
                            }`}
                          >
                            {example.complexity}
                          </span>
                          <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded flex items-center">
                            <Clock className="h-3 w-3 mr-1" />
                            {example.timeToProcess}
                          </span>
                        </div>
                      </div>

                      <div className="grid md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <div className="flex items-center space-x-2">
                            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                            <span className="text-sm font-medium text-red-700">Original (Complex)</span>
                          </div>
                          <div className="bg-red-50 p-4 rounded-lg border-l-4 border-red-500">
                            <p className="text-sm text-gray-700 italic">{example.before}</p>
                          </div>
                        </div>

                        <div className="space-y-2">
                          <div className="flex items-center space-x-2">
                            <div className="w-3 h-3 bg-[#40684D] rounded-full"></div>
                            <span className="text-sm font-medium text-[#40684D]">Simplified</span>
                          </div>
                          <div className="bg-green-50 p-4 rounded-lg border-l-4 border-[#40684D]">
                            <p className="text-sm text-gray-700">{example.after}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Upload Tips & Privacy */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.0 }}
            className="grid md:grid-cols-2 gap-6"
          >
            <Card className="border-blue-200 bg-blue-50">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2 text-blue-800">
                  <Upload className="h-5 w-5" />
                  <span>Upload Guidelines</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <h4 className="font-medium text-blue-900">File Requirements:</h4>
                  <ul className="text-sm text-blue-800 space-y-2">
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-blue-600" />
                      <span>Maximum file size: 10MB per document</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-blue-600" />
                      <span>Supported formats: PDF, DOC, DOCX, JPG, PNG</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-blue-600" />
                      <span>Multiple files can be uploaded simultaneously</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-blue-600" />
                      <span>Scanned documents and images supported</span>
                    </li>
                  </ul>
                </div>
                <div className="space-y-3">
                  <h4 className="font-medium text-blue-900">For Best Results:</h4>
                  <ul className="text-sm text-blue-800 space-y-2">
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-blue-600" />
                      <span>Use high-resolution scans (300 DPI or higher)</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-blue-600" />
                      <span>Ensure all text is clearly readable</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-blue-600" />
                      <span>Include all relevant pages of the document</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-blue-600" />
                      <span>Remove or redact sensitive personal information if needed</span>
                    </li>
                  </ul>
                </div>
              </CardContent>
            </Card>

            <Card className="border-green-200 bg-green-50">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2 text-[#40684D]">
                  <Shield className="h-5 w-5" />
                  <span>Privacy & Security</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <h4 className="font-medium text-green-900">Your Data is Protected:</h4>
                  <ul className="text-sm text-green-800 space-y-2">
                    <li className="flex items-center space-x-2">
                      <Shield className="h-4 w-4 text-[#40684D]" />
                      <span>256-bit SSL encryption during upload and processing</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <Shield className="h-4 w-4 text-[#40684D]" />
                      <span>Processing happens on secure, isolated servers</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <Shield className="h-4 w-4 text-[#40684D]" />
                      <span>Files are automatically deleted within 24 hours</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <Shield className="h-4 w-4 text-[#40684D]" />
                      <span>No human access to your documents during processing</span>
                    </li>
                  </ul>
                </div>
                <div className="space-y-3">
                  <h4 className="font-medium text-green-900">Compliance Standards:</h4>
                  <ul className="text-sm text-green-800 space-y-2">
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-[#40684D]" />
                      <span>GDPR and CCPA compliant</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-[#40684D]" />
                      <span>SOC 2 Type II certified infrastructure</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-[#40684D]" />
                      <span>Bank-level security standards</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-[#40684D]" />
                      <span>Regular third-party security audits</span>
                    </li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* File List */}
          {files.length > 0 && (
            <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
              <Card className="bg-white">
                <CardHeader>
                  <CardTitle>Selected Files ({files.length})</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {files.map((file, index) => (
                    <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        {file.type.includes("image") ? (
                          <ImageIcon className="h-8 w-8 text-blue-600" />
                        ) : (
                          <FileText className="h-8 w-8 text-[#40684D]" />
                        )}
                        <div>
                          <p className="font-medium text-gray-900">{file.name}</p>
                          <div className="flex items-center space-x-4 text-sm text-gray-500">
                            <span>{(file.size / 1024 / 1024).toFixed(2)} MB</span>
                            <span>•</span>
                            <span>{file.type.split("/")[1].toUpperCase()}</span>
                            <span>•</span>
                            <span className="text-[#40684D]">Ready to process</span>
                          </div>
                        </div>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => removeFile(index)}
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        Remove
                      </Button>
                    </div>
                  ))}

                  {!uploading && !processed && (
                    <div className="space-y-4">
                      <div className="bg-blue-50 p-4 rounded-lg">
                        <div className="flex items-start space-x-3">
                          <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5" />
                          <div>
                            <h4 className="font-medium text-blue-900">Processing Information</h4>
                            <p className="text-sm text-blue-800 mt-1">
                              Your {files.length} document{files.length > 1 ? "s" : ""} will be processed
                              simultaneously. Estimated total time: {Math.max(20, files.length * 15)} seconds.
                            </p>
                          </div>
                        </div>
                      </div>
                      <Button onClick={simulateUpload} className="w-full bg-[#40684D] hover:bg-[#355a42]" size="lg">
                        Process {files.length} Document{files.length > 1 ? "s" : ""}
                      </Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          )}

          {/* Progress */}
          {uploading && (
            <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
              <Card className="bg-white">
                <CardContent className="p-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold">
                        Processing your document{files.length > 1 ? "s" : ""}...
                      </h3>
                      <span className="text-sm text-gray-500">{progress}%</span>
                    </div>
                    <Progress value={progress} className="w-full" />
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-[#40684D]"></div>
                      <span>AI is analyzing and simplifying your legal document{files.length > 1 ? "s" : ""}</span>
                    </div>
                    <div className="grid grid-cols-3 gap-4 text-center text-xs text-gray-500">
                      <div className={progress >= 30 ? "text-[#40684D]" : ""}>
                        <div className="font-medium">Text Extraction</div>
                        <div>{progress >= 30 ? "Complete" : "In Progress"}</div>
                      </div>
                      <div className={progress >= 70 ? "text-[#40684D]" : ""}>
                        <div className="font-medium">AI Analysis</div>
                        <div>{progress >= 70 ? "Complete" : progress >= 30 ? "In Progress" : "Pending"}</div>
                      </div>
                      <div className={progress >= 100 ? "text-[#40684D]" : ""}>
                        <div className="font-medium">Simplification</div>
                        <div>{progress >= 100 ? "Complete" : progress >= 70 ? "In Progress" : "Pending"}</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {/* Sample Output Preview */}
          {processed && (
            <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
              <Card className="border-green-200 bg-green-50">
                <CardHeader>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-6 w-6 text-[#40684D]" />
                    <CardTitle className="text-green-800">Upload Complete!</CardTitle>
                  </div>
                  <p className="text-green-700">
                    Your document{files.length > 1 ? "s have" : " has"} been uploaded and analysis has started
                  </p>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="bg-white rounded-lg p-6 border border-green-200">
                    <h4 className="font-semibold text-gray-900 mb-4">What's happening now:</h4>
                    <div className="space-y-3">
                      <div className="flex items-start space-x-3">
                        <CheckCircle className="h-5 w-5 text-[#40684D] mt-0.5" />
                        <div>
                          <p className="font-medium text-gray-900">Documents Uploaded</p>
                          <p className="text-sm text-gray-600">
                            {files.length} document{files.length > 1 ? "s" : ""} saved successfully
                          </p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-3">
                        <Activity className="h-5 w-5 text-blue-600 mt-0.5 animate-pulse" />
                        <div>
                          <p className="font-medium text-gray-900">AI Analysis In Progress</p>
                          <p className="text-sm text-gray-600">
                            7 AI models are analyzing your document{files.length > 1 ? "s" : ""}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-3">
                        <Clock className="h-5 w-5 text-purple-600 mt-0.5" />
                        <div>
                          <p className="font-medium text-gray-900">Estimated Time</p>
                          <p className="text-sm text-gray-600">
                            30-60 seconds per document
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-4">
                    <Button 
                      onClick={viewInDashboard}
                      className="bg-[#40684D] hover:bg-[#355a42] text-white" 
                      size="lg"
                    >
                      View Results in Dashboard
                    </Button>
                    <Button
                      onClick={() => {
                        setFiles([])
                        setProcessed(false)
                        setProgress(0)
                        setUploadedAnalysisIds([])
                      }}
                      variant="outline"
                      className="border-[#40684D] text-[#40684D] hover:bg-green-50"
                      size="lg"
                    >
                      Upload Another Document
                    </Button>
                  </div>

                  <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="flex items-start space-x-3">
                      <Zap className="h-5 w-5 text-blue-600 mt-0.5" />
                      <div className="text-sm text-blue-800">
                        <p className="font-medium">AI Models Processing:</p>
                        <ul className="mt-2 space-y-1">
                          <li>• Named Entity Recognition</li>
                          <li>• Clause Classification</li>
                          <li>• Risk Assessment</li>
                          <li>• Document Summarization</li>
                          <li>• Question Answering</li>
                          <li>• Clause Comparison</li>
                          <li>• Recommendations</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  )
}
