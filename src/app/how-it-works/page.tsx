"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Upload, Brain, CheckCircle, FileText, Languages, Shield, Zap, ArrowRight, Users } from "lucide-react"
import Link from "next/link"
import { motion } from "framer-motion"

export default function HowItWorksPage() {
  const steps = [
    {
      icon: Upload,
      title: "Upload",
      description:
        "Upload your legal document in PDF, DOC, or image format. Our AI processes your file securely and never stores your data permanently.",
      details: [
        "Supports multiple file formats",
        "Secure file processing",
        "No permanent storage",
        "Fast upload speeds",
      ],
      color: "text-emerald-700",
      bgColor: "bg-emerald-50",
    },
    {
      icon: Brain,
      title: "Simplify",
      description:
        "AI analyzes complex legal language and converts it into simple, easy-to-understand terms using advanced natural language processing.",
      details: [
        "Advanced AI analysis",
        "Legal jargon translation",
        "Context-aware simplification",
        "Maintains legal accuracy",
      ],
      color: "text-emerald-700",
      bgColor: "bg-emerald-50",
    },
    {
      icon: CheckCircle,
      title: "Understand",
      description:
        "Get clear explanations and actionable insights about your document in your preferred language with highlighted key points.",
      details: ["Clear explanations", "Key point highlighting", "Multi-language support", "Actionable insights"],
      color: "text-slate-600",
      bgColor: "bg-slate-50",
    },
  ]

  const features = [
    {
      icon: Languages,
      title: "Multi-Language Support",
      description: "Get your documents simplified in Hindi, English, and various regional languages.",
    },
    {
      icon: Shield,
      title: "Privacy & Security",
      description: "Your documents are processed securely with end-to-end encryption and never stored.",
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Get results in seconds, not hours. Our AI processes documents instantly.",
    },
    {
      icon: FileText,
      title: "Multiple Formats",
      description: "Support for PDF, DOC, DOCX, and image files including scanned documents.",
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-stone-50 via-amber-50 to-emerald-50">
      {/* Hero Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-5xl font-bold text-gray-900 mb-6">How It Works</h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Three simple steps to understand your legal documents. Our AI-powered platform makes complex legal
              language accessible to everyone.
            </p>
          </motion.div>

          {/* Steps */}
          <div className="space-y-16">
            {steps.map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.2 }}
                viewport={{ once: true }}
                className={`flex flex-col ${index % 2 === 1 ? "lg:flex-row-reverse" : "lg:flex-row"} items-center gap-12`}
              >
                <div className="flex-1 space-y-6">
                  <div className="flex items-center space-x-4">
                    <div className={`p-4 rounded-full ${step.bgColor} ${step.color}`}>
                      <step.icon className="h-8 w-8" />
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-500">STEP {index + 1}</span>
                      <h2 className="text-3xl font-bold text-gray-900">{step.title}</h2>
                    </div>
                  </div>

                  <p className="text-lg text-gray-600 leading-relaxed">{step.description}</p>

                  <div className="grid grid-cols-2 gap-4">
                    {step.details.map((detail, detailIndex) => (
                      <div key={detailIndex} className="flex items-center space-x-2">
                        <CheckCircle className="h-4 w-4 text-emerald-600" />
                        <span className="text-sm text-gray-600">{detail}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="flex-1">
                  <Card className={`p-8 ${step.bgColor} border-none shadow-lg`}>
                    <CardContent className="space-y-6">
                      <div className="text-center">
                        <div className={`inline-flex p-6 rounded-full bg-white ${step.color} shadow-lg`}>
                          <step.icon className="h-12 w-12" />
                        </div>
                      </div>

                      {index === 0 && (
                        <div className="space-y-4">
                          <div className="bg-white rounded-lg p-4 shadow">
                            <div className="flex items-center space-x-3">
                              <FileText className="h-6 w-6 text-emerald-700" />
                              <span className="font-medium">contract.pdf</span>
                            </div>
                          </div>
                          <div className="text-center">
                            <Upload className="h-8 w-8 text-emerald-700 mx-auto animate-bounce" />
                          </div>
                        </div>
                      )}

                      {index === 1 && (
                        <div className="space-y-4">
                          <div className="bg-white rounded-lg p-4 shadow">
                            <div className="flex items-center justify-center">
                              <Brain className="h-12 w-12 text-emerald-700 animate-pulse" />
                            </div>
                            <div className="mt-4 space-y-2">
                              <div className="h-2 bg-emerald-200 rounded animate-pulse"></div>
                              <div className="h-2 bg-emerald-200 rounded w-3/4 animate-pulse"></div>
                            </div>
                          </div>
                        </div>
                      )}

                      {index === 2 && (
                        <div className="space-y-4">
                          <div className="bg-white rounded-lg p-4 shadow">
                            <div className="flex items-center space-x-2 mb-3">
                              <CheckCircle className="h-5 w-5 text-emerald-600" />
                              <span className="font-medium text-green-700">Simplified</span>
                            </div>
                            <div className="space-y-2">
                              <div className="h-2 bg-slate-200 rounded"></div>
                              <div className="h-2 bg-slate-200 rounded w-4/5"></div>
                              <div className="h-2 bg-slate-200 rounded w-3/5"></div>
                            </div>
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 bg-gradient-to-br from-stone-50 to-amber-50">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Frequently Asked Questions</h2>
            <p className="text-xl text-gray-600">Get answers to common questions about our process</p>
          </motion.div>

          <div className="max-w-4xl mx-auto space-y-6">
            {[
              {
                step: "Upload",
                question: "What file formats do you support?",
                answer:
                  "We support PDF, DOC, DOCX, JPG, and PNG files up to 10MB each. Our AI can process both digital documents and scanned images with high accuracy.",
                icon: Upload,
                color: "blue",
              },
              {
                step: "Upload",
                question: "Is my document secure during upload?",
                answer:
                  "Absolutely! We use bank-level 256-bit SSL encryption for all uploads. Your documents are processed immediately and permanently deleted from our servers within 24 hours.",
                icon: Shield,
                color: "blue",
              },
              {
                step: "Simplify",
                question: "How accurate is the AI simplification?",
                answer:
                  "Our AI maintains 99.9% accuracy while simplifying legal language. It's trained on millions of legal documents and continuously learns from legal experts to ensure precision.",
                icon: Brain,
                color: "green",
              },
              {
                step: "Simplify",
                question: "Does the AI change the legal meaning?",
                answer:
                  "No, our AI preserves the original legal meaning while making it easier to understand. It translates complex jargon into plain language without altering the document's intent.",
                icon: CheckCircle,
                color: "green",
              },
              {
                step: "Understand",
                question: "Can I get explanations in different languages?",
                answer:
                  "Yes! We support Hindi, English, and 10+ regional Indian languages. You can choose your preferred language for the simplified explanation.",
                icon: Languages,
                color: "purple",
              },
              {
                step: "Understand",
                question: "What if I need legal advice?",
                answer:
                  "While we simplify documents, we don't provide legal advice. For complex legal matters, we recommend consulting with a qualified attorney. Our platform helps you understand documents better before seeking professional help.",
                icon: Users,
                color: "purple",
              },
            ].map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <Card className="hover:shadow-lg transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-start space-x-4">
                      <div
                        className={`p-3 rounded-lg ${
                          faq.color === "blue"
                            ? "bg-blue-100"
                            : faq.color === "green"
                              ? "bg-green-100"
                              : "bg-purple-100"
                        }`}
                      >
                        <faq.icon
                          className={`h-6 w-6 ${
                            faq.color === "blue"
                              ? "text-blue-600"
                              : faq.color === "green"
                                ? "text-green-600"
                                : "text-purple-600"
                          }`}
                        />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <span
                            className={`text-xs font-medium px-2 py-1 rounded ${
                              faq.color === "blue"
                                ? "bg-blue-100 text-blue-800"
                                : faq.color === "green"
                                  ? "bg-green-100 text-green-800"
                                  : "bg-purple-100 text-purple-800"
                            }`}
                          >
                            {faq.step}
                          </span>
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">{faq.question}</h3>
                        <p className="text-gray-600 leading-relaxed">{faq.answer}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* AI Processing Visualization */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">AI Processing Timeline</h2>
            <p className="text-xl text-gray-600">See how our AI transforms your document in real-time</p>
          </motion.div>

          <div className="max-w-6xl mx-auto">
            <div className="relative">
              {/* Timeline Line */}
              <div className="absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-gradient-to-b from-blue-500 via-green-500 to-purple-500 rounded-full"></div>

              <div className="space-y-16">
                {[
                  {
                    time: "0-5 seconds",
                    title: "Document Analysis",
                    description: "AI scans and identifies document structure, legal clauses, and key terms",
                    details: [
                      "OCR text extraction",
                      "Document type classification",
                      "Legal term identification",
                      "Structure mapping",
                    ],
                    icon: "🔍",
                    side: "left",
                  },
                  {
                    time: "5-15 seconds",
                    title: "Language Processing",
                    description:
                      "Advanced NLP algorithms break down complex legal language into understandable components",
                    details: [
                      "Syntax analysis",
                      "Legal jargon detection",
                      "Context understanding",
                      "Meaning preservation",
                    ],
                    icon: "🧠",
                    side: "right",
                  },
                  {
                    time: "15-25 seconds",
                    title: "Simplification",
                    description: "AI rewrites complex terms in plain language while maintaining legal accuracy",
                    details: [
                      "Plain language conversion",
                      "Readability optimization",
                      "Legal accuracy check",
                      "Context preservation",
                    ],
                    icon: "✨",
                    side: "left",
                  },
                  {
                    time: "25-30 seconds",
                    title: "Quality Assurance",
                    description: "Final review ensures accuracy and completeness of the simplified document",
                    details: ["Accuracy verification", "Completeness check", "Format optimization", "Final review"],
                    icon: "✅",
                    side: "right",
                  },
                ].map((step, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: step.side === "left" ? -50 : 50 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.8, delay: index * 0.2 }}
                    viewport={{ once: true }}
                    className={`flex items-center ${step.side === "right" ? "flex-row-reverse" : ""}`}
                  >
                    <div className={`w-5/12 ${step.side === "right" ? "text-right" : ""}`}>
                      <Card className="p-6 shadow-lg hover:shadow-xl transition-shadow">
                        <CardContent className="space-y-4">
                          <div
                            className={`flex items-center space-x-3 ${step.side === "right" ? "flex-row-reverse space-x-reverse" : ""}`}
                          >
                            <div className="text-3xl">{step.icon}</div>
                            <div>
                              <div className="text-sm text-green-600 font-medium">{step.time}</div>
                              <h3 className="text-xl font-bold text-gray-900">{step.title}</h3>
                            </div>
                          </div>
                          <p className="text-gray-600">{step.description}</p>
                          <div className="grid grid-cols-2 gap-2">
                            {step.details.map((detail, detailIndex) => (
                              <div key={detailIndex} className="flex items-center space-x-2">
                                <CheckCircle className="h-3 w-3 text-emerald-600" />
                                <span className="text-xs text-gray-500">{detail}</span>
                              </div>
                            ))}
                          </div>
                        </CardContent>
                      </Card>
                    </div>

                    {/* Timeline Node */}
                    <div className="w-2/12 flex justify-center">
                      <div className="w-8 h-8 bg-white border-4 border-emerald-600 rounded-full flex items-center justify-center shadow-lg">
                        <div className="w-3 h-3 bg-emerald-600 rounded-full"></div>
                      </div>
                    </div>

                    <div className="w-5/12"></div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Why Our Process Works</h2>
            <p className="text-xl text-gray-600">
              Advanced features that make legal document simplification reliable and secure
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <Card className="text-center p-6 h-full hover:shadow-lg transition-shadow">
                  <CardContent className="space-y-4">
                    <div className="inline-flex p-4 rounded-full bg-gradient-to-br from-blue-50 to-purple-50">
                      <feature.icon className="h-8 w-8 text-blue-600" />
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900">{feature.title}</h3>
                    <p className="text-gray-600">{feature.description}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-emerald-700 to-slate-700">
        <div className="container mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="space-y-8"
          >
            <h2 className="text-4xl font-bold text-white">Ready to Try It Yourself?</h2>
            <p className="text-xl text-blue-100 max-w-2xl mx-auto">
              Upload your first document and see how our AI can simplify complex legal language in seconds.
            </p>
            <Link href="/upload">
              <Button
                size="lg"
                variant="secondary"
                className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-4 text-lg"
              >
                <Upload className="mr-2 h-5 w-5" />
                Upload Your Document
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
