'use client'

import { useRouter, useParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import Cookies from 'js-cookie'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2 } from "lucide-react"

export default function QRScanPage() {
  const router = useRouter()
  const { id } = useParams()
  const [sessionStatus, setSessionStatus] = useState<'loading' | 'opened' | 'declined' | null>(null)
  const [requestSended, setRequestSended] = useState(false);
  
  const startSession = async () => {
    const sessionCookie = Cookies.get('authToken')
    if (!sessionCookie) {
      router.push('/login')
      return
    }

    setSessionStatus('loading')
    console.log(sessionCookie)
    try {
      const response = await fetch(`http://localhost:8000/market/fridge/start-session/${id}/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${sessionCookie}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        setSessionStatus('opened')
      } else {
        setSessionStatus('declined')
      }
    } catch (error) {
      console.error('Error starting session:', error)
      setSessionStatus('declined')
    }
  }
  
  useEffect(() => {
    if (!requestSended) {
      setRequestSended(true);
      startSession();
    }
  }, [])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>Sesion de compra</CardTitle>
        </CardHeader>
        <CardContent>
          {sessionStatus === 'loading' && (
            <div className="flex flex-col items-center space-y-4">
              <Loader2 className="h-8 w-8 animate-spin" />
              <p>Iniciando sesion...</p>
            </div>
          )}
          {sessionStatus === 'opened' && (
            <div className="text-center space-y-4">
              <p className="text-green-600 font-semibold">Sesion abierta exitosamente!</p>
              <p className="font-light">La heladera esta abierta, ya puede retirar productos.</p>
              <p>ID de Heladera: {id}</p>
              <Button className='m-3' onClick={() => router.push('/')}>Finalizar compra</Button>
              <Button className='m-3' onClick={() => router.push('/')}>Cancelar compra</Button>
            </div>
          )}
          {sessionStatus === 'declined' && (
            <div className="text-center space-y-4">
              <p className="text-red-600 font-semibold">No se ha podido abrir la sesion!</p>
              <p>No hemos podido abrir tu sesion en la heladera: {id}</p>
              <Button onClick={() => router.push('/')}>Intentar de nuevo</Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}