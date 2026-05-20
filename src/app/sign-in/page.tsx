"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Checkbox } from "@/components/ui/checkbox"
import { Alert, AlertDescription } from "@/components/ui/alert"
import {
  Eye,
  EyeOff,
  Mail,
  Lock,
  ArrowRight,
  CheckCircle,
  AlertCircle,
  User,
  Phone,
  Building,
  Shield,
  Zap,
  Clock,
} from "lucide-react"
import Link from "next/link"
import { motion } from "framer-motion"

export default function SignInPage() {
  const [isSignUp, setIsSignUp] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")

  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
    firstName: "",
    lastName: "",
    phone: "",
    organization: "",
    agreeToTerms: false,
    rememberMe: false,
  })

  const [formErrors, setFormErrors] = useState({
    email: "",
    password: "",
    confirmPassword: "",
    firstName: "",
    lastName: "",
    phone: "",
    organization: "",
    agreeToTerms: "",
  })

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  const validatePassword = (password: string) => {
    return password.length >= 8 && /[A-Z]/.test(password) && /[a-z]/.test(password) && /\d/.test(password)
  }

  const validateForm = () => {
    const errors = {
      email: "",
      password: "",
      confirmPassword: "",
      firstName: "",
      lastName: "",
      phone: "",
      organization: "",
      agreeToTerms: "",
    }

    if (!formData.email) {
      errors.email = "Email is required"
    } else if (!validateEmail(formData.email)) {
      errors.email = "Please enter a valid email address"
    }

    if (!formData.password) {
      errors.password = "Password is required"
    } else if (isSignUp && !validatePassword(formData.password)) {
      errors.password = "Password must be at least 8 characters with uppercase, lowercase, and number"
    }

    if (isSignUp) {
      if (!formData.firstName) {
        errors.firstName = "First name is required"
      }

      if (!formData.lastName) {
        errors.lastName = "Last name is required"
      }

      if (formData.password !== formData.confirmPassword) {
        errors.confirmPassword = "Passwords do not match"
      }

      if (!formData.agreeToTerms) {
        errors.agreeToTerms = "You must agree to the terms and conditions"
      }
    }

    setFormErrors(errors)
    return Object.values(errors).every((error) => error === "")
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setSuccess("")

    if (!validateForm()) {
      return
    }

    setIsLoading(true)

    // Simulate API call
    try {
      await new Promise((resolve) => setTimeout(resolve, 2000))

      if (isSignUp) {
        setSuccess("Account created successfully! Please check your email to verify your account.")
      } else {
        setSuccess("Sign in successful! Redirecting to dashboard...")
        // Simulate redirect
        setTimeout(() => {
          window.location.href = "/dashboard"
        }, 1500)
      }
    } catch (err) {
      setError("An error occurred. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }))

    // Clear error when user starts typing
    if (formErrors[name as keyof typeof formErrors]) {
      setFormErrors((prev) => ({
        ...prev,
        [name]: "",
      }))
    }
  }

  const handleSocialLogin = (provider: string) => {
    setIsLoading(true)
    // Simulate social login
    setTimeout(() => {
      setIsLoading(false)
      setSuccess(`${provider} login successful! Redirecting...`)
    }, 1500)
  }

  return (
    <div className="min-h-screen flex items-center justify-center py-12" style={{ backgroundColor: "#F2FFF5" }}>
      <div className="container mx-auto px-4">
        <div className="grid lg:grid-cols-2 gap-12 max-w-6xl mx-auto items-center">
          {/* Left Side - Benefits */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="hidden lg:block space-y-8"
          >
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                {isSignUp ? "Join" : "Welcome back to"} <span className="text-[#40684D]">Nyay-Mitra</span>
              </h1>
              <p className="text-xl text-gray-600">
                {isSignUp
                  ? "Create your account and start simplifying legal documents with AI-powered clarity."
                  : "Continue simplifying your legal documents with AI-powered clarity."}
              </p>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-sm">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">
                {isSignUp ? "Why create an account?" : "Account benefits:"}
              </h3>

              <div className="space-y-4">
                {[
                  {
                    icon: Shield,
                    title: "Secure Document History",
                    description: "Access all your processed documents with bank-level security",
                  },
                  {
                    icon: Zap,
                    title: "Priority Processing",
                    description: "Skip the queue with 2x faster document processing",
                  },
                  {
                    icon: Clock,
                    title: "24/7 Expert Support",
                    description: "Get help from legal and technical experts anytime",
                  },
                ].map((benefit, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.2 + index * 0.1 }}
                    className="flex items-start space-x-3"
                  >
                    <div className="p-2 bg-green-50 rounded-lg">
                      <benefit.icon className="h-5 w-5 text-[#40684D]" />
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900">{benefit.title}</h4>
                      <p className="text-sm text-gray-600">{benefit.description}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Right Side - Form */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <Card className="shadow-xl border-0 bg-white">
              <CardHeader className="text-center pb-6">
                <CardTitle className="text-3xl font-bold text-gray-900">
                  {isSignUp ? "Create Account" : "Sign In"}
                </CardTitle>
                <p className="text-gray-600 mt-2">
                  {isSignUp
                    ? "Join thousands of users simplifying legal documents"
                    : "Access your Nyay-Mitra dashboard"}
                </p>
              </CardHeader>

              <CardContent className="space-y-6">
                {/* Error/Success Messages */}
                {error && (
                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}

                {success && (
                  <Alert className="border-green-200 bg-green-50">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <AlertDescription className="text-green-800">{success}</AlertDescription>
                  </Alert>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                  {/* Name Fields (Sign Up Only) */}
                  {isSignUp && (
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="firstName">First Name</Label>
                        <div className="relative">
                          <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                          <Input
                            id="firstName"
                            name="firstName"
                            value={formData.firstName}
                            onChange={handleChange}
                            placeholder="John"
                            className={`pl-10 ${formErrors.firstName ? "border-red-500" : ""}`}
                            required={isSignUp}
                          />
                        </div>
                        {formErrors.firstName && <p className="text-sm text-red-600">{formErrors.firstName}</p>}
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="lastName">Last Name</Label>
                        <div className="relative">
                          <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                          <Input
                            id="lastName"
                            name="lastName"
                            value={formData.lastName}
                            onChange={handleChange}
                            placeholder="Doe"
                            className={`pl-10 ${formErrors.lastName ? "border-red-500" : ""}`}
                            required={isSignUp}
                          />
                        </div>
                        {formErrors.lastName && <p className="text-sm text-red-600">{formErrors.lastName}</p>}
                      </div>
                    </div>
                  )}

                  {/* Email */}
                  <div className="space-y-2">
                    <Label htmlFor="email">Email Address</Label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input
                        id="email"
                        name="email"
                        type="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="your.email@example.com"
                        className={`pl-10 ${formErrors.email ? "border-red-500" : ""}`}
                        required
                      />
                    </div>
                    {formErrors.email && <p className="text-sm text-red-600">{formErrors.email}</p>}
                  </div>

                  {/* Phone & Organization (Sign Up Only) */}
                  {isSignUp && (
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="phone">Phone (Optional)</Label>
                        <div className="relative">
                          <Phone className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                          <Input
                            id="phone"
                            name="phone"
                            value={formData.phone}
                            onChange={handleChange}
                            placeholder="+91 98765 43210"
                            className="pl-10"
                          />
                        </div>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="organization">Organization (Optional)</Label>
                        <div className="relative">
                          <Building className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                          <Input
                            id="organization"
                            name="organization"
                            value={formData.organization}
                            onChange={handleChange}
                            placeholder="Law Firm / Company"
                            className="pl-10"
                          />
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Password */}
                  <div className="space-y-2">
                    <Label htmlFor="password">Password</Label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input
                        id="password"
                        name="password"
                        type={showPassword ? "text" : "password"}
                        value={formData.password}
                        onChange={handleChange}
                        placeholder={isSignUp ? "Create a strong password" : "Enter your password"}
                        className={`pl-10 pr-10 ${formErrors.password ? "border-red-500" : ""}`}
                        required
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                      >
                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                      </button>
                    </div>
                    {formErrors.password && <p className="text-sm text-red-600">{formErrors.password}</p>}
                    {isSignUp && (
                      <div className="text-xs text-gray-500 space-y-1">
                        <p>Password must contain:</p>
                        <ul className="list-disc list-inside space-y-1">
                          <li className={formData.password.length >= 8 ? "text-green-600" : ""}>
                            At least 8 characters
                          </li>
                          <li className={/[A-Z]/.test(formData.password) ? "text-green-600" : ""}>
                            One uppercase letter
                          </li>
                          <li className={/[a-z]/.test(formData.password) ? "text-green-600" : ""}>
                            One lowercase letter
                          </li>
                          <li className={/\d/.test(formData.password) ? "text-green-600" : ""}>One number</li>
                        </ul>
                      </div>
                    )}
                  </div>

                  {/* Confirm Password (Sign Up Only) */}
                  {isSignUp && (
                    <div className="space-y-2">
                      <Label htmlFor="confirmPassword">Confirm Password</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                        <Input
                          id="confirmPassword"
                          name="confirmPassword"
                          type={showConfirmPassword ? "text" : "password"}
                          value={formData.confirmPassword}
                          onChange={handleChange}
                          placeholder="Confirm your password"
                          className={`pl-10 pr-10 ${formErrors.confirmPassword ? "border-red-500" : ""}`}
                          required={isSignUp}
                        />
                        <button
                          type="button"
                          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                          className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                        >
                          {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </button>
                      </div>
                      {formErrors.confirmPassword && (
                        <p className="text-sm text-red-600">{formErrors.confirmPassword}</p>
                      )}
                    </div>
                  )}

                  {/* Checkboxes */}
                  <div className="space-y-3">
                    {!isSignUp && (
                      <div className="flex items-center space-x-2">
                        <Checkbox
                          id="rememberMe"
                          name="rememberMe"
                          checked={formData.rememberMe}
                          onCheckedChange={(checked) =>
                            setFormData((prev) => ({ ...prev, rememberMe: checked as boolean }))
                          }
                        />
                        <Label htmlFor="rememberMe" className="text-sm text-gray-600">
                          Remember me for 30 days
                        </Label>
                      </div>
                    )}

                    {isSignUp && (
                      <div className="space-y-2">
                        <div className="flex items-start space-x-2">
                          <Checkbox
                            id="agreeToTerms"
                            name="agreeToTerms"
                            checked={formData.agreeToTerms}
                            onCheckedChange={(checked) =>
                              setFormData((prev) => ({ ...prev, agreeToTerms: checked as boolean }))
                            }
                            className={formErrors.agreeToTerms ? "border-red-500" : ""}
                          />
                          <Label htmlFor="agreeToTerms" className="text-sm text-gray-600 leading-relaxed">
                            I agree to the{" "}
                            <Link href="/terms" className="text-[#40684D] hover:underline">
                              Terms of Service
                            </Link>{" "}
                            and{" "}
                            <Link href="/privacy" className="text-[#40684D] hover:underline">
                              Privacy Policy
                            </Link>
                          </Label>
                        </div>
                        {formErrors.agreeToTerms && <p className="text-sm text-red-600">{formErrors.agreeToTerms}</p>}
                      </div>
                    )}
                  </div>

                  {/* Forgot Password Link (Sign In Only) */}
                  {!isSignUp && (
                    <div className="text-right">
                      <Link href="/forgot-password" className="text-sm text-[#40684D] hover:underline">
                        Forgot your password?
                      </Link>
                    </div>
                  )}

                  {/* Submit Button */}
                  <Button
                    type="submit"
                    disabled={isLoading}
                    className="w-full bg-[#40684D] hover:bg-[#355a42] text-white py-3"
                    size="lg"
                  >
                    {isLoading ? (
                      <div className="flex items-center space-x-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        <span>{isSignUp ? "Creating Account..." : "Signing In..."}</span>
                      </div>
                    ) : (
                      <>
                        {isSignUp ? "Create Account" : "Sign In"}
                        <ArrowRight className="ml-2 h-4 w-4" />
                      </>
                    )}
                  </Button>
                </form>

                {/* Social Login */}
                <div className="relative">
                  <Separator />
                  <span className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-white px-4 text-sm text-gray-500">
                    Or continue with
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => handleSocialLogin("Google")}
                    disabled={isLoading}
                    className="w-full"
                  >
                    <svg className="mr-2 h-4 w-4" viewBox="0 0 24 24">
                      <path
                        fill="currentColor"
                        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                      />
                      <path
                        fill="currentColor"
                        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                      />
                      <path
                        fill="currentColor"
                        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                      />
                      <path
                        fill="currentColor"
                        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                      />
                    </svg>
                    Google
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => handleSocialLogin("Microsoft")}
                    disabled={isLoading}
                    className="w-full"
                  >
                    <svg className="mr-2 h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M11.4 24H0V12.6h11.4V24zM24 24H12.6V12.6H24V24zM11.4 11.4H0V0h11.4v11.4zM24 11.4H12.6V0H24v11.4z" />
                    </svg>
                    Microsoft
                  </Button>
                </div>

                {/* Toggle Sign In/Sign Up */}
                <div className="text-center">
                  <p className="text-sm text-gray-600">
                    {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
                    <button
                      type="button"
                      onClick={() => {
                        setIsSignUp(!isSignUp)
                        setFormData({
                          email: "",
                          password: "",
                          confirmPassword: "",
                          firstName: "",
                          lastName: "",
                          phone: "",
                          organization: "",
                          agreeToTerms: false,
                          rememberMe: false,
                        })
                        setFormErrors({
                          email: "",
                          password: "",
                          confirmPassword: "",
                          firstName: "",
                          lastName: "",
                          phone: "",
                          organization: "",
                          agreeToTerms: "",
                        })
                        setError("")
                        setSuccess("")
                      }}
                      className="text-[#40684D] hover:underline font-medium"
                    >
                      {isSignUp ? "Sign in here" : "Create account"}
                    </button>
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  )
}
