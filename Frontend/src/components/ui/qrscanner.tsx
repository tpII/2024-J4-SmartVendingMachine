"use client"

import React, { useState, useRef, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Camera, XCircle } from "lucide-react"

export function QRScanner() {
  const [scanning, setScanning] = useState(false)
  const [result, setResult] = useState<string | null>(null)
  const videoRef = useRef<HTMLVideoElement>(null)

  useEffect(() => {
    let stream: MediaStream | null = null

    const startCamera = async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
        if (videoRef.current) {
          videoRef.current.srcObject = stream
        }
      } catch (err) {
        console.error("Error accessing the camera:", err)
      }
    }

    if (scanning) {
      startCamera()
    }

    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop())
      }
    }
  }, [scanning])

  const handleScan = () => {
    setScanning(true)
    setResult(null)
  }

  const handleStop = () => {
    setScanning(false)
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = (videoRef.current.srcObject as MediaStream).getTracks()
      tracks.forEach(track => track.stop())
    }
  }

  // In a real application, you would implement QR code detection here
  // For this example, we'll simulate a scan after 5 seconds
  useEffect(() => {
    if (scanning) {
      const timer = setTimeout(() => {
        setResult("https://example.com/scanned-qr-code")
        setScanning(false)
      }, 5000)

      return () => clearTimeout(timer)
    }
  }, [scanning])

  return (
    <div className="space-y-4">
      {!scanning && !result && (
        <Button onClick={handleScan} className="w-full">
          <Camera className="mr-2 h-4 w-4" /> Start Scanning
        </Button>
      )}
      {scanning && (
        <div className="relative">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="w-full h-64 object-cover rounded-md"
          />
          <Button
            variant="secondary"
            className="absolute top-2 right-2"
            onClick={handleStop}
          >
            <XCircle className="h-4 w-4" />
          </Button>
        </div>
      )}
      {result && (
        <div className="p-4 bg-muted rounded-md">
          <p className="font-medium">Scanned Result:</p>
          <p className="text-sm break-all">{result}</p>
          <Button onClick={() => setResult(null)} className="mt-2">
            Scan Again
          </Button>
        </div>
      )}
    </div>
  )
}