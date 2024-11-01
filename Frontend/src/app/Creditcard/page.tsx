"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import React, { useState } from 'react';

function SimulatedCreditCardForm() {
  const [form, setForm] = useState({
    cardNumber: '',
    expirationDate: '',
    cvv: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert(`Datos de la tarjeta:
      Número: ${form.cardNumber}
      Fecha de Vencimiento: ${form.expirationDate}
      CVV: ${form.cvv}`);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form onSubmit={handleSubmit}>
        <Card className="w-96 p-4">
          <CardHeader>
            <CardTitle>Registrar Tarjeta de Crédito</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Número de Tarjeta</label>
              <input
                type="text"
                name="cardNumber"
                value={form.cardNumber}
                onChange={handleChange}
                maxLength={16}
                placeholder="1234 5678 9123 4567"
                className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:ring-blue-300"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Fecha de Vencimiento</label>
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
              <label className="block text-sm font-medium text-gray-700">CVV</label>
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
            <Button className="w-full mt-4" type="submit">Enviar</Button>
          </CardContent>
        </Card>
      </form>
    </div>
  );
}

export default SimulatedCreditCardForm;
