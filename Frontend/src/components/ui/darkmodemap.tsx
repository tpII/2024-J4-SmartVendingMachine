"use client";

import React, { useEffect, useState } from "react";
import { GoogleMap, Marker, useJsApiLoader } from "@react-google-maps/api";
import Cookies from "js-cookie";

const containerStyle = {
  width: "100%",
  height: "80vh",
};

const center = {
  lat: -34.921373331186786,
  lng: -57.95463789289836,
};

const mapOptions = {
  zoom: 14,
  styles: [
    { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
    { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
    { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
    {
      featureType: "administrative.locality",
      elementType: "labels.text.fill",
      stylers: [{ color: "#d59563" }],
    },
    {
      featureType: "poi",
      elementType: "labels.text.fill",
      stylers: [{ color: "#d59563" }],
    },
    {
      featureType: "poi.park",
      elementType: "geometry",
      stylers: [{ color: "#263c3f" }],
    },
    {
      featureType: "poi.park",
      elementType: "labels.text.fill",
      stylers: [{ color: "#6b9a76" }],
    },
    {
      featureType: "road",
      elementType: "geometry",
      stylers: [{ color: "#38414e" }],
    },
    {
      featureType: "road",
      elementType: "geometry.stroke",
      stylers: [{ color: "#212a37" }],
    },
    {
      featureType: "road",
      elementType: "labels.text.fill",
      stylers: [{ color: "#9ca5b3" }],
    },
    {
      featureType: "road.highway",
      elementType: "geometry",
      stylers: [{ color: "#746855" }],
    },
    {
      featureType: "road.highway",
      elementType: "geometry.stroke",
      stylers: [{ color: "#1f2835" }],
    },
    {
      featureType: "road.highway",
      elementType: "labels.text.fill",
      stylers: [{ color: "#f3d19c" }],
    },
    {
      featureType: "transit",
      elementType: "geometry",
      stylers: [{ color: "#2f3948" }],
    },
    {
      featureType: "transit.station",
      elementType: "labels.text.fill",
      stylers: [{ color: "#d59563" }],
    },
    {
      featureType: "water",
      elementType: "geometry",
      stylers: [{ color: "#17263c" }],
    },
    {
      featureType: "water",
      elementType: "labels.text.fill",
      stylers: [{ color: "#515c6d" }],
    },
    {
      featureType: "water",
      elementType: "labels.text.stroke",
      stylers: [{ color: "#17263c" }],
    },
    {
      featureType: "poi",
      elementType: "all",
      stylers: [{ visibility: "off" }],
    },
    {
      featureType: "transit",
      elementType: "all",
      stylers: [{ visibility: "off" }],
    },
    { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
    {
      featureType: "road",
      elementType: "geometry",
      stylers: [{ color: "#38414e" }],
    },
    {
      featureType: "road",
      elementType: "geometry.stroke",
      stylers: [{ color: "#212a37" }],
    },
    {
      featureType: "road.highway",
      elementType: "geometry",
      stylers: [{ color: "#746855" }],
    },
    {
      featureType: "road.highway",
      elementType: "geometry.stroke",
      stylers: [{ color: "#1f2835" }],
    },
  ],
};

export function DarkModeMap() {
  const { isLoaded } = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: "AIzaSyC2XaW_3rmpdaqrgIgYHR67R1uFzMzMN_w", // Coloca aquí tu API key
  });

  const [map, setMap] = useState(null);
  const [markers, setMarkers] = useState([]); // Estado para almacenar las ubicaciones de las heladeras

  const onLoad = React.useCallback(function callback(map: any) {
    setMap(map);
  }, []);

  const onUnmount = React.useCallback(function callback(map: any) {
    setMap(null);
  }, []);

  // Función para obtener las ubicaciones de las heladeras
  const fetchHeladeras = async () => {
    try {
      const response = async () => {
        try {
          const res = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}market/fridge/geolocations/`,
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
          console.log("res", res)
          const data = await res.json();
          console.log("data", data);
          setMarkers(Object.values(data)); // Almacena las ubicaciones en el estado
        } catch (error) {
          console.error("Error en la peticion:", error);
        }
      };

    } catch (error) {
      console.error("Error al obtener las ubicaciones de las heladeras:", error);
    }
  };

  // Cargar las ubicaciones al montar el componente
  useEffect(() => {
    fetchHeladeras();
  }, []);

  return isLoaded ? (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      options={mapOptions}
      onLoad={onLoad}
      onUnmount={onUnmount}
    >
      {/* Renderizar marcadores */}
      {markers.map((location: any, index) => (
        <Marker
          key={index}
          position={{ lat: location.lat, lng: location.lng }}
          icon={{
            url: "/public/heladera.png", 
            scaledSize: new window.google.maps.Size(40, 40), // Tamaño del icono
          }}
        />
      ))}
    </GoogleMap>
  ) : (
    <></>
  );
}
