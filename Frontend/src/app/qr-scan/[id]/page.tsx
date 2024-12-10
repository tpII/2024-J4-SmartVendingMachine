'use client'

import { useRouter, useParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import Cookies from 'js-cookie'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2 } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

export default function QRScanPage() {
  const router = useRouter()
  const { id } = useParams()
  const [sessionStatus, setSessionStatus] = useState<'loading-start-session' | 'loading-end-session' | 'opened' | 'declined' | null>(null)
  const [requestSended, setRequestSended] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false)

  const startSession = async () => {
    const sessionCookie = Cookies.get('authToken')
    if (!sessionCookie) {
      router.push('/login')
      return
    }

    setSessionStatus('loading-start-session')
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

  const openModal = () => {
    setIsModalOpen(true)
  }

  const closeModal = () => {
    setIsModalOpen(false)
  }

  const handleOkClick = () => {
    closeModal()
    handleEndSession()
  }

  const handleEndSession = async () => {
    const sessionCookie = Cookies.get('authToken')
    setSessionStatus('loading-end-session')

    try {
      const response = await fetch(`http://localhost:8000/market/fridge/end-session/${id}/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${sessionCookie}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const responseData = await response.json()
        console.log(responseData)
        //const queryString = new URLSearchParams({ data: JSON.stringify(responseData) }).toString()
        //router.push(`/thank-you?${queryString}`)
      } else {
        setSessionStatus('declined')
      }
    } catch (error) {
      console.error('Error ending session:', error)
      setSessionStatus('declined')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>Sesion de compra</CardTitle>
        </CardHeader>
        <CardContent>
        {sessionStatus === 'loading-end-session' && (
          <div className="flex flex-col items-center space-y-4">
            <Loader2 className="h-8 w-8 animate-spin" />
            <p>Procesando...</p>
          </div>
        )}
          {sessionStatus === 'loading-start-session' && (
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
              <Button className='m-3' onClick={openModal}>Finalizar compra</Button>
              {/* <Button className='m-3' onClick={() => router.push('/')}>Cancelar compra</Button> */}
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

      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Confirmar cierre de sesión</DialogTitle>
            <DialogDescription>
              Asegúrese que la puerta esté cerrada antes de finalizar. Presione Ok si ya fue cerrada.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={closeModal}>
              Cancelar
            </Button>
            <Button onClick={handleOkClick}>
              Ok
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}