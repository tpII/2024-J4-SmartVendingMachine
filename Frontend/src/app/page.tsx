"use client";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import { Trash2, User } from "lucide-react";
import Cookies from "js-cookie";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { QRScanner } from "@/components/ui/qrscanner";
import { DarkModeMap } from "@/components/ui/darkmodemap";

// Mock data for fo

const foodItems = [
  {
    id: 1,
    name: "Fresh Salad",
    price: 8.99,
    image: "/food-items/fresh_salad.jpg", // Ajustar extension si no la tiene
  },
  {
    id: 2,
    name: "Chicken Sandwich",
    price: 10.99,
    image: "/food-items/chicken_sandwich.jpeg",
  },
  {
    id: 3,
    name: "Fruit Bowl",
    price: 6.99,
    image: "/food-items/fruit_bowl.jpeg",
  },
  {
    id: 4,
    name: "Veggie Wrap",
    price: 9.99,
    image: "/food-items/veggie_wrap.jpg",
  },
];

interface FoodItem {
  id: number;
  name: string;
  price: number;
  image: string;
}

export default function SmartFridgeEcommerce() {
  const [activeTab, setActiveTab] = useState("browse");

  useEffect(() => {
    const checkUserCard = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}payment/check-card/`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${Cookies.get("authToken")}`, // Usa el token guardado en cookies
              "Content-Type": "application/json",
            },
          }
        );
        if (!response.ok) {
          throw new Error("Error en la respuesta de la API");
        }

        const data = await response.json();
        if (!data.has_card) {
          window.location.href = "/cards/add?homeRedirect=true";
        } else {
          console.error("El usuario tiene tarjeta...");
        }
      } catch (error) {
        console.error("Error en la peticion", error);
      }
    };
    checkUserCard();
  }, []);

  const handleLogout = () => {
    // Eliminar todas las cookies
    const allCookies = Cookies.get(); // Obtener todas las cookies actuales
    // Recorrer y eliminar cada cookie
    for (let cookie in allCookies) {
      Cookies.remove(cookie);
    }
    // Redirigir al usuario a la pgina de inicio de sesion
    window.location.href = "/login";
  };

  const handleAddCreditCard = () => {
    window.location.href = "/cards";
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">
            Smart Fridge Eats
          </h1>
          <div className="flex items-center space-x-4">
            <Button variant="ghost" onClick={handleAddCreditCard}>
              <Card className="mr-2 h-4 w-4" />
              Credit Cards
            </Button>
            <Button variant="ghost" onClick={handleLogout}>
              <User className="mr-2 h-4 w-4" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="browse">Menu</TabsTrigger>
            <TabsTrigger value="qr-scanner">Scan QR</TabsTrigger>
            <TabsTrigger value="map">Nearby Fridges</TabsTrigger>
          </TabsList>
          <TabsContent value="browse">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">
              {foodItems.map((item) => (
                <Card key={item.id}>
                  <CardHeader>
                    <CardTitle>{item.name}</CardTitle>
                    <CardDescription>${item.price.toFixed(2)}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <img
                      src={item.image}
                      alt={item.name}
                      className="w-full h-40 object-cover rounded-md"
                    />
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
          <TabsContent value="qr-scanner">
            <Card>
              <CardHeader>
                <CardTitle>Scan QR Code</CardTitle>
                <CardDescription>
                  Use your device's camera to scan a QR code
                </CardDescription>
              </CardHeader>
              <CardContent>
                <QRScanner />
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="map">
            <Card>
              <CardHeader>
                <CardTitle>Dark Mode Map</CardTitle>
                <CardDescription>
                  Google Maps in dark mode with zoom level 14
                </CardDescription>
              </CardHeader>
              <CardContent>
                <DarkModeMap />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
