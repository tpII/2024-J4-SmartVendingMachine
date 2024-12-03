"use client";
import { useEffect } from 'react';

const handleGoogleCallback = async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code');

  if (code) {
    // Enviar el codigo al backend para obtener la informacion del usuario
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login/google/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code }),
    });

    if (response.ok) {
      const userInfo = await response.json();
      console.log('Informacion del usuario:', userInfo);
      // Aqu puedes almacenar la informacion del usuario en el estado de tu aplicacion o en cookies
    } else {
      console.error('Error al obtener la informacion del usuario');
    }
  }
};

export default function SmartFridgeEcommerce() {
  useEffect(() => {
    // Ejecutar el callback de Google automticamente al montar el componente
    handleGoogleCallback();
    
  }, []); // El array vaco significa que solo se ejecutar una vez al montar

  return (
    <div className="min-h-screen bg-gray-100">
      <p>Google auth callback</p>
    </div>
  );
}
