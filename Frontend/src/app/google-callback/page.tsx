"use client";
import { useEffect } from 'react';

const handleGoogleCallback = async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code');

  if (code) {
    // Enviar el código al backend para obtener la información del usuario
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login/google/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code }),
    });

    if (response.ok) {
      const userInfo = await response.json();
      console.log('Información del usuario:', userInfo);
      // Aquí puedes almacenar la información del usuario en el estado de tu aplicación o en cookies
    } else {
      console.error('Error al obtener la información del usuario');
    }
  }
};

export default function SmartFridgeEcommerce() {
  useEffect(() => {
    // Ejecutar el callback de Google automáticamente al montar el componente
    handleGoogleCallback();
    
  }, []); // El array vacío significa que solo se ejecutará una vez al montar

  return (
    <div className="min-h-screen bg-gray-100">
      <p>Google auth callback</p>
    </div>
  );
}
