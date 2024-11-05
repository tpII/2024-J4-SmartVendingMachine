"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import React, { useState } from "react";
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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Formulario enviado"); // <- Esto debería aparecer en la consola cuando envías el formulario.

    // Convertir expirationDate a formato YYYY-MM-DD
    const [month, year] = form.expirationDate.split("/");
    const formattedExpirationDate = `20${year}-${month}`; // Asumiendo que el formato es MM/YY y que el día es el primero del mes

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
            card_number: form.cardNumber,
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


  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">
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
            <Card className="w-96 p-4">
              <CardHeader>
                <CardTitle>Información de Tarjeta de Crédito</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Nombre del Titular
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
