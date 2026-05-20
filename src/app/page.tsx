"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import {
  Upload,
  FileText,
  Brain,
  CheckCircle,
  Shield,
  Smartphone,
  Users,
  ArrowRight,
  Star,
  Clock,
  Award,
} from "lucide-react"
import Link from "next/link"
import { motion } from "framer-motion"

export default function HomePage() {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
  }, [])

  const fadeInUp = {
    initial: { opacity: 0, y: 60 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 },
  }

  const staggerChildren = {
    animate: {
      transition: {
        staggerChildren: 0.1,
      },
    },
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: "#F2FFF5" }}>
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <motion.div
            className="space-y-8"
            initial="initial"
            animate={isVisible ? "animate" : "initial"}
            variants={staggerChildren}
          >
            <motion.h1 className="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight" variants={fadeInUp}>
              Making Legal<span className="text-[#40684D] italic">सरल</span> Documents
            </motion.h1>

            <motion.p className="text-xl text-gray-600 leading-relaxed" variants={fadeInUp}>
              Upload your documents and get instant clarity on your legal matters with our AI-powered simplification
              platform.
            </motion.p>

            <motion.div className="flex flex-col sm:flex-row gap-4" variants={fadeInUp}>
              <Link href="/upload">
                <Button size="lg" className="bg-[#40684D] hover:bg-[#355a42] text-white px-8 py-4 text-lg">
                  <Upload className="mr-2 h-5 w-5" />
                  Upload Document
                </Button>
              </Link>
              <Link href="/how-it-works">
                <Button
                  variant="outline"
                  size="lg"
                  className="px-8 py-4 text-lg border-[#40684D] text-[#40684D] hover:bg-green-50 bg-transparent"
                >
                  See How It Works
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </motion.div>

            {/* Trust Indicators */}
            <motion.div className="flex items-center space-x-6 pt-4" variants={fadeInUp}>
              <div className="flex items-center space-x-1">
                <div className="flex">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>
                <span className="text-sm text-gray-600 ml-2">4.9/5 rating</span>
              </div>
              <div className="flex items-center space-x-2">
                <Award className="h-4 w-4 text-[#40684D]" />
                <span className="text-sm text-gray-600">99.9% accuracy</span>
              </div>
              <div className="flex items-center space-x-2">
                <Clock className="h-4 w-4 text-[#40684D]" />
                <span className="text-sm text-gray-600">30-second processing</span>
              </div>
            </motion.div>
          </motion.div>

          <motion.div
            className="relative"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-3xl p-8 shadow-2xl">
              <div className="grid grid-cols-2 gap-4 mb-6">
                <motion.div
                  className="bg-white rounded-lg p-4 shadow-lg"
                  animate={{ y: [0, -10, 0] }}
                  transition={{ duration: 3, repeat: Number.POSITIVE_INFINITY, delay: 0 }}
                >
                  <FileText className="h-8 w-8 text-blue-600 mb-2" />
                  <div className="h-2 bg-gray-200 rounded mb-1"></div>
                  <div className="h-2 bg-gray-200 rounded w-3/4"></div>
                </motion.div>
                <motion.div
                  className="bg-white rounded-lg p-4 shadow-lg"
                  animate={{ y: [0, -10, 0] }}
                  transition={{ duration: 3, repeat: Number.POSITIVE_INFINITY, delay: 0.5 }}
                >
                  <FileText className="h-8 w-8 text-[#40684D] mb-2" />
                  <div className="h-2 bg-gray-200 rounded mb-1"></div>
                  <div className="h-2 bg-gray-200 rounded w-2/3"></div>
                </motion.div>
              </div>

              <div className="flex justify-center mb-6">
                <motion.div
                  className="bg-[#40684D] rounded-full p-4"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 8, repeat: Number.POSITIVE_INFINITY, ease: "linear" }}
                >
                  <Brain className="h-12 w-12 text-white" />
                </motion.div>
              </div>

              <div className="bg-white rounded-lg p-4 shadow-lg">
                <div className="flex items-center mb-2">
                  <CheckCircle className="h-5 w-5 text-[#40684D] mr-2" />
                  <span className="text-sm font-medium">SIMPLIFIED</span>
                </div>
                <div className="space-y-2">
                  <div className="h-2 bg-green-100 rounded"></div>
                  <div className="h-2 bg-green-100 rounded w-4/5"></div>
                  <div className="h-2 bg-green-100 rounded w-3/5"></div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Supported Document Types Banner */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-12"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Legal Documents We Support</h2>
            <p className="text-lg text-gray-600">
              Our AI understands and simplifies all types of legal documents with precision and accuracy
            </p>
          </motion.div>

          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
            {[
              {
                name: "Affidavits",
                icon: "📋",
                description: "Sworn statements and declarations",
                complexity: "Medium",
              },
              { name: "Agreements", icon: "🤝", description: "Contracts and legal agreements", complexity: "High" },
              { name: "Court Orders", icon: "⚖️", description: "Judicial decisions and orders", complexity: "High" },
              { name: "Property Deeds", icon: "🏠", description: "Real estate documents", complexity: "Medium" },
              { name: "Wills & Trusts", icon: "📜", description: "Estate planning documents", complexity: "High" },
              { name: "Legal Notices", icon: "📢", description: "Official legal notifications", complexity: "Low" },
              { name: "Power of Attorney", icon: "✍️", description: "Authorization documents", complexity: "Medium" },
              { name: "Divorce Papers", icon: "💔", description: "Family law documents", complexity: "High" },
              {
                name: "Employment Contracts",
                icon: "💼",
                description: "Work-related agreements",
                complexity: "Medium",
              },
              { name: "Insurance Policies", icon: "🛡️", description: "Coverage documents", complexity: "Medium" },
              { name: "Loan Documents", icon: "💰", description: "Financial agreements", complexity: "High" },
              { name: "Lease Agreements", icon: "🔑", description: "Rental contracts", complexity: "Medium" },
            ].map((doc, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ scale: 1.05, y: -5 }}
                className="group"
              >
                <Card className="p-4 text-center h-full hover:shadow-lg transition-all duration-300 bg-white border-green-100">
                  <CardContent className="space-y-3">
                    <div className="text-3xl group-hover:scale-110 transition-transform duration-300">{doc.icon}</div>
                    <h3 className="font-semibold text-gray-900 text-sm">{doc.name}</h3>
                    <p className="text-xs text-gray-600 leading-relaxed">{doc.description}</p>
                    <div
                      className={`text-xs px-2 py-1 rounded-full ${
                        doc.complexity === "High"
                          ? "bg-red-100 text-red-700"
                          : doc.complexity === "Medium"
                            ? "bg-yellow-100 text-yellow-700"
                            : "bg-green-100 text-green-700"
                      }`}
                    >
                      {doc.complexity} Complexity
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>

          <motion.div
            className="text-center mt-12"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.8 }}
            viewport={{ once: true }}
          >
            <p className="text-gray-600 mb-6">
              Don't see your document type? We support 50+ legal document formats and continuously add more!
            </p>
            <Link href="/upload">
              <Button className="bg-[#40684D] hover:bg-[#355a42] text-white px-8 py-3">
                Upload Any Document
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Trust Indicators */}
      <section className="py-16" style={{ backgroundColor: "#F2FFF5" }}>
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-12"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Trusted by Legal Professionals Nationwide</h2>
            <p className="text-lg text-gray-600">
              Join thousands who rely on Nyay-Mitra for legal clarity and understanding
            </p>
          </motion.div>

          <div className="grid md:grid-cols-4 gap-8 mb-12">
            {[
              { number: "50,000+", label: "Documents Processed", icon: "📄", growth: "+25% this month" },
              { number: "25,000+", label: "Happy Users", icon: "😊", growth: "4.9/5 rating" },
              { number: "99.9%", label: "Accuracy Rate", icon: "🎯", growth: "Verified by experts" },
              { number: "24/7", label: "Support Available", icon: "🕒", growth: "< 2min response" },
            ].map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center bg-white rounded-lg p-6 shadow-sm"
              >
                <div className="text-4xl mb-2">{stat.icon}</div>
                <div className="text-3xl font-bold text-[#40684D] mb-1">{stat.number}</div>
                <div className="text-gray-600 mb-2">{stat.label}</div>
                <div className="text-xs text-green-600 bg-green-50 px-2 py-1 rounded">{stat.growth}</div>
              </motion.div>
            ))}
          </div>

          <div className="bg-white rounded-2xl p-8 shadow-sm">
            <div className="grid md:grid-cols-3 gap-6">
              {[
                {
                  title: "Bank-Level Security",
                  description: "256-bit SSL encryption protects your documents with military-grade security",
                  icon: "🔒",
                  features: ["End-to-end encryption", "Zero data retention", "SOC 2 compliant"],
                },
                {
                  title: "No Data Storage",
                  description: "Documents are processed instantly and permanently deleted within 24 hours",
                  icon: "🗑️",
                  features: ["Immediate processing", "Auto-deletion", "No cloud storage"],
                },
                {
                  title: "GDPR Compliant",
                  description: "Full compliance with international privacy laws and data protection standards",
                  icon: "✅",
                  features: ["Privacy by design", "Data minimization", "User control"],
                },
              ].map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.2 }}
                  viewport={{ once: true }}
                  className="text-center"
                >
                  <div className="text-3xl mb-3">{feature.icon}</div>
                  <h3 className="font-semibold text-gray-900 mb-2">{feature.title}</h3>
                  <p className="text-gray-600 text-sm mb-3">{feature.description}</p>
                  <ul className="text-xs text-gray-500 space-y-1">
                    {feature.features.map((item, idx) => (
                      <li key={idx} className="flex items-center justify-center space-x-1">
                        <CheckCircle className="h-3 w-3 text-[#40684D]" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Preview */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">How It Works</h2>
            <p className="text-xl text-gray-600">
              Three simple steps to understand your legal documents in plain English
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Upload,
                title: "Upload",
                description:
                  "Upload your legal document in PDF, DOC, or image format. Our AI processes your file securely with bank-level encryption.",
                color: "text-blue-600",
                time: "< 5 seconds",
                features: ["Drag & drop", "Multiple formats", "Secure upload"],
              },
              {
                icon: Brain,
                title: "Simplify",
                description:
                  "AI analyzes complex legal language and converts it into simple, easy-to-understand terms while maintaining legal accuracy.",
                color: "text-[#40684D]",
                time: "15-30 seconds",
                features: ["AI analysis", "Plain language", "Context preserved"],
              },
              {
                icon: CheckCircle,
                title: "Understand",
                description:
                  "Get clear explanations and actionable insights about your document with highlighted key points and summaries.",
                color: "text-purple-600",
                time: "Instant",
                features: ["Key highlights", "Action items", "Summary"],
              },
            ].map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
              >
                <Card className="text-center p-8 h-full hover:shadow-lg transition-shadow">
                  <CardContent className="space-y-4">
                    <div className={`inline-flex p-4 rounded-full bg-gray-50 ${step.color}`}>
                      <step.icon className="h-8 w-8" />
                    </div>
                    <div className="text-sm text-[#40684D] font-medium">{step.time}</div>
                    <h3 className="text-2xl font-semibold text-gray-900">{step.title}</h3>
                    <p className="text-gray-600 leading-relaxed">{step.description}</p>
                    <div className="flex justify-center space-x-4 text-xs text-gray-500">
                      {step.features.map((feature, idx) => (
                        <span key={idx} className="bg-gray-100 px-2 py-1 rounded">
                          {feature}
                        </span>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20" style={{ backgroundColor: "#F2FFF5" }}>
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Why Choose Nyay-Mitra?</h2>
            <p className="text-xl text-gray-600">
              Powerful AI features designed to make legal documents accessible to everyone
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Shield,
                title: "Secure & Private",
                description:
                  "Your documents are processed securely with end-to-end encryption and never stored permanently",
                color: "text-[#40684D]",
                benefits: ["Zero data retention", "Military-grade encryption", "Privacy compliant"],
              },
              {
                icon: CheckCircle,
                title: "Expert Results",
                description:
                  "Get simplified explanations in seconds with 99.9% accuracy verified by legal professionals",
                color: "text-purple-600",
                benefits: ["Legal expert verified", "Instant results", "High accuracy"],
              },
              {
                icon: Brain,
                title: "Legal Accuracy",
                description:
                  "AI trained specifically on Indian legal documents and procedures for contextual understanding",
                color: "text-orange-600",
                benefits: ["India-specific training", "Legal context", "Continuous learning"],
              },
              {
                icon: Smartphone,
                title: "Mobile Friendly",
                description: "Access from anywhere on any device with our responsive design and mobile optimization",
                color: "text-pink-600",
                benefits: ["Responsive design", "Cross-platform", "Offline capable"],
              },
              {
                icon: Users,
                title: "Expert Support",
                description: "Get help from our team of legal and technical experts available 24/7 for assistance",
                color: "text-indigo-600",
                benefits: ["24/7 availability", "Legal experts", "Technical support"],
              },
              {
                icon: Clock,
                title: "Lightning Fast",
                description: "Process documents in under 30 seconds with our optimized AI infrastructure",
                color: "text-blue-600",
                benefits: ["30-second processing", "Optimized AI", "Scalable infrastructure"],
              },
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <Card className="p-6 h-full hover:shadow-lg transition-all hover:-translate-y-1 bg-white">
                  <CardContent className="space-y-4">
                    <div className={`inline-flex p-3 rounded-lg bg-gray-50 ${feature.color}`}>
                      <feature.icon className="h-6 w-6" />
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900">{feature.title}</h3>
                    <p className="text-gray-600">{feature.description}</p>
                    <ul className="space-y-1">
                      {feature.benefits.map((benefit, idx) => (
                        <li key={idx} className="flex items-center space-x-2 text-sm text-gray-500">
                          <CheckCircle className="h-3 w-3 text-[#40684D]" />
                          <span>{benefit}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-[#40684D]">
        <div className="container mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="space-y-8"
          >
            <h2 className="text-4xl font-bold text-white">Ready to Simplify Your Legal Documents?</h2>
            <p className="text-xl text-green-100 max-w-2xl mx-auto">
              Join thousands of users who trust Nyay-Mitra to make legal documents understandable. Start your free trial
              today.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/upload">
                <Button
                  size="lg"
                  variant="secondary"
                  className="bg-white text-[#40684D] hover:bg-gray-100 px-8 py-4 text-lg"
                >
                  <Upload className="mr-2 h-5 w-5" />
                  Get Started Free
                </Button>
              </Link>
              <Link href="/sign-in">
                <Button
                  size="lg"
                  variant="outline"
                  className="border-white text-white hover:bg-white hover:text-[#40684D] px-8 py-4 text-lg bg-transparent"
                >
                  Sign In
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
