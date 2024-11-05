"use client";
import { Suspense, useEffect, useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  CreditCard as CreditCardIcon,
  Loader2,
  PlusCircle,
  Trash2,
  User,
} from "lucide-react";
import Cookies from "js-cookie";
import Link from "next/link";

// Types
type CreditCard = {
  card_holder_name: string;
  card_number: string;
  cvv: string;
  expiration_date: string;
  id: number;
  user: number;
  favourite: boolean;
};

// Componente de lista de tarjetas de crédito
function CreditCardList() {
  const [cards, setCards] = useState<CreditCard[]>([]);

  useEffect(() => {
    const fetchCards = async () => {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}payment/credit-cards/`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${Cookies.get("authToken")}`,
            },
          }
        );
        if (!res.ok) {
          alert("Error al cargar tarjetas!");
          return;
        }

        const data = await res.json();
        console.log(data);
        setCards(data);
      } catch (error) {
        console.error("Error en la petición:", error);
      }
    };

    fetchCards();
  }, []);

  if (cards.length === 0) {
    return (
      <p className="text-center text-muted-foreground">
        No credit cards found.
      </p>
    );
  }

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
    <div>
      <ul className="space-y-4">
        {cards.map((card) => (
          <li key={card.id}>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  {card.card_number}
                </CardTitle>
                <CreditCardIcon className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Titular: {card.card_holder_name}
                </CardDescription>
                <CardDescription>
                  Expiration date: {card.expiration_date}
                </CardDescription>
              </CardContent>
              <CardFooter className="flex justify-between">
                <DeleteCardButton cardId={card.id} />
                {!card.favourite && <SetDefaultCardButton cardId={card.id} />}
              </CardFooter>
            </Card>
          </li>
        ))}
      </ul>
    </div>
  );
}

// Botones interactivos
function AddCardButton() {
  const handleAddCard = () => {
    console.log("Add card clicked");
    window.location.href = "/cards/add";
  };

  return (
    <Button onClick={handleAddCard}>
      <PlusCircle className="mr-2 h-4 w-4" />
      Add New Card
    </Button>
  );
}

function DeleteCardButton({ cardId }: { cardId: number }) {
  const handleDeleteCard = async () => {
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}payment/delete-card/${cardId}/`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${Cookies.get("authToken")}`,
          },
        }
      );
      if (!res) {
        alert("Error al eliminar la tarjeta!");
        return;
      }

      const data = await res.json();
      alert("Error al eliminar la tarjeta!");
      console.log(data);
      window.location.href = "/cards";
    } catch (error) {
      alert("Error al eliminar la tarjeta!");
    }
  };

  return (
    <Button variant="destructive" size="sm" onClick={handleDeleteCard}>
      <Trash2 className="mr-2 h-4 w-4" />
      Delete
    </Button>
  );
}

function SetDefaultCardButton({ cardId }: { cardId: number }) {
  const handleSetDefault = async () => {
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}payment/credit-cards/add-favourite/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${Cookies.get("authToken")}`,
          },
          body: JSON.stringify({
            id: cardId,
          }),
        }
      );
      if (!res) {
        alert("Error al asociar la tarjeta como favorita!");
        return;
      }

      const data = await res.json();
      console.log(data);
      window.location.href = "/cards";
    } catch (error) {
      alert("Error al asociar la tarjeta como favorita!");
      return;
    }
  };

  return (
    <Button variant="secondary" size="sm" onClick={handleSetDefault}>
      Set as Default
    </Button>
  );
}

// Componente principal de la página
export default function CreditCardsPage() {
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
    <div className="container mx-auto py-10">
      <header className="bg-white shadow-sm">
        <Link href="/">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">
              Smart Fridge Eats
            </h1>
            <h1 className="text-2xl font-bold text-gray-900">
              Your credit cards
            </h1>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" onClick={handleLogout}>
                <User className="mr-2 h-4 w-4" />
                Logout
              </Button>
            </div>
          </div>
        </Link>
      </header>
      <Suspense fallback={<Loader2 className="h-6 w-6 animate-spin" />}>
        <CreditCardList />
      </Suspense>
      <div className="mt-6">
        <AddCardButton />
      </div>
    </div>
  );
}
