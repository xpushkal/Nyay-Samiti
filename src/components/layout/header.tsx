"use client"

import { useState } from "react"
import Image from "next/image";
import Link from "next/link"
import { usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Menu, Scale } from "lucide-react"
import { motion } from "framer-motion"

export default function Header() {
  const [isOpen, setIsOpen] = useState(false)
  const pathname = usePathname()

  const navigation = [
    { name: "Home", href: "/" },
    { name: "Upload Docs", href: "/upload" },
    { name: "How It Works", href: "/how-it-works" },
    { name: "Contact", href: "/contact" },
  ]

  const isActive = (href: string) => pathname === href

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
         {/* Logo */}
<Link href="/" className="flex items-center space-x-2">
  <motion.div
    whileHover={{ rotate: 360 }}
    transition={{ duration: 0.5 }}
    className="flex items-center justify-center w-10 h-10 rounded-lg overflow-hidden"
   
  >
    <Image
      src="/logo.png"
      alt="Nyay-Mitra Logo"
      width={50}
      height={50}
      className="object-contain"
    />
  </motion.div>
  <span
    className="ml-2 text-2xl font-extrabold tracking-tight flex items-center"
    style={{
      letterSpacing: "0.5px",
      fontStyle: "italic",
      color: "#40684D",
      fontFamily: "'Playfair Display', 'Georgia', serif",
      textShadow: "0 1px 6px #dbeadf, 0 0.5px 0 #40684D22",
    }}
  >
    न्याय
    <span
      className="ml-1 font-semibold"
      style={{
        fontStyle: "italic",
        fontWeight: 600,
        fontSize: "1.18em",
        letterSpacing: "1px",
        color: "#40684D",
        fontFamily: "'Playfair Display', 'Georgia', serif",
        textShadow: "0 1px 6px #dbeadf, 0 0.5px 0 #40684D22",
      }}
    >
      Mitra
    </span>
  </span>
</Link>


          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={`text-sm font-medium transition-colors hover:text-[#40684D] relative ${
                  isActive(item.href) ? "text-[#40684D]" : "text-gray-600"
                }`}
              >
                {item.name}
                {isActive(item.href) && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute -bottom-1 left-0 right-0 h-0.5"
                    style={{ backgroundColor: "#40684D" }}
                    initial={false}
                    transition={{ type: "spring", stiffness: 500, damping: 30 }}
                  />
                )}
              </Link>
            ))}
          </nav>

          {/* Desktop Actions */}
          <div className="hidden md:flex items-center space-x-4">
            <Link href="/sign-in">
              <Button className="text-white" style={{ backgroundColor: "#40684D" }}>
                Sign In
              </Button>
            </Link>
          </div>

          {/* Mobile Menu */}
          <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild className="md:hidden">
              <Button variant="ghost" size="sm">
                <Menu className="h-5 w-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-[300px] sm:w-[400px]">
              <div className="flex flex-col space-y-4 mt-8">
                {navigation.map((item) => (
                  <Link
                    key={item.name}
                    href={item.href}
                    onClick={() => setIsOpen(false)}
                    className={`text-lg font-medium transition-colors hover:text-[#40684D] ${
                      isActive(item.href) ? "text-[#40684D]" : "text-gray-600"
                    }`}
                  >
                    {item.name}
                  </Link>
                ))}
                <div className="pt-4 border-t">
                  <Link href="/sign-in" onClick={() => setIsOpen(false)}>
                    <Button className="w-full text-white" style={{ backgroundColor: "#40684D" }}>
                      Sign In
                    </Button>
                  </Link>
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  )
}
