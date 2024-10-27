"use client";

import { useEffect, useState } from 'react';

const MercadoPagoCheckout = () => {
  const [preferenceId, setPreferenceId] = useState(null);

  useEffect(() => {
    const loadMercadoPagoScript = () => {
      const script = document.createElement('script');
      script.src = 'https://sdk.mercadopago.com/js/v2';
      script.async = true;
      script.onload = () => {
        console.log("MercadoPago cargado: ", window.MercadoPago); // Verifica si el script está cargado
  
        if (preferenceId) {
          const mp = new window.MercadoPago('APP_USR-fa852683-3af5-4c37-8d91-765dc0a68c19', {
            locale: 'es-AR',
          });
  
          mp.checkout({
            preference: {
              id: preferenceId,
            },
            render: {
              container: '.mercadopago-button',
              label: 'Pagar',
            },
          });
        }
      };
      document.body.appendChild(script);
    };
  
    if (!window.MercadoPago) {
      loadMercadoPagoScript();
    }
  }, [preferenceId]);
  

  return <div className="mercadopago-button">Holaaa </div>;
};

export default MercadoPagoCheckout;
