"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { MessageCircle, X, Send } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

export default function FloatingChat() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            transition={{ duration: 0.2 }}
            className="mb-4"
          >
            <Card className="w-80 shadow-2xl border-green-200">
              <CardHeader className="text-white rounded-t-lg" style={{ backgroundColor: "#40684D" }}>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">Nyay-Mitra Support</CardTitle>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setIsOpen(false)}
                    className="text-white hover:bg-white/20"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <span>Online - We typically reply instantly</span>
                </div>
              </CardHeader>
              <CardContent className="p-4">
                <div className="space-y-4 mb-4 max-h-64 overflow-y-auto">
                  <div className="bg-gray-100 rounded-lg p-3">
                    <p className="text-sm text-gray-700">
                      👋 Hi! I'm here to help you with any questions about document simplification. How can I assist you
                      today?
                    </p>
                  </div>

                  <div className="space-y-2">
                    <p className="text-xs text-gray-500">Quick questions:</p>
                    <div className="space-y-1">
                      {[
                        "How does document processing work?",
                        "What file formats do you support?",
                        "Is my data secure?",
                        "How accurate is the AI?",
                      ].map((question, index) => (
                        <button
                          key={index}
                          className="block w-full text-left text-xs bg-blue-50 hover:bg-blue-100 text-blue-700 p-2 rounded transition-colors"
                        >
                          {question}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="flex space-x-2">
                  <input
                    type="text"
                    placeholder="Type your message..."
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2"
                    style={{}}
                  />
                  <Button size="sm" className="text-white" style={{ backgroundColor: "#40684D" }}>
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
        <Button
          onClick={() => setIsOpen(!isOpen)}
          className="w-14 h-14 rounded-full shadow-lg text-white"
          style={{ backgroundColor: "#40684D" }}
        >
          {isOpen ? <X className="h-6 w-6 text-white" /> : <MessageCircle className="h-6 w-6 text-white" />}
        </Button>
      </motion.div>
    </div>
  )
}
