"use client";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Cookies from "js-cookie";
import { User } from "lucide-react";

function SimulatedCreditCardForm() {
  const router = useRouter();
  const [form, setForm] = useState({
    cardHolderName: "",
    cardNumber: "",
    expirationDate: "",
    cvv: "",
  });
  const [showExplanation, setShowExplanation] = useState(false)

  // Si se redirige desde el home, significa que el usuario recien crea su cuenta y todavia no tiene 
  // una tarjeta cargada, por lo que mostramos un mensaje explicativo
  useEffect(() => {
    // Obtener el valor del parámetro homeRedirect de la URL
    const urlParams = new URLSearchParams(window.location.search);
    const homeRedirect = urlParams.get("homeRedirect");
  
    // Verificar si el parámetro homeRedirect existe y es 'true'
    if (homeRedirect === "true") {
      // Mostramos el mensaje
      setShowExplanation(true);
    } else {
      // No lo mostramos
      setShowExplanation(false);
    }

  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    if (name === "cardNumber") {
      // Remove any non-digit characters
      const digits = value.replace(/\D/g, "");
      // Add a space every 4 characters
      const formatted = digits.replace(/(\d{4})(?=\d)/g, "$1 ").trim();
      // Limit to 19 characters (16 digits + 3 spaces)
      setForm((prev) => ({ ...prev, [name]: formatted.slice(0, 19) }));
    } else if (name === "expirationDate") {
      // Format as MM/YY
      const formatted = value
        .replace(/\D/g, "")
        .replace(/^(\d{2})/, "$1/")
        .slice(0, 5);
      setForm((prev) => ({ ...prev, [name]: formatted }));
    } else {
      setForm((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Formulario enviado"); // <- Esto debería aparecer en la consola cuando envías el formulario.

    // Convertir expirationDate a formato YYYY-MM-DD
    const [month, year] = form.expirationDate.split("/");
    const formattedExpirationDate = `20${year}-${month}`; // Asumiendo que el formato es MM/YY y que el día es el primero del mes

    let string = form.cardNumber; // Suponiendo que 'form.cardNumber' es el valor que contiene la cadena
    let stringSinEspacios = string.replace(/\s+/g, "");

    try {
      console.log(Cookies.get("authToken"));
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}payment/create-card/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${Cookies.get("authToken")}`, // Usa el token guardado en cookies
          },
          body: JSON.stringify({
            card_holder_name: form.cardHolderName,
            card_number: stringSinEspacios,
            expiration_date: formattedExpirationDate,
            cvv: form.cvv,
          }),
        }
      );

      if (response.ok) {
        alert("Tarjeta registrada exitosamente");
        router.push("/cards"); // Redirige al login después de registrar la tarjeta
      } else {
        const errorData = await response.json();
        console.error("Error al registrar la tarjeta:", errorData);
        alert(
          `Error al registrar la tarjeta: ${
            errorData.message || "Verifica los datos ingresados"
          }`
        );
      }
    } catch (error) {
      console.error("Error en la solicitud:", error);
      alert("Hubo un problema al intentar registrar la tarjeta");
    }
  };

  const handleLogout = () => {
    // Eliminar todas las cookies
    const allCookies = Cookies.get(); // Obtener todas las cookies actuales
    // Recorrer y eliminar cada cookie
    for (let cookie in allCookies) {
      Cookies.remove(cookie);
    }
    // Redirigir al usuario a la página de inicio de sesión
    window.location.href = "/login";
  };

  const goHome = () => {
    window.location.href = "/";
  }

  return (
    <div className="min-h-screen bg-gray-100" >
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900" onClick={goHome}>
            Smart Fridge Eats
          </h1>
          <div className="flex items-center space-x-4">
            <Button variant="ghost" onClick={handleLogout}>
              <User className="mr-2 h-4 w-4" />
              Logout
            </Button>
          </div>
        </div>
      </header>
      <main>
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
          <form onSubmit={handleSubmit}>
            <Card className="w-96 p-7">
              <CardHeader>
                <CardTitle>Información de Tarjeta de Crédito</CardTitle>
              </CardHeader>
              { showExplanation ? <CardDescription >
                Para completar tu registro y acceder a todas las funciones de
                nuestra aplicación, es necesario ingresar los datos de tu
                tarjeta de crédito. Esto es indispensable para realizar la
                compra de productos dentro de la plataforma. Aseguramos que tus
                datos estarán completamente protegidos, y que solo se utilizarán
                para procesar las transacciones de compra. Una vez ingresados
                los datos, podrás disfrutar de todas las funcionalidades y
                productos disponibles en nuestra aplicación de manera rápida y
                segura. ¡Gracias por elegirnos!
              </CardDescription> : null }
              <p>-</p>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Nombre completo del titular
                  </label>
                  <input
                    type="text"
                    name="cardHolderName"
                    value={form.cardHolderName}
                    onChange={handleChange}
                    placeholder="Nombre del Titular"
                    className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:ring-blue-300"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Número de Tarjeta
                  </label>
                  <input
                    type="text"
                    name="cardNumber"
                    value={form.cardNumber}
                    onChange={handleChange}
                    maxLength={19}
                    placeholder="1234 5678 9123 4567"
                    className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:ring-blue-300"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Fecha de Vencimiento (MM/YY)
                  </label>
                  <input
                    type="text"
                    name="expirationDate"
                    value={form.expirationDate}
                    onChange={handleChange}
                    maxLength={5}
                    placeholder="MM/YY"
                    className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:ring-blue-300"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    CVV
                  </label>
                  <input
                    type="text"
                    name="cvv"
                    maxLength={3}
                    value={form.cvv}
                    onChange={handleChange}
                    placeholder="123"
                    className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:ring-blue-300"
                  />
                </div>
                <Button className="w-full mt-4" type="submit">
                  Enviar
                </Button>
              </CardContent>
            </Card>
          </form>
        </div>
      </main>
    </div>
  );
}

export default SimulatedCreditCardForm;
