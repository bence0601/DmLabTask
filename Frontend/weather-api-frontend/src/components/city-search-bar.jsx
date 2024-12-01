import React, { useState } from "react";
import fetchWeather from "../services/Weather-api";

const WeatherSearch = () => {
  const [city, setCity] = useState(""); // A város neve
  const [weatherData, setWeatherData] = useState(null); // Az időjárás adatai
  const [loading, setLoading] = useState(false); // Töltés állapot
  const [error, setError] = useState(""); // Hiba üzenet

  // A keresési kérés indítása
  const handleSearch = async () => {
    if (!city) {
      setError("Kérjük, adjon meg egy várost!");
      return;
    }

    setLoading(true); // Bekapcsoljuk a töltési állapotot
    setError(""); // Hiba üzenet törlése

    try {
      const data = await fetchWeather(city);
      setWeatherData(data); 
    } catch (error) {
      setError("Hiba történt az időjárás lekérdezése közben.");
    } finally {
      setLoading(false); 
    }
  };

  return (
    <div>
      <input
        type="text"
        value={city}
        onChange={(e) => setCity(e.target.value)} // Beírt város változása
        placeholder="Írja be a város nevét"
      />
      <button onClick={handleSearch} disabled={loading}>
        {loading ? "Töltés..." : "Keresés"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>} {/* Hiba üzenet megjelenítése */}

      {weatherData && (
        <div>
          <h2>Időjárás:</h2>
          <p>{`Város: ${weatherData.city}`}</p>
          <p>{`Hőmérséklet: ${weatherData.temperature}°C`}</p>
          <p>{`Időjárás: ${weatherData.weather}`}</p>
          {/* Itt több adatot is kiírhatsz, pl. szélsebesség, páratartalom */}
        </div>
      )}
    </div>
  );
};

export default WeatherSearch;
