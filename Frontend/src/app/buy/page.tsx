"use client";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import React from "react";
import { useRouter } from "next/navigation";

function TwoButtonsPage() {
  const router = useRouter();

  const handleButton1Click = () => {
    alert("¡Hiciste clic en el Botón 1!");
    // Lógica adicional para este botón (redirigir, hacer un fetch, etc.)
  };

  const handleButton2Click = () => {
    alert("¡Hiciste clic en el Botón 2!");
    // Lógica adicional para este botón (redirigir, hacer un fetch, etc.)
  };

  const goHome = () => {
    router.push("/");
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900" onClick={goHome}>
            Smart Fridge Eats
          </h1>
        </div>
      </header>
      <main>
        <div className="flex items-center justify-center min-h-screen">
          <Card className="w-96 p-7">
            <CardHeader>
              <CardTitle>Gracias por su compra!</CardTitle>
              <CardDescription>
                Antes de pulsar finalizar la compra cierre la puerta.
               </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button
                className="w-full"
                onClick={handleButton1Click}
                variant="default"
              >
                Cancelar
              </Button>
              <Button
                className="w-full"
                onClick={handleButton2Click}
                variant="default"
              >
                Finalizar
              </Button>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}

export default TwoButtonsPage;
