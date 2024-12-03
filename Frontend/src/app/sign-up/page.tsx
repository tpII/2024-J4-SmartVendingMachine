"use client";
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
import { LogIn } from "lucide-react";
import Cookies from "js-cookie";

export default function Login() {
  const [password2, setPassword2] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [phonenumber, setPhonenumber] = useState("");
  const [email, setEmail] = useState("");

  const handleLogin = async () => {
    if (password != password2) {
        alert('Passwords dont match');
        return;
    }

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}api/sign-up/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email,
            password: password,
          }),
        }
      );

      if (response.ok) {
        const data = await response.json();
        console.log(response)

        // Supongamos que el token est en data.token
        Cookies.set("authToken", data.token, { expires: 7 }); // La cookie expira en 7 das
        alert("Sign up exitoso, puede iniciar sesion!");
        window.location.href = "/login";
        console.log("Sign up exitoso");
      } else {
        alert("Error en el sign up");
        console.error("Error en el sign up");
      }
    } catch (error) {
      console.error("Error en la peticion", error);
    }
  };

  const handleLogInEvent = () => {
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
            <Button variant="ghost" onClick={handleLogInEvent}>
              <LogIn className="mr-2 h-4 w-4" />
              Log In
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Sign Up</CardTitle>
            <CardDescription>Create a new account</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              placeholder="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <Input
              placeholder="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Input
              placeholder="Repeat your password"
              type="password"
              value={password2}
              onChange={(e) => setPassword2(e.target.value)}
            />
            <Button className="w-full" onClick={handleLogin}>
              Sign Up
            </Button>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
