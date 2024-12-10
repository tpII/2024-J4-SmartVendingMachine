"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { CheckCircle, ArrowRight, ShoppingBag } from "lucide-react";
import Link from "next/link";


interface OrderItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
}

interface Order {
  id: string;
  date: string;
  items: OrderItem[];
  subtotal: number;
  tax: number;
  total: number;
}


const mockOrder: Order = {
  id: "1234567890",
  date: new Date().toLocaleDateString(),
  items: [
    { id: 1, name: "Fresh Salad", price: 8.99, quantity: 2 },
    { id: 2, name: "Chicken Sandwich", price: 10.99, quantity: 1 },
  ],
  subtotal: 28.97,
  tax: 2.9,
  total: 31.87,
};

export default function ThankYouPage() {
  const [order, setOrder] = useState<Order | null>(null);

  useEffect(() => {
    setOrder(mockOrder);
  }, []);

  if (!order) {
    return <div>Cargando...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <CheckCircle className="mx-auto h-16 w-16 text-green-500" />
          <h1 className="mt-4 text-3xl font-extrabold text-gray-900">
            Gracias por su compra
          </h1>
          <p className="mt-2 text-lg text-gray-600">
            Su pedido ha sido realizado y está siendo procesado.
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Resumen del Pedido</CardTitle>
            <CardDescription>
              Pedido #{order.id} - Realizado el {order.date}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Producto</TableHead>
                  <TableHead>Cantidad</TableHead>
                  <TableHead>Precio</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {order.items.map((item: any) => (
                  <TableRow key={item.id}>
                    <TableCell>{item.name}</TableCell>
                    <TableCell>{item.quantity}</TableCell>
                    <TableCell>
                      ${(item.price * item.quantity).toFixed(2)}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            <div className="mt-4 space-y-2">
              <div className="flex justify-between">
                <span>Subtotal:</span>
                <span>${order.subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span>Impuestos:</span>
                <span>${order.tax.toFixed(2)}</span>
              </div>
              <div className="flex justify-between font-bold">
                <span>Total:</span>
                <span>${order.total.toFixed(2)}</span>
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4">
            <Button asChild className="w-full">
              <Link href="/">
                <ShoppingBag className="mr-2 h-4 w-4" />
                Volver al menu
              </Link>
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
