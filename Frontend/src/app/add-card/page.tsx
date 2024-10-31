import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Cookies from "js-cookie";

export default function AddCreditCard() {
  const [cardNumber, setCardNumber] = useState("");
  const [expirationDate, setExpirationDate] = useState("");
  const [cvv, setCvv] = useState("");
  const [cardHolderName, setCardHolderName] = useState("");

  const handleAddCard = async () => {
    // Validaciones básicas
    if (cardNumber.length !== 16) {
      alert("The card number must be 16 digits.");
      return;
    }
    if (!/^\d{4}-\d{2}$/.test(expirationDate)) {
      alert("The expiration date must be in the format YYYY-MM.");
      return;
    }
    if (cvv.length < 3 || cvv.length > 4) {
      alert("The CVV must be 3 or 4 digits.");
      return;
    }

    try {
      const token = Cookies.get("authToken");
      if (!token) {
        alert("You must be logged in to add a credit card.");
        return;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/credit-card/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          card_number: cardNumber,
          expiration_date: expirationDate,
          cvv: cvv,
          card_holder_name: cardHolderName,
        }),
      });

      if (response.ok) {
        alert("Credit card added successfully!");
        window.location.href = "/dashboard";
      } else {
        alert("Failed to add credit card");
      }
    } catch (error) {
      console.error("Request error", error);
      alert("An error occurred. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Smart Fridge Eats</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Add Credit Card</CardTitle>
            <CardDescription>Enter your card details</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              placeholder="Card Number"
              type="text"
              value={cardNumber}
              onChange={(e) => setCardNumber(e.target.value)}
              maxLength={16}
            />
            <Input
              placeholder="Expiration Date (YYYY-MM)"
              type="text"
              value={expirationDate}
              onChange={(e) => setExpirationDate(e.target.value)}
            />
            <Input
              placeholder="CVV"
              type="text"
              value={cvv}
              onChange={(e) => setCvv(e.target.value)}
              maxLength={4}
            />
            <Input
              placeholder="Card Holder Name"
              type="text"
              value={cardHolderName}
              onChange={(e) => setCardHolderName(e.target.value)}
            />
            <Button className="w-full" onClick={handleAddCard}>
              Add Credit Card
            </Button>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
